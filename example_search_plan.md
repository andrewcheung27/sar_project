# Example Search Plan - SAR Assignment 1

The agent takes a message with natural language strings in the `terrain_data`, `weather_data`, `resource_status`, and `mission_objectives` fields. Then, it generates a search plan.


## I. Defining the Input Strings in Python
location = "San Luis Obispo"

test_elevation = 1000
test_obstacle = "a rapid stream that should be avoided"
test_obstacle_object = "stream"
terrain_data = f"The terrain is mountainous, with few passable trails. Two landslides have occurred here in the last five years. The elevation is {test_elevation} meters above sea level, and there is {test_obstacle}."

test_wind_speed = 30
test_temperature = 45
weather_data = f"The wind speed is {test_wind_speed}. It will be raining hard for the next two days. The temperature is {test_temperature} degrees Fahrenheit."

resource1 = "drinking water"
availability1 = "80%"
location1 = "Franz's house"
resource2 = "flashlights"
availability2 = "low"
location2 = "Andrew's house"
resource_status_data = f"We have {resource1} at {availability1} availability at {location1}. We also have {resource2} at {availability2} availability at {location2}."

obj1 = "make sure all of the search team members stay safe and are prepared for the conditions."
obj1_keyword = "safe"
obj2 = "find Bob, a 10-year-old student who went missing on a field trip to Cal Poly."
obj2_keyword = "Bob"
mission_objectives = f"First, you need to {obj1}. Your secondary objective is to {obj2}"


## II. Information Given to the Agent
message = {  
    "source": "incident_commander",  
    "location": location,  
    "mission_objectives": mission_objectives,  
    "terrain_data": terrain_data,  
    "weather_data": weather_data,  
    "resource_status": resource_status_data  
}


## III. Generated Search Plan
SEARCH PLAN:
Okay, here's a preliminary search plan, taking into account the mission objectives, terrain, weather, and available resources. This plan will need to be flexible and adjusted based on field reports.

**Incident Action Plan – Search and Rescue Operation for Missing Child "Bob"**

**I.  Situation Overview**

*   **Missing Person:** Bob, 10 years old.
*   **Location:** San Luis Obispo Area.
*   **Terrain:** Mountainous, few passable trails. Known hazards include two past landslide areas and a rapid stream.
*   **Weather:** Heavy rain expected for the next two days. Temperature: 45°F. Wind Speed: 30 mph.
*   **Resources:** 80% drinking water availability (Franz's house), low availability of flashlights (Andrew's house).
*   **Mission Objectives:**
    1.  Ensure safety and preparedness of all search team members.
    2.  Locate Bob, a missing 10-year-old student.

**II. Safety Considerations**

*   **Primary Hazard:**  Weather (hypothermia risk due to rain and cold), dangerous terrain (landslide areas, rapid stream), low visibility.
*   **Mitigation:**
    *   **Weather:** All teams must be equipped with appropriate rain gear (waterproof jackets, pants, hats), thermal layers, and a change of dry clothes if possible.  Monitor weather conditions frequently and adjust plans accordingly. Emphasize recognizing signs of hypothermia (shivering, confusion, slurred speech) in themselves and others.
    *   **Terrain:**  Avoid landslide areas entirely. If unavoidable, maintain a wide safety margin and utilize ropes for support on steep or slippery sections. The rapid stream is strictly off-limits for crossing unless absolutely necessary and with appropriate safety equipment and trained personnel.
    *   **Visibility:** With limited flashlights, prioritize high-visibility clothing for all team members. Plan search sectors to maximize daylight hours.
    *   **Communication:** Ensure all teams have reliable communication (radios) and a clear communication plan. Establish check-in procedures at regular intervals.
    *   **Medical:** Each team will have a designated person trained in basic first aid and equipped with a first-aid kit including items to treat hypothermia (warm packs, blankets).
    *   **Team Awareness:** Encourage open communication among team members regarding fatigue, concerns, and potential hazards.

**III. Search Strategy & Tactics**

**A.  Initial Search Area Prioritization:**

Given the limited information and Bob's age, we will initially prioritize areas where a lost child is most likely to be found:

