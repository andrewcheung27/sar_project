from sar_project.agents.base_agent import SARBaseAgent
import google.generativeai as genai


class OperationsSectionChiefAgent(SARBaseAgent):
    def __init__(self, name="operations_section_chief", knowledge_base=None):
        super().__init__(
            name=name,
            role="Operations Section Chief",
            system_message="""You are the Operations Section Chief for Search and Rescue (SAR) operations. Your role is to:
            1. Follow the mission objectives given by the Incident Commander
            2. Deploy Search and Rescue teams
            3. Send information to the Search and Rescue teams in order to achieve the mission objectives
            4. Adapt strategies based on field reports given by the Search and Rescue teams""", 
            knowledge_base=knowledge_base
        )
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
            self.kb.update_terrain(message["location"], message["terrain_data"])
            kb_updated = True
        if "weather_data" in message:
            self.kb.update_weather(message["location"], message["weather_data"])
            kb_updated = True
        if "resources" in message:
            for r in message["resources"].keys():
                self.kb.update_resource_status(r, message["resources"][r])
            kb_updated = True

        return kb_updated


    # function copied from Ashton Alonge's message on Slack
    def _query_gemini(self, prompt, model="gemini-pro", max_tokens=200):
        """Query Google Gemini API and return response."""
        try:
            response = genai.GenerativeModel(model).generate_content(prompt)
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
