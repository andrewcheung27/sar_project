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
Okay, here's a search plan I've developed, considering the mission objectives, available teams, terrain, weather, and resources:

**Incident Action Plan – Operations Section: Search and Rescue**

**I. Mission Objectives:**

*   Ensure the safety and preparedness of all search team members.
*   Locate Bob, a missing 10-year-old student.

**II. Situation Assessment:**

*   **Missing Person:** Bob, 10 years old.
*   **Location:** San Luis Obispo, mountainous terrain with few passable trails.
*   **Terrain Hazards:** Two landslides in the past five years, rapid stream.
*   **Weather:** Heavy rain for the next two days, temperature 45°F, wind speed 30 mph. This poses a significant risk of hypothermia.
*   **Resource Constraints:** Low availability of flashlights.

**III. Operational Period:**

*   Immediately and for the next 24 hours. Re-evaluate and adjust the plan at that time.

**IV. Search Strategy:**

Given Bob's age, the mountainous terrain, inclement weather, and terrain hazards, the strategy will focus on the following:

*   **Prioritize likely escape routes and areas where a child might seek shelter.** This includes areas near trails, natural shelters (caves, overhangs), and potentially lower elevations due to the cold and wind.
*   **Utilize the strengths of each team to maximize coverage and effectiveness while mitigating risks.**
*   **Maintain constant communication and monitoring of team safety.**

**V. Task Assignments:**

*   **General Safety Instructions for All Teams:**
    *   Strict adherence to the buddy system.
    *   Constant communication with Operations Section (me) via radio.
    *   Monitor for signs of hypothermia in themselves and others. Carry extra layers.
    *   Avoid the rapid stream at all costs.
    *   Be aware of the potential for landslides, especially given the heavy rain.
    *   Document all findings (clues, observations) with photos and detailed notes.
    *   If Bob is found, immediately provide first aid, establish communications, and await extraction.
*   **Team 1 (Joel, Jia, Franz):**
    *   **Task:** Primary ground search team focusing on areas closest to the last known location of Bob.
    *   **Rationale:** Experience is crucial in these conditions. Franz's medical expertise is highly valuable. Jia's clue-spotting abilities are beneficial for locating tracks or items belonging to Bob.
    *   **Specific Area:** Focus on the most accessible trails closest to the suspected point of departure. Start search pattern at the trailhead and expand outwards.
    *   **Equipment:** Full medical kit (carried by Franz), extra warm layers for all members, map and compass.
    *   **Contingency:** Prepare for possible emergency medical situation.
*   **Team 2 (Riley, Meyli, Andrew):**
    *   **Task:** Secondary search team, focusing on more difficult and dangerous terrain.
    *   **Rationale:** Riley's reconnaissance experience will be beneficial for navigation. Meyli's rock climbing experience makes her suitable for traversing challenging terrain. Andrew will remain at base and help guide the other team members through communications.
    *   **Specific Area:** Focus on higher elevations and areas off the main trails where Bob might have wandered.
    *   **Equipment:** Ropes and climbing gear (for Meyli), map and compass, and cold weather gear.
    *   **Contingency:** Use caution when crossing streams or traversing steep slopes. Report back to base for all hazards encountered.
*   **Team 3 (Deja, Peter, Jack):**
    *   **Task:** Support and reconnaissance.
    *   **Rationale:** Deja's dogs can cover large areas quickly and locate Bob by scent. Jack's drone can provide an aerial view of the search area, and Peter can search water.
    *   **Specific Area:** Drone reconnaissance of the overall search area to identify potential areas of interest or hazards. Coordinate with ground teams to deploy dogs to specific areas identified by drone. Peter will be on standby for water rescue, if necessary.
    *   **Equipment:** Drone with spare batteries (Jack), dog search equipment (Deja), and diving gear for Peter.
    *   **Contingency:** Be wary of low visibility due to rain and fog. Be aware of the potential for drone crashes.

**VI. Resource Management:**

*   **Water:** Ensure all teams have sufficient drinking water. Refill from Franz's house if needed before deployment.
*   **Flashlights:** Due to limited availability, prioritize flashlights for Team 1 and strategic placement along trails. Get flashlights from Andrew's house immediately.

**VII. Communications:**

*   All teams will maintain radio contact with the Operations Section Chief.
*   Report all findings, changes in conditions, and safety concerns immediately.
*   Establish a pre-determined communication schedule for regular check-ins.

**VIII. Risk Management:**