1.  **"Lost-Proofing" principle:** Within a 1-2 mile radius of Bob's last known location if available, and focus on any roads, tracks or pathways running from that location.
2.  **Near the Stream:** Streams and rivers can be natural hazards and children sometimes end up nearby.
3.  **Areas of Refuge:**  Look for areas that provide shelter from the rain and wind (e.g., overhanging rocks, dense vegetation, abandoned structures).
4.  **Landslide Zone Edges:** While avoiding the immediate landslide zones, search the *edges* of these areas, as Bob may have been trying to navigate around them and become disoriented.

**B. Search Teams & Assignments:**

*   **Team Structure:**  Organize search teams into groups of 2-4 individuals for safety and efficiency.
*   **Assignments:** (The following assumes we have sufficient personnel. If not, we will need to combine sectors or prioritize based on likelihood of success).

    *   **Team 1 (Stream Search):**  Thoroughly search both sides of the stream. *Safety is paramount!*  Maintain visual contact with each other at all times. Do NOT attempt to cross.  Document any tracks or signs found near the stream. GPS track their route.
    *   **Team 2 (Landslide Zone Edge – West):**  Search the west edge of the landslide zone. Maintain a safe distance from the unstable areas. Mark all trails and potential hazards on their GPS.
    *   **Team 3 (Landslide Zone Edge – East):** Search the east edge of the landslide zone. Maintain a safe distance from the unstable areas. Mark all trails and potential hazards on their GPS.
    *   **Team 4 (Refuge Search):** Search any areas of refuge within the 1-2 mile radius that are not near a landslide or stream. This should include caves or thickets of trees.

**C. Search Techniques:**

*   **Linear Search:** Teams will utilize linear search techniques within their assigned sectors, maintaining close proximity and clear communication.
*   **Hasty Search:** If there are credible leads (e.g., footprints, reported sightings), deploy a small, fast-moving team to investigate.
*   **Shouting:** Teams should periodically shout Bob's name and listen for a response.

**IV. Communications**

*   **Radio Frequencies:** [Specify frequencies]
*   **Check-in Schedule:**  Teams will check in with the Operations Section Chief every hour on the hour.
*   **Emergency Signals:** [Specify emergency signals, e.g., three whistle blasts repeated].
*   **Reporting:** Teams will report any findings (tracks, signs, potential leads) immediately to the Operations Section Chief.

**V. Resource Management**

*   **Water Distribution:** Teams will collect water from Franz's house *before* deploying to the field.  Strict water rationing will be enforced.
*   **Flashlight Allocation:** Due to low availability, flashlights will be prioritized for teams working near the stream and for potential nighttime operations. Each team will have at least one.
*   **Additional Supplies:**  If possible, acquire additional flashlights, batteries, and warm clothing from local sources.

**VI. Contingency Planning**

*   **Lost Team:** If a team becomes lost, the highest priority is their safe recovery. Implement lost person procedures immediately.
*   **Medical Emergency:** Have a plan for rapid evacuation of injured personnel.
*   **Weather Deterioration:** If weather conditions worsen significantly, consider suspending search operations until conditions improve.
*   **Search Fatigue:** Implement mandatory rest periods for all teams to prevent fatigue and maintain safety.

**VII.  Information Dissemination**

*   All team leads will be briefed on this plan.
*   Teams will be provided with maps of their assigned search sectors.
*   Teams will be equipped with GPS devices to track their routes and mark any findings.

**VIII.  Next Steps**

1.  **Briefing:** Conduct a comprehensive briefing for all search team members on the Incident Action Plan, safety protocols, and search assignments.
2.  **Resource Gathering:** Ensure all necessary resources (water, flashlights, first aid kits, radios) are collected and distributed to the teams.
3.  **Deployment:** Deploy search teams to their assigned sectors.
4.  **Monitoring & Adaptation:** Continuously monitor weather conditions, team progress, and field reports. Be prepared to adapt the search plan as needed.

**IX.  Operations Section Chief Contact Information:**

[Your Name/Contact Information]

This plan is a starting point and will be adjusted based on incoming information.  The safety of the search teams is always the top priority. Good luck, and stay safe.
