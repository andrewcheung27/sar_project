import json
from google import genai
from sar_project.agents.base_agent import SARBaseAgent


# message to explain the LLM's role in the SAR system
system_message = """You are the Operations Section Chief for Search and Rescue (SAR) operations. Your role is to:
            1. Follow the mission objectives given by the Incident Commander.
            2. Deploy Search and Rescue teams.
            3. Send information to the Search and Rescue teams in order to achieve the mission objectives.
            4. Adapt strategies based on field reports given by the Search and Rescue teams.
            """
# message to tell the LLM to update its knowledge base (string input, JSON output)
kb_message = """Your current task is to update your knowledge base with information provided by the Incident Commander. 
If there is any unknown information, provide a description in the 'unknown_information' field. 
Convert the following information into JSON:
"""
# message to tell the LLM to make a list of mission objectives, in order of highest to lowest importance
mission_objectives_message = """Your current task is to determine your mission objectives based on the instructions provided by the Incident Commander. 
Convert the following objectives into JSON, and rank them in order of highest to lowest importance:
"""

# schemas for putting information in the knowledge base. 
# the LLM will take text input and generate JSON according to one of these schemas.
# documentation: https://ai.google.dev/gemini-api/docs/structured-output?lang=python
terrain_schema = {
    "type": "OBJECT",
    "properties": {
        "description": {"type": "STRING"}, 
        "elevation": {"type": "INTEGER"},
        "obstacles": {"type": "ARRAY", "items": {"type": "STRING"}},
        "unknown_information": {"type": "STRING"}
    },
    "required": ["description", "elevation", "obstacles", "unknown_information"]
}
weather_schema = {
    "type": "OBJECT",
    "properties": {
        "description": {"type": "STRING"}, 
        "temperature": {"type": "INTEGER"},
        "wind_speed": {"type": "INTEGER"},
        "unknown_information": {"type": "STRING"}
    },
    "required": ["description", "temperature", "wind_speed", "unknown_information"]
}
resources_schema = {
    "type": "ARRAY", 
    "items": {
        "type": "OBJECT", 
        "properties": {
            "name": {"type": "STRING"}, 
            "availability": {"type": "STRING"}, 
            "location": {"type": "STRING"}
        }, 
        "required": ["name", "availability", "location"]
    }
}
# schema for storing a list of mission objectives
mission_objectives_schema = {
    "type": "ARRAY", 
    "items": {
        "type": "STRING"
    }
}
# schema for storing a list of Team Search Plans, with one plan for each Search Team
team_search_plan_schema = {
    "type": "ARRAY", 
    "items": {
        "type": "OBJECT", 
        "properties": {
            "search_team_number": {"type": "INTEGER"}, 
            "plan": {"type": "STRING"}, 
        }, 
        "required": ["search_team_number", "plan"]
    }
}