*   **Hypothermia:** High risk due to weather. Emphasis on warm clothing, monitoring for symptoms, and rapid evacuation if necessary.
*   **Landslides:** Monitor for unstable slopes. Avoid areas with recent slide activity.
*   **Rapid Stream:** Avoid crossing the stream.
*   **Injuries:** Be prepared for potential injuries due to falls, slips, and exposure. Full medical kit with Team 1.

**IX. Demobilization:**

*   Demobilization will be determined by the Incident Commander based on search progress and the likelihood of finding Bob.

**X. Contingency Planning:**

*   **If Bob is not found within the first 12 hours:** Re-evaluate the search area and adjust the strategy based on gathered information. Consider expanding the search area and requesting additional resources.
*   **If weather conditions worsen:** Suspend the search if conditions become too dangerous.
*   **If a team member is injured:** Immediately provide first aid and evacuate the injured person.

**XI. Briefing:**

*   All team leaders will be briefed on this plan before deployment.
*   Ensure all team members understand their assignments, safety procedures, and communication protocols.



## IV. Generated Plans to Send to Each Search Team

### A. Search Team Plan 0
**Team 1 (Joel, Jia, Franz):**
*   **Task:** Primary ground search team focusing on areas closest to the last known location of Bob.
*   **Rationale:** Experience is crucial in these conditions. Franz's medical expertise is highly valuable. Jia's clue-spotting abilities are beneficial for locating tracks or items belonging to Bob.
*   **Specific Area:** Focus on the most accessible trails closest to the suspected point of departure. Start search pattern at the trailhead and expand outwards.
*   **Equipment:** Full medical kit (carried by Franz), extra warm layers for all members, map and compass.
*   **Contingency:** Prepare for possible emergency medical situation.

**General Safety Instructions for All Teams:**
*   Strict adherence to the buddy system.
*   Constant communication with Operations Section (me) via radio.
*   Monitor for signs of hypothermia in themselves and others. Carry extra layers.
*   Avoid the rapid stream at all costs.
*   Be aware of the potential for landslides, especially given the heavy rain.
*   Document all findings (clues, observations) with photos and detailed notes.
*   If Bob is found, immediately provide first aid, establish communications, and await extraction.

**Water:** Ensure all teams have sufficient drinking water. Refill from Franz's house if needed before deployment.
*   **Flashlights:** Due to limited availability, prioritize flashlights for Team 1 and strategic placement along trails. Get flashlights from Andrew's house immediately.

### B. Search Team Plan 1
**Team 2 (Riley, Meyli, Andrew):**
*   **Task:** Secondary search team, focusing on more difficult and dangerous terrain.
*   **Rationale:** Riley's reconnaissance experience will be beneficial for navigation. Meyli's rock climbing experience makes her suitable for traversing challenging terrain. Andrew will remain at base and help guide the other team members through communications.
*   **Specific Area:** Focus on higher elevations and areas off the main trails where Bob might have wandered.
*   **Equipment:** Ropes and climbing gear (for Meyli), map and compass, and cold weather gear.
*   **Contingency:** Use caution when crossing streams or traversing steep slopes. Report back to base for all hazards encountered.

**General Safety Instructions for All Teams:**
*   Strict adherence to the buddy system.
*   Constant communication with Operations Section (me) via radio.
*   Monitor for signs of hypothermia in themselves and others. Carry extra layers.
*   Avoid the rapid stream at all costs.
*   Be aware of the potential for landslides, especially given the heavy rain.
*   Document all findings (clues, observations) with photos and detailed notes.
*   If Bob is found, immediately provide first aid, establish communications, and await extraction.

### C. Search Team Plan 2
**Team 3 (Deja, Peter, Jack):**
*   **Task:** Support and reconnaissance.
*   **Rationale:** Deja's dogs can cover large areas quickly and locate Bob by scent. Jack's drone can provide an aerial view of the search area, and Peter can search water.
*   **Specific Area:** Drone reconnaissance of the overall search area to identify potential areas of interest or hazards. Coordinate with ground teams to deploy dogs to specific areas identified by drone. Peter will be on standby for water rescue, if necessary.
*   **Equipment:** Drone with spare batteries (Jack), dog search equipment (Deja), and diving gear for Peter.
*   **Contingency:** Be wary of low visibility due to rain and fog. Be aware of the potential for drone crashes.

**General Safety Instructions for All Teams:**
*   Strict adherence to the buddy system.
*   Constant communication with Operations Section (me) via radio.
*   Monitor for signs of hypothermia in themselves and others. Carry extra layers.
*   Avoid the rapid stream at all costs.
*   Be aware of the potential for landslides, especially given the heavy rain.
*   Document all findings (clues, observations) with photos and detailed notes.
*   If Bob is found, immediately provide first aid, establish communications, and await extraction.
