import pytest
from sar_project.agents.operations_section_chief_agent import OperationsSectionChiefAgent
from sar_project.knowledge.knowledge_base import KnowledgeBase


# these variables are shared between classes (mainly between smaller tests and the test that creates a search plan).
# it's better to make PyTest fixtures, but I was lazy.

# LOCATION
location = "San Luis Obispo"

# TERRAIN DATA
test_elevation = 1000
test_obstacle = "a rapid stream that should be avoided"
test_obstacle_object = "stream"
terrain_data = f"The terrain is mountainous, with few passable trails. Two landslides have occurred here in the last five years. The elevation is {test_elevation} meters above sea level, and there is {test_obstacle}."

# WEATHER DATA
test_wind_speed = 30
test_temperature = 45
weather_data = f"The wind speed is {test_wind_speed}. It will be raining hard for the next two days. The temperature is {test_temperature} degrees Fahrenheit."

# AVAILABLE RESOURCES
resource1 = "drinking water"
availability1 = "high"
location1 = "Franz's house"
resource2 = "flashlights"
availability2 = "low"
location2 = "Andrew's house"
resource_status_data = f"We have {resource1} at {availability1} availability at {location1}. We also have {resource2} at {availability2} availability at {location2}."

# MISSION OBJECTIVES
obj1 = "make sure all of the search team members stay safe and are prepared for the conditions."
obj1_keyword = "safe"
obj2 = "find Bob, a 10-year-old student who went missing on a field trip to Cal Poly."
obj2_keyword = "Bob"
mission_objectives = f"First, you need to {obj1}. Your secondary objective is to {obj2}"

