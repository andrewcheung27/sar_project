# Example Search Plan - SAR Assignment 3

The agent takes a message with natural language strings in the `terrain_data`, `weather_data`, `resource_status`, and `mission_objectives` fields. It also gets a list of natural language strings in the `search_team_info` field, which describe each available Search Team.  
The agent generates a Search Plan. Then, it generates instructions to send to each Search Team based on the overall Search Plan.


## I. Defining the Input Strings in Python
```python
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
```


## II. Information Given to the Agent
```python
message = {  
    "source": "incident_commander",  
    "location": location,  
    "mission_objectives": mission_objectives,  
    "terrain_data": terrain_data,  
    "weather_data": weather_data,  
    "resource_status": resource_status_data,  
    "search_team_info": search_team_info  
}
```


## III. Generated Search Plan
Okay, here's a search plan draft based on the mission objectives, available teams, terrain, weather, and resources. This plan prioritizes the safety of our teams and focuses on efficiently locating Bob, given the challenging conditions.

**Search Plan: Missing Child - Bob - Cal Poly Field Trip**

**I. Mission Objectives (Restated):**

*   Ensure the safety and preparedness of all search team members.
*   Locate Bob, a missing 10-year-old student, during the field trip to Cal Poly.

**II. Incident Commander's Intent:**

*   Conduct a thorough and rapid search, prioritizing areas where a 10-year-old might wander or become stranded, given the terrain and weather conditions.
*   Maintain constant communication with all teams and adapt the search strategy as new information becomes available.
*   Account for the potential for hypothermia given the temperature and rain.
*   Take extra caution around landslide and stream areas.

**III. Safety Considerations:**

*   **Weather:**  Heavy rain, low temperature (45°F), and high wind speed (30 mph) create a high risk of hypothermia. All teams must have appropriate rain gear and be trained in recognizing and treating hypothermia.
*   **Terrain:**  Mountainous terrain with few passable trails increases the risk of slips, trips, and falls. The landslide and rapid stream pose significant hazards. Teams must exercise extreme caution in these areas.
*   **Communication:** Due to the mountainous terrain, communication may be unreliable. Establish primary and alternate communication methods (e.g., satellite phones if available, designated relay points). Regular check-ins are mandatory.

**IV. Team Assignments & Search Areas:**

Given Bob's age and the environmental conditions, we will focus our search on areas where a lost child might reasonably be found, and areas that present the greatest immediate risk.

*   **Team 1 (Experienced):**
    *   **Personnel:** Joel, Jia, Franz
    *   **Mission:** Perform a hasty search along potential trails near where the field trip was taking place and along the stream. Assess the stream’s width and depth and find a passable crossing location. Because Franz is a former combat medic, he will be responsible for providing medical aid. 
    *   **Rationale:**  Experienced team best suited for initial assessment of hazardous terrain and medical response. Jia is well-suited to search for clues while Joel can help keep the team calm under pressure.
    *   **Equipment:** First Aid Kit, rope, stream crossing gear, communication equipment, and high-visibility clothing.
    *   **Specific tasks:** Mark any findings clearly with flagging tape.

*   **Team 2 (Mixed Expertise):**
    *   **Personnel:** Riley, Meyli, Andrew
    *   **Mission:**  Search for Bob in rocky locations.
    *   **Rationale:** Meyli is a rock climber, while Riley has military reconnaissance experience. Andrew can use his expertise in search strategies to plan the search.
    *   **Equipment:** Climbing Gear, Navigation Tools, Andrew will be a safety officer, communication equipment, and high-visibility clothing.

*   **Team 3 (Specialized):**
    *   **Personnel:** Deja, Peter, Jack
    *   **Mission:**
        *   Jack will pilot the drone to search the area broadly, focusing on areas identified by Teams 1 and 2 as potential points of interest. He will prioritize areas that are difficult to access on foot, especially near the landslide zone (maintaining a safe distance).
        *   Deja and her search dogs will assist in identifying trails and spots where Bob could have passed by.
        *   Peter will be on standby to search the stream if requested.
    *   **Rationale:** Jack's drone can cover a large area quickly, and Deja's dogs can detect Bob's scent. Peter is available to search bodies of water.
    *   **Equipment:** Drone with extra batteries, dog-handling gear, diving gear, communication equipment, and high-visibility clothing.

**V. Resource Allocation:**

*   **Drinking Water:** Gather drinking water from Franz's house.
*   **Flashlights:** Gather flashlights from Andrew's house. Ensure each team has an adequate number of flashlights with extra batteries.
*   **Rain Gear:** Ensure all team members have appropriate rain gear.
*   **Navigation:** Each team must have a GPS and a paper map of the area.
*   **Communication:** Ensure reliable communication devices for all teams. Consider deploying a communication relay point if necessary.

**VI. Communication Plan:**

*   **Primary:** Radio communication on designated frequencies.
*   **Secondary:** Satellite phones (if available).
*   **Contingency:** Pre-determined rendezvous points and time intervals for physical check-ins if electronic communication fails.
*   **Reporting:** All teams will report their location and findings every hour.  Critical information (e.g., discovery of clues, changes in terrain, injuries) must be reported immediately.

