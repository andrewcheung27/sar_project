import pytest
from sar_project.agents.operations_section_chief_agent import OperationsSectionChiefAgent
from sar_project.knowledge.knowledge_base import KnowledgeBase


class TestOperationsSectionChiefAgent:
    @pytest.fixture
    def agent(self):
        kb = KnowledgeBase()
        return OperationsSectionChiefAgent(knowledge_base=kb)


    def test_initialization(self, agent):
        assert agent.name == "operations_section_chief"
        assert agent.role == "Operations Section Chief"
        assert agent.mission_status == "standby"


    def test_process_message_from_incident_commander_mission_objectives(self, agent):
        location = "San Luis Obispo"
        mission_objectives = ["Make sure the ground pounders are safe during their search.", 
                              "Find Bob, a 10-year-old student who went missing on a field trip to Cal Poly."]

        message = {
            "source": "incident_commander", 
            "location": location, 
            "mission_objectives": mission_objectives, 
        }
        response = agent.process_request(message)

        # response should say that it understands the mission objectives
        assert "mission_objectives_understood" in response and response["mission_objectives_understood"] == True

        # mission objectives should be saved
        assert agent.mission_objectives == mission_objectives


    def test_process_message_from_incident_commander_kb(self, agent):
        location = "San Luis Obispo"
        # terrain_data = {location: {"elevation": 1000, "slope": 20}}
        # weather_data = {location: {"temperature": 90, "wind_speed": 15}}
        terrain_data = {"elevation": 1000, "slope": 20}
        weather_data = {"temperature": 90, "wind_speed": 15}
        test_resource = "drinking_water"
        test_resource_status = {"availability": 80, "location": "Franz's House"}
        resources = {test_resource: test_resource_status}

        message = {
            "source": "incident_commander", 
            "location": location, 
            "terrain_data": terrain_data, 
            "weather_data": weather_data, 
            "resources": resources
        }
        response = agent.process_request(message)

        # response should say something about knowledge base being updated
        assert "knowledge_base_updated" in response and response["knowledge_base_updated"] == True
        # knowledge base should be updated
        assert agent.kb.terrain_data[location] == terrain_data
        assert agent.kb.weather_data[location] == weather_data
        assert agent.kb.resource_status[test_resource] == test_resource_status


    def test_status_update(self, agent):
        response = agent.update_status("active")
        assert response["new_status"] == "active"
        assert agent.get_status() == "active"