# SEARCH TEAMS
# team 1
t1_m1 = "Joel"
t1_m2 = "Jia"
t1_m3 = "Franz"
t1_info = f"Team 1 consists of the most experienced SAR workers. {t1_m1} works well under pressure, {t1_m2} is good at spotting clues, and {t1_m3} is a former combat medic."
# team 2
t2_m1 = "Riley"
t2_m2 = "Meyli"
t2_m3 = "Andrew"
t2_info = f"Team 2 has mixed expertise. {t2_m1} has military reconnaissance experience, {t2_m2} is a thrill-seeking rock climber, and {t2_m3} is an expert in search strategies but doesn't have field experience."
# team 3
t3_m1 = "Deja"
t3_m2 = "Peter"
t3_m3 = "Jack"
t3_info = f"The members of Team 3 all have interesting specialties. {t3_m1} has a team of search dogs, {t3_m2} is an experienced diver, and {t3_m3} flies a drone with cameras and LIDAR."
# team info
search_team_info = [t1_info, t2_info, t3_info]


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
        message = {
            "source": "incident_commander", 
            "location": location, 
            "terrain_data": terrain_data
        }
        response = agent.process_request(message)
        assert "error" not in response

        assert "knowledge_base_updated" in response and response["knowledge_base_updated"] == True

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
        message = {
            "source": "incident_commander", 
            "location": location, 
            "weather_data": weather_data
        }
        response = agent.process_request(message)
        assert "error" not in response

        assert "knowledge_base_updated" in response and response["knowledge_base_updated"] == True

        # TODO: test description?

        # identify the wind speed
        assert agent.kb.weather_data[location]["wind_speed"] == test_wind_speed

        # identify the temperature
        assert agent.kb.weather_data[location]["temperature"] == test_temperature


    def test_resource_status_data(self, agent):
        """Test whether the agent can extract information about resources from text into its knowledge base."""
        message = {
            "source": "incident_commander", 
            "location": location, 
            "resource_status": resource_status_data
        }
        response = agent.process_request(message)
        assert "error" not in response

        assert "knowledge_base_updated" in response and response["knowledge_base_updated"] == True

        # identify the availability
        assert agent.kb.resource_status[resource1]["availability"] == availability1
        assert agent.kb.resource_status[resource2]["availability"] == availability2

        # identify the location
        assert agent.kb.resource_status[resource1]["location"] == location1
        assert agent.kb.resource_status[resource2]["location"] == location2


    # TESTS FOR GETTING MISSION OBJECTIVES FROM NATURAL LANGUAGE INPUT -------------------------------------------------
    def test_mission_objectives(self, agent):
        """Tests whether the agent can identify its mission objectives."""
        message = {
            "source": "incident_commander", 
            "location": location, 
            "mission_objectives": mission_objectives, 
        }
        response = agent.process_request(message)
        assert "error" not in response

        assert "mission_objectives_understood" in response and response["mission_objectives_understood"] == True

        # identify mission objectives
        assert obj1_keyword in agent.mission_objectives[0]
        assert obj2_keyword in agent.mission_objectives[1]


    # TESTS FOR CREATING A SEARCH PLAN ---------------------------------------------------------------------------------
    def test_create_search_plan(self, agent):
        """Tests whether the agent can create a search plan. 
        Since the message doesn't provide search_team_info, it should generate a Search Plan, 
        but not divide up the plan for each Search Team Leader.
        """
        message = {
            "source": "incident_commander", 
            "location": location, 
            "mission_objectives": mission_objectives, 
            "terrain_data": terrain_data, 
            "weather_data": weather_data, 
            "resource_status": resource_status_data
        }
        response = agent.process_request(message)
        assert "error" not in response

        # the response should show that the agent processed the mission objectives and knowledge base update, and created a search plan
        assert "mission_objectives_understood" in response and response["mission_objectives_understood"] == True
        assert "knowledge_base_updated" in response and response["knowledge_base_updated"] == True
        assert "search_plan" in response

        search_plan = response["search_plan"]
        # you can use 'pytest -rP' to display this output even when the test passes
        print("test_create_search_plan() generated this search plan:\n" + search_plan)

        # check that the plan covers the mission objectives and the info from the knowledge base
        assert obj1_keyword in search_plan
        assert obj2_keyword in search_plan
        assert "terrain" in search_plan or "Terrain" in search_plan
        assert "weather" in search_plan or "Weather" in search_plan
        assert "resource" in search_plan or "Resource" in search_plan


    def test_create_search_plan_with_search_team_info(self, agent):
        """Tests whether the agent can create a search plan. 
        Since the message provides search_team_info, it should generate a Search Plan, 
        and then divide up the plan for each Search Team Leader.
        """
        message = {
            "source": "incident_commander", 
            "location": location, 
            "mission_objectives": mission_objectives, 
            "terrain_data": terrain_data, 
            "weather_data": weather_data, 
            "resource_status": resource_status_data, 
            "search_team_info": search_team_info
        }
        response = agent.process_request(message)
        assert "error" not in response

        # the response should show that the agent processed the mission objectives and knowledge base update, and created a search plan
        assert "mission_objectives_understood" in response and response["mission_objectives_understood"] == True
        assert "knowledge_base_updated" in response and response["knowledge_base_updated"] == True
        assert "search_plan" in response
        # we should also get a plan for each search team
        assert "search_team_plans" in response

        search_plan = response["search_plan"]
        search_team_plans = response["search_team_plans"]

        print("test_create_search_plan_with_search_team_info() generated this search plan:\n" + search_plan)
        for i in range(len(search_team_plans)):
            print(f"Search Team Plan {i}:")
            print(search_team_plans[i] + "\n")

        # check that the plan covers the mission objectives and the info from the knowledge base
        assert obj1_keyword in search_plan
        assert obj2_keyword in search_plan
        assert "terrain" in search_plan or "Terrain" in search_plan
        assert "weather" in search_plan or "Weather" in search_plan
        assert "resource" in search_plan or "Resource" in search_plan

        # there should be one plan for each search team
        assert type(search_team_plans) == list
        assert len(search_team_plans) == len(search_team_info)
        # TODO: search plans for each team should mention the members of the team. need to change some things to make this work because search_team_plans is not necessarily in order.
