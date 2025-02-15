from sar_project.agents.base_agent import SARBaseAgent
import google.generativeai as genai


class OperationsSectionChiefAgent(SARBaseAgent):
    def __init__(self, name="operations_section_chief"):
        super().__init__(
            name=name,
            role="Operations Section Chief",
            system_message="""You are the Operations Section Chief for Search and Rescue (SAR) operations. Your role is to:
            1. Follow the mission objectives given by the Incident Commander
            2. Deploy Search and Rescue teams
            3. Send information to the Search and Rescue teams in order to achieve the mission objectives
            4. Adapt strategies based on field reports given by the Search and Rescue teams"""
        )
        self.current_conditions = {}
        self.forecasts = {}


    def process_message(self, message: dict):
        try:
            # need to know who sent the message
            if "source" not in message:
                return {"error": "Message does not have a source"}

            if message["source"] == "incident_commander":
                return self._process_message_from_incident_commander(message)
            elif message["source"] == "search_team_leader":
                return self._process_message_from_search_team_leader(message)
            else:
                return {"error": "Unexpected message source"}

        except Exception as e:
            return {"error": str(e)}


    def _process_message_from_incident_commander(self, message: dict):
        ...


    def _process_message_from_search_team_leader(self, message: dict):
        ...


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
