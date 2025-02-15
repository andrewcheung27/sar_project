from sar_project.agents.base_agent import SARBaseAgent


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

    def process_message(self, message):
        pass

    def update_status(self, status):
        """Update the agent's status"""
        self.status = status
        return {"status": "updated", "new_status": status}

    def get_status(self):
        """Get the agent's current status"""
        return getattr(self, "status", "unknown")