**VII. Adaptation Plan:**

*   **Based on Team 1's Assessment:** If the stream is deemed impassable, adjust search areas to prioritize the near side of the stream.
*   **Based on Drone Imagery:** Jack's drone imagery will be used to identify potential search areas and hazards.
*   **Based on Dog Scent:** Deja and her dogs may be able to pinpoint a potential area for Bob to be.
*   **Missing Person Profile:** If we get more information about Bob’s personality (e.g., if he is afraid of heights, likes to climb trees, is easily frightened), we will adapt the search plan accordingly.

**VIII.  Contingency Planning:**

*   **Lost Search Team Member:**  Immediately initiate a search for the lost team member, using the remaining teams.
*   **Medical Emergency:**  Franz (Team 1) is designated as the primary medical responder.  Evacuation plan in place.
*   **Worsening Weather:**  If weather conditions significantly worsen (e.g., increased wind, flash flood warning), suspend the search and move teams to safe locations.

**IX.  Demobilization:**

*   Demobilization will be ordered by the Incident Commander when the search is completed or suspended.  All teams will be debriefed before being released.

**X. Next Steps:**

1.  Brief all teams on the search plan.
2.  Gather resources (water, flashlights) and distribute them to teams.
3.  Establish communication protocols.
4.  Deploy teams to their assigned search areas.
5.  Continuously monitor weather conditions and adjust the plan as needed.
6.  Follow the mission objectives.

This is a draft plan and will be adapted based on the Incident Commander's guidance, and real-time field reports. The safety of our teams remains the top priority.



## IV. Generated Plans to Send to Each Search Team

### Search Team Plan 1:
**Search Plan: Missing Child - Bob - Cal Poly Field Trip - Team 1**

**I. Mission Objectives:** Locate Bob, a missing 10-year-old student, during the field trip to Cal Poly. Ensure the safety and preparedness of all search team members.

**II. Incident Commander's Intent:** Conduct a thorough and rapid search, prioritizing areas where a 10-year-old might wander or become stranded, given the terrain and weather conditions. Maintain constant communication with all teams and adapt the search strategy as new information becomes available. Account for the potential for hypothermia given the temperature and rain. Take extra caution around landslide and stream areas.

**III. Safety Considerations:** Weather: Heavy rain, low temperature (45°F), and high wind speed (30 mph) create a high risk of hypothermia. All teams must have appropriate rain gear and be trained in recognizing and treating hypothermia. Terrain: Mountainous terrain with few passable trails increases the risk of slips, trips, and falls. The landslide and rapid stream pose significant hazards. Teams must exercise extreme caution in these areas. Communication: Due to the mountainous terrain, communication may be unreliable. Establish primary and alternate communication methods (e.g., satellite phones if available, designated relay points). Regular check-ins are mandatory.

**IV. Team Assignment & Search Area:**
*   **Team 1 (Experienced):**
    *   **Personnel:** Joel, Jia, Franz
    *   **Mission:** Perform a hasty search along potential trails near where the field trip was taking place and along the stream. Assess the stream’s width and depth and find a passable crossing location. Because Franz is a former combat medic, he will be responsible for providing medical aid. 
    *   **Rationale:** Experienced team best suited for initial assessment of hazardous terrain and medical response. Jia is well-suited to search for clues while Joel can help keep the team calm under pressure.
    *   **Equipment:** First Aid Kit, rope, stream crossing gear, communication equipment, and high-visibility clothing.
    *   **Specific tasks:** Mark any findings clearly with flagging tape.

**V. Communication Plan:** Primary: Radio communication on designated frequencies. Secondary: Satellite phones (if available). Contingency: Pre-determined rendezvous points and time intervals for physical check-ins if electronic communication fails. Reporting: Report your location and findings every hour. Critical information (e.g., discovery of clues, changes in terrain, injuries) must be reported immediately.

**VI. Adaptation Plan:**
*   If the stream is deemed impassable, adjust search areas to prioritize the near side of the stream.

**VII. Contingency Planning:**
*   **Medical Emergency:**  Franz (Team 1) is designated as the primary medical responder.  Evacuation plan in place.

**VIII. Next Steps:**
1.  Brief all team members on the search plan.
2.  Gather resources (water, flashlights) and distribute them to team members.
3.  Establish communication protocols.
4.  Deploy to assigned search area.
5.  Continuously monitor weather conditions and adjust the plan as needed.
6.  Follow the mission objectives.

This is a draft plan and will be adapted based on the Incident Commander's guidance, and real-time field reports. The safety of our teams remains the top priority.

### Search Team Plan 2:
**Search Plan: Missing Child - Bob - Cal Poly Field Trip - Team 2**

**I. Mission Objectives:** Locate Bob, a missing 10-year-old student, during the field trip to Cal Poly. Ensure the safety and preparedness of all search team members.