class OperationsSectionChiefAgent(SARBaseAgent):
    def __init__(self, name="operations_section_chief", knowledge_base=None):
        super().__init__(
            name=name,
            role="Operations Section Chief",
            system_message=system_message, 
            knowledge_base=knowledge_base
        )
        self.genai_client = genai.Client()
        self.mission_objectives = []
        self.search_team_info = []


    def process_request(self, message: dict) -> dict:
        """Process a request from either the Incident Commander or Search Team Leader."""
        try:
            # need to know who sent the message
            if "source" not in message:
                raise ValueError("Message must provide 'source' key")

            if message["source"] == "incident_commander":
                return self._process_request_from_incident_commander(message)
            elif message["source"] == "search_team_leader":
                return self._process_request_from_search_team_leader(message)
            else:
                raise ValueError("Invalid message source")

        except Exception as e:
            return {"error": str(e)}


    def _process_request_from_incident_commander(self, message: dict) -> dict:
        """Process a request from the Incident Commander, which should outline 
        mission objectives and provide information for the knowledge base.
        """
        response = {}

        # require location
        if "location" not in message:
            raise ValueError("Message must provide 'location' key")

        # update knowledge base
        kb_updated = self._update_knowledge_base(message)
        response["knowledge_base_updated"] = kb_updated

        # get mission objectives
        mission_objectives_understood = self._process_mission_objectives(message)
        response["mission_objectives_understood"] = mission_objectives_understood
        # early return if we didn't get mission objectives
        if not mission_objectives_understood:
            return response

        if "search_team_info" in message and type(message["search_team_info"]) == list:
            self.search_team_info = message["search_team_info"]

        # make a search plan
        plan = self._create_search_plan()
        response["search_plan"] = plan

        # split the search plan into a plan for each Search Team
        search_team_plans = self._split_search_plan(self.search_team_info, plan)
        if len(search_team_plans) > 0:
            # sort ascending by search team number
            search_team_plans.sort(key=lambda x: x["search_team_number"])
            # add to response
            response["search_team_plans"] = search_team_plans
            # send instructions to Search Team Leaders
            for p in search_team_plans:
                # TODO: search_team_number is based on structured output generated by LLM from search_team_info. is there a way to make sure the LLM doesn't get the number wrong?
                self._send_plan_to_search_team_leader(p["plan"], p["search_team_number"])

        return response


    def _process_request_from_search_team_leader(self, message: dict) -> dict:
        # TODO
        pass


    def _send_plan_to_search_team_leader(self, plan: str, search_team_leader_index: int):
        """Send plan to a Search Team Leader based on index."""
        # TODO: send plan to the Search Team Leader
        pass


    def _update_knowledge_base(self, message: dict) -> bool:
        """Updates the agent's knowledge base based on a message. 
        Return True if knowledge base was updated.
        """
        kb_updated = False
        prompt = system_message + kb_message

        if "terrain_data" in message:
            prompt += message["terrain_data"]
            response = self._text_to_kb_data(prompt, terrain_schema)
            self.kb.update_terrain(message["location"], response)
            kb_updated = True

        if "weather_data" in message:
            prompt += message["weather_data"]
            response = self._text_to_kb_data(prompt, weather_schema)
            self.kb.update_weather(message["location"], response)
            kb_updated = True

        if "resource_status" in message:
            prompt += message["resource_status"]
            response = self._text_to_kb_data(prompt, resources_schema)
            for resource_info in response:
                resource_name = resource_info.pop("name")
                self.kb.update_resource_status(resource_name, resource_info)
                kb_updated = True

        return kb_updated


    def _process_mission_objectives(self, message: dict) -> bool:
        """Given a message that may have mission objectives 
        (message["mission_objectives"] should be a string), makes a list of mission objectives.
        Returns True if the objectives could be identified, False otherwise.
        """
        if "mission_objectives" not in message:
            return False

        prompt = system_message + mission_objectives_message + message["mission_objectives"]
        response = self._text_to_kb_data(prompt, mission_objectives_schema)

        self.mission_objectives = response
        return True


    def _create_search_plan(self) -> str:
        """Uses mission objectives and knowledge base to generate a search plan."""
        # TODO: implement functionality to specify different resources for each Search Team

        # make prompt with all the info
        prompt = system_message 
        prompt += f"Your current task is to create a search plan based on the mission objectives and other information. \n"
        prompt += f"The mission objectives are: {self.mission_objectives} \n"
        if len(self.search_team_info) > 0:
            prompt += f"Here is information about the available Search Teams: {self.search_team_info} \n"
        prompt += f"This is the terrain information: {self.kb.terrain_data} \n"
        prompt += f"This is the weather information: {self.kb.weather_data} \n"
        prompt += f"And finally, these are the available resources: {self.kb.resource_status}"

        response = self.genai_client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        return response.text


    def _split_search_plan(self, search_team_info: list, search_plan: str):
        """Input: A Search Plan generated by self._create_search_plan().
        Output: A Python object representing the generated output.
        """
        # don't do anything without search team info
        if type(search_team_info) != list or len(search_team_info) == 0:
            return []

        prompt = f"Your current task is to divide the Search Plan into plans for each individual Search Team."
        prompt += f"The sub-plans will be shared with the corresponding Search Team Leaders. \n"
        prompt += f"This is the information about the {len(search_team_info)} Search Teams: {search_team_info} \n"
        prompt += f"This is the Search Plan to split up: {search_plan} \n"

        response = self._generate_json_str(prompt, team_search_plan_schema)
        return json.loads(response)


    def _text_to_kb_data(self, prompt: str, schema):
        """Input: A prompt and a Google Gemini JSON schema to specify the JSON output.
        Output: A Python object representing the generated output.
        """
        response = self._generate_json_str(prompt, schema)
        return json.loads(response)


    # https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/control-generated-output
    def _generate_json_str(self, prompt: str, response_schema: dict):
        """Based on a prompt, generates JSON according to the specified schema."""
        response = self.genai_client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt, 
            config={
                "response_mime_type": "application/json",
                "response_schema": response_schema
            }
        )
        return response.text


    def update_status(self, status):
        """Update the agent's status"""
        self.status = status
        return {"status": "updated", "new_status": status}


    def get_status(self):
        """Get the agent's current status"""
        return getattr(self, "status", "unknown")
