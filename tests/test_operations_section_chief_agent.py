import pytest
from sar_project.agents.operations_section_chief_agent import OperationsSectionChiefAgent


class TestOperationsSectionChiefAgent:
    @pytest.fixture
    def agent(self):
        return OperationsSectionChiefAgent()
    
    def test_initialization(self, agent):
        assert agent.name == "operations_section_chief"
        assert agent.role == "Operations Section Chief"
        assert agent.mission_status == "standby"

    def test_process_request(self, agent):
        # TODO
        pass

    def test_status_update(self, agent):
        response = agent.update_status("active")
        assert response["new_status"] == "active"
        assert agent.get_status() == "active"