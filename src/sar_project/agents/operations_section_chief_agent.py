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
Convert the following information into JSON:
"""

# schemas for putting information in the knowledge base. 
# the LLM will take text input and generate JSON according to one of these schemas.
terrain_schema = {
    "type": "OBJECT",
    "properties": {
        "description": {"type": "STRING"}, 
        "elevation": {"type": "INTEGER"},
        "obstacles": {"type": "ARRAY", "items": {"type": "STRING"}},
    },
    "required": ["description", "elevation", "obstacles"]
}
weather_schema = {
    "type": "OBJECT",
    "properties": {
        "description": {"type": "STRING"}, 
        "temperature": {"type": "INTEGER"},
        "wind_speed": {"type": "INTEGER"},
    },
    "required": ["description", "temperature", "wind_speed"]
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


    def process_request(self, message: dict):
        try:
            # need to know who sent the message
            if "source" not in message:
                return {"error": "Message does not have a source"}

            if message["source"] == "incident_commander":
                return self._process_request_from_incident_commander(message)
            elif message["source"] == "search_team_leader":
                return self._process_request_from_search_team_leader(message)
            else:
                return {"error": "Unexpected message source"}

        except Exception as e:
            return {"error": str(e)}


    def _process_request_from_incident_commander(self, message: dict):
        response = {}

        # require location
        if "location" not in message:
            return {"error": "Location was not provided"}

        # update knowledge base
        kb_updated = self._update_knowledge_base(message)
        response["knowledge_base_updated"] = kb_updated

        # get mission objectives
        if "mission_objectives" in message:
            self.mission_objectives = message["mission_objectives"]

            # TODO: process mission objectives

            # indicate that mission objectives are understood
            response["mission_objectives_understood"] = True

            # TODO: send instructions to Search Team Leaders

        return response


    def _process_request_from_search_team_leader(self, message: dict):
        # TODO
        pass


    def _update_knowledge_base(self, message: dict) -> bool:
        """Update the agent's knowledge base based on a message. 
        Return True if knowledge base was updated.
        """
        kb_updated = False

        if "terrain_data" in message:
            response, error = self._text_to_kb_data(terrain_schema, message["terrain_data"])
            if error is None:
                self.kb.update_terrain(message["location"], response)
                kb_updated = True
            else:
                print(error)

        if "weather_data" in message:
            response, error = self._text_to_kb_data(weather_schema, message["weather_data"])
            if error is None:
                self.kb.update_weather(message["location"], response)
                kb_updated = True
            else:
                print(error)
        
        if "resource_status" in message:
            response, error = self._text_to_kb_data(resources_schema, message["resource_status"])
            if error is None:
                for resource_info in response:
                    resource_name = resource_info.pop("name")
                    self.kb.update_resource_status(resource_name, resource_info)
                kb_updated = True
            else:
                print(error)

        return kb_updated


    def _text_to_kb_data(self, schema, text: str) -> tuple:
        """Input: Google Gemini JSON schema and text to convert into JSON.
        Output: 2-Tuple of the JSON result (made of lists/dicts) 
        and an error message, which is None if there is no error.
        """
        prompt = system_message + kb_message + text
        response = self._generate_json_str(prompt, schema)

        if (response.startswith("Error")):
            return {}, response

        # return parsed JSON
        try:
            parsed_response = json.loads(response)
            return parsed_response, None
        except Exception as e:
            return {}, f"Error: {e}"


    # https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/control-generated-output
    def _generate_json_str(self, prompt, response_schema):
        """Based on a prompt, generates JSON according to the specified schema."""
        try:
            response = self.genai_client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt, 
                config={
                    "response_mime_type": "application/json",
                    "response_schema": response_schema
                }
            )
            return response.text
        except Exception as e:
            return f"Error: {e}"


    def update_status(self, status):
        """Update the agent's status"""
        self.status = status
        return {"status": "updated", "new_status": status}


    def get_status(self):
        """Get the agent's current status"""
        return getattr(self, "status", "unknown")
