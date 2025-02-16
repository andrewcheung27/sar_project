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


    def test_status_update(self, agent):
        response = agent.update_status("active")
        assert response["new_status"] == "active"
        assert agent.get_status() == "active"


    # TESTS FOR UPDATING KNOWLEDGE BASE WITH NATURAL LANGUAGE INPUT ----------------------------------------------------
    def test_terrain_data(self, agent):
        """Test whether the agent can extract terrain information from text into its knowledge base."""
        location = "San Luis Obispo"
        test_elevation = 1000
        test_obstacle = "a rapid stream that should be avoided"
        test_obstacle_object = "stream"
        terrain_data = f"The terrain is mountainous, with few passable trails. Two landslides have occurred here in the last five years. The elevation is {test_elevation} meters above sea level, and there is {test_obstacle}."

        message = {
            "source": "incident_commander", 
            "location": location, 
            "terrain_data": terrain_data
        }

        response = agent.process_request(message)
        assert response["knowledge_base_updated"] == True

        # TODO: test description?

        # identify the elevation
        assert agent.kb.terrain_data[location]["elevation"] == test_elevation

        # identify the obstacle
        test_obstacle_found = False
        for ob in agent.kb.terrain_data[location]["obstacles"]:
            if test_obstacle_object in ob:
                test_obstacle_found = True
        assert test_obstacle_found


    def test_weather_data(self, agent):
        """Test whether the agent can extract weather information from text into its knowledge base."""
        location = "San Luis Obispo"
        test_wind_speed = 30
        test_temperature = 45
        weather_data = f"The wind speed is {test_wind_speed}. It will be raining hard for the next two days. The temperature is {test_temperature} degrees Fahrenheit."

        message = {
            "source": "incident_commander", 
            "location": location, 
            "weather_data": weather_data
        }

        response = agent.process_request(message)
        assert response["knowledge_base_updated"] == True

        # TODO: test description?

        # identify the wind speed
        assert agent.kb.weather_data[location]["wind_speed"] == test_wind_speed

        # identify the temperature
        assert agent.kb.weather_data[location]["temperature"] == test_temperature


    def test_resource_status_data(self, agent):
        """Test whether the agent can extract information about resources from text into its knowledge base."""
        location = "San Luis Obispo"
        # first element in array of resources
        resource1 = "drinking water"
        availability1 = "80%"
        location1 = "Franz's house"
        # second element
        resource2 = "flashlights"
        availability2 = "low"
        location2 = "Andrew's house"
        resource_status_data = f"We have {resource1} at {availability1} availability at {location1}. We also have {resource2} at {availability2} availability at {location2}."

        message = {
            "source": "incident_commander", 
            "location": location, 
            "resource_status": resource_status_data
        }

        response = agent.process_request(message)
        assert response["knowledge_base_updated"] == True

        # identify the availability
        assert agent.kb.resource_status[resource1]["availability"] == availability1
        assert agent.kb.resource_status[resource2]["availability"] == availability2

        # identify the location
        assert agent.kb.resource_status[resource1]["location"] == location1
        assert agent.kb.resource_status[resource2]["location"] == location2


    # def test_process_message_from_incident_commander_mission_objectives(self, agent):
    #     location = "San Luis Obispo"
    #     mission_objectives = ["Make sure the ground pounders are safe during their search.", 
    #                           "Find Bob, a 10-year-old student who went missing on a field trip to Cal Poly."]

    #     message = {
    #         "source": "incident_commander", 
    #         "location": location, 
    #         "mission_objectives": mission_objectives, 
    #     }
    #     response = agent.process_request(message)

    #     # response should say that it understands the mission objectives
    #     assert "mission_objectives_understood" in response and response["mission_objectives_understood"] == True

    #     # mission objectives should be saved
    #     assert agent.mission_objectives == mission_objectives