**II. Incident Commander's Intent:** Conduct a thorough and rapid search, prioritizing areas where a 10-year-old might wander or become stranded, given the terrain and weather conditions. Maintain constant communication with all teams and adapt the search strategy as new information becomes available. Account for the potential for hypothermia given the temperature and rain. Take extra caution around landslide and stream areas.

**III. Safety Considerations:** Weather: Heavy rain, low temperature (45°F), and high wind speed (30 mph) create a high risk of hypothermia. All teams must have appropriate rain gear and be trained in recognizing and treating hypothermia. Terrain: Mountainous terrain with few passable trails increases the risk of slips, trips, and falls. The landslide and rapid stream pose significant hazards. Teams must exercise extreme caution in these areas. Communication: Due to the mountainous terrain, communication may be unreliable. Establish primary and alternate communication methods (e.g., satellite phones if available, designated relay points). Regular check-ins are mandatory.

**IV. Team Assignment & Search Area:**
*   **Team 2 (Mixed Expertise):**
    *   **Personnel:** Riley, Meyli, Andrew
    *   **Mission:**  Search for Bob in rocky locations.
    *   **Rationale:** Meyli is a rock climber, while Riley has military reconnaissance experience. Andrew can use his expertise in search strategies to plan the search.
    *   **Equipment:** Climbing Gear, Navigation Tools, Andrew will be a safety officer, communication equipment, and high-visibility clothing.

**V. Communication Plan:** Primary: Radio communication on designated frequencies. Secondary: Satellite phones (if available). Contingency: Pre-determined rendezvous points and time intervals for physical check-ins if electronic communication fails. Reporting: Report your location and findings every hour. Critical information (e.g., discovery of clues, changes in terrain, injuries) must be reported immediately.

**VI. Next Steps:**
1.  Brief all team members on the search plan.
2.  Gather resources (water, flashlights) and distribute them to team members.
3.  Establish communication protocols.
4.  Deploy to assigned search area.
5.  Continuously monitor weather conditions and adjust the plan as needed.
6.  Follow the mission objectives.

This is a draft plan and will be adapted based on the Incident Commander's guidance, and real-time field reports. The safety of our teams remains the top priority.

### Search Team Plan 3:
**Search Plan: Missing Child - Bob - Cal Poly Field Trip - Team 3**

**I. Mission Objectives:** Locate Bob, a missing 10-year-old student, during the field trip to Cal Poly. Ensure the safety and preparedness of all search team members.

**II. Incident Commander's Intent:** Conduct a thorough and rapid search, prioritizing areas where a 10-year-old might wander or become stranded, given the terrain and weather conditions. Maintain constant communication with all teams and adapt the search strategy as new information becomes available. Account for the potential for hypothermia given the temperature and rain. Take extra caution around landslide and stream areas.

**III. Safety Considerations:** Weather: Heavy rain, low temperature (45°F), and high wind speed (30 mph) create a high risk of hypothermia. All teams must have appropriate rain gear and be trained in recognizing and treating hypothermia. Terrain: Mountainous terrain with few passable trails increases the risk of slips, trips, and falls. The landslide and rapid stream pose significant hazards. Teams must exercise extreme caution in these areas. Communication: Due to the mountainous terrain, communication may be unreliable. Establish primary and alternate communication methods (e.g., satellite phones if available, designated relay points). Regular check-ins are mandatory.

**IV. Team Assignment & Search Area:**
*   **Team 3 (Specialized):**
    *   **Personnel:** Deja, Peter, Jack
    *   **Mission:**
        *   Jack will pilot the drone to search the area broadly, focusing on areas identified by Teams 1 and 2 as potential points of interest. He will prioritize areas that are difficult to access on foot, especially near the landslide zone (maintaining a safe distance).
        *   Deja and her search dogs will assist in identifying trails and spots where Bob could have passed by.
        *   Peter will be on standby to search the stream if requested.
    *   **Rationale:** Jack's drone can cover a large area quickly, and Deja's dogs can detect Bob's scent. Peter is available to search bodies of water.
    *   **Equipment:** Drone with extra batteries, dog-handling gear, diving gear, communication equipment, and high-visibility clothing.

**V. Communication Plan:** Primary: Radio communication on designated frequencies. Secondary: Satellite phones (if available). Contingency: Pre-determined rendezvous points and time intervals for physical check-ins if electronic communication fails. Reporting: Report your location and findings every hour. Critical information (e.g., discovery of clues, changes in terrain, injuries) must be reported immediately.

**VI. Adaptation Plan:**
*   **Based on Drone Imagery:** Jack's drone imagery will be used to identify potential search areas and hazards.
*   **Based on Dog Scent:** Deja and her dogs may be able to pinpoint a potential area for Bob to be.

**VII. Next Steps:**
1.  Brief all team members on the search plan.
2.  Gather resources (water, flashlights) and distribute them to team members.
3.  Establish communication protocols.
4.  Deploy to assigned search area.
5.  Continuously monitor weather conditions and adjust the plan as needed.
6.  Follow the mission objectives.

This is a draft plan and will be adapted based on the Incident Commander's guidance, and real-time field reports. The safety of our teams remains the top priority.
