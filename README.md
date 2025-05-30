# Operations Section Chief Agent

Author: Andrew Cheung

This agent was developed for the <i>AI for Search and Rescue Project</i>, as a part of Franz Kurfess's Computer Support for Knowledge Management class at Cal Poly SLO. 

The code is located in `src/sar_project/agents/operations_section_chief_agent.py`, and the tests are in `tests/test_operations_section_chief_agent.py`. You can run the tests with `pytest -rP` to have the search plan printed to stdout.

You can view an example Search Plan in `example_search_plan_with_search_team_info_and_unknowns.md`.


The source code is available at: https://github.com/andrewcheung27/sar_project.


## Description
The Operations Section Chief Agent receives mission objectives, Search Team information, and knowledge base information from the Incident Commander, which are all given as natural language strings. Then, it uses the information to generate a Search Plan, and also generates a plan for each team based on the Search Plan.

Notes about the agent:
* The agent's `process_request()` method takes `message` as a parameter, which must be a dictionary. It requires a `source` key in the dictionary, which must be either `incident_commander` or `search_team_leader`. 
* Other supported keys in the `message` dictionary are: `location` (required for incident_commander messages), `terrain_data`, `weather_data`, `resource_status`, `mission_objectives`, and `search_team_info`.
* The `terrain_data`, `weather_data`, `resource_status`, and `mission_objectives` values in the `message` dictionary should be natural language strings. The `search_team_info` value should be a list of natural language strings, one for each Search Team. The agent uses Google Gemini's Structured Output feature to convert the values into JSON, which is parsed and put into the knowledge base.
* The `process_request()` method returns a dictionary, whose keys may include: `knowledge_base_updated` (a boolean), `mission_objectives_understood` (a boolean), `search_plan` (a string describing the agent's search plan), and `search_team_plans` (a list of strings describing the plan for each team)


## Setup
1. Clone this forked repository.

2. Set up a Python environment with version `3.10.0`.

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```

Pip might have dependency resolver issues from requirements.txt. The fix is install the necessary packages explicitly with pip:
```bash
# for example...
pip install httplib2
```

4. Configure environment variables in your `.env` file:
```
GOOGLE_API_KEY=<your_google_api_key_here>
DEPLOYMENT_NAME=SAR_Project
```


## Assignment 3 - SAR Agent Modifications

### Insights
Thanks to Joel for his [review](https://docs.google.com/document/d/1yJgItLgLgjiecpSirkEly4WZWvC2wCDs7TKbi6q7Dq0/edit?tab=t.0) of this agent! He gave positive feedback about how I represented knowledge: giving multiple dictionaries as input to represent different knowledge domains, and writing schemas to get structured output from the LLM. This aligns with my original intention of taking natural language input for each domain (terrain, weather, etc.) and adding it to the knowledge base to use as context for generating the Search Plan. When Joel ran the agent with his own Search and Rescue scenario, he identified some improvements I could make to the functionality of the agent. The generated plan was reasonable and it accounted for all of the information given to the agent. However, the `test_terrain_data()` test failed to identify the forest as the obstacle, demonstrating the limitations of the agent due to its reliance on an LLM. The Search Plan still involved the forest, probably because it was in the mission objectives, but the agent could have missed important information about the situation if the obstacle was something different. To improve the agent, Joel recommended that I should find a way to deal with missing information, such as changing the prompts to account for it. I didn't think about this too much because the LLM passed the tests when I ran it, so this was valuable feedback. In addition, he suggested adding the ability to take in information about the available Search Teams, and to send Search Plan documents to team leaders. This is something I wrote comments about in Assignment 1, but I didn't have time to implement it. It's an important modification to improve the agent's integration into the SAR framework. Finally, Joel suggested adding the capability to update the Search Plan with new information. This seems like a logical next step once the plan has been created because the incident commander will likely send updates during the operation.

### Modifications
I was able to address the two most important suggestions from Joel: using information about the Search Teams and handling unknown information. I thought it was most important to use information about the Search Teams because they are the most important resource for the SAR operation and the plan should be based on what they can do. So, I implemented this feature by adding a `search_team_info` field to the message from the incident commander, which must be a list of strings describing each team. I made the `_split_search_plan()` method to generate a list of sub-plans for each team based on the overall Search Plan. The sub-plans can be sent to each Search Team Leader based on their `search_team_number`. I couldn't find an example of sending a message to another agent in the existing SAR framework, so I left the `_send_plan_to_search_team_leader()` function blank, but the implementation can be easily inserted in the future. I tested this functionality in `test_create_search_plan_with_search_team_info()`, giving a short description of the 3 teams of 3 members. I asked ChatGPT to generate SAR teams for a story, and adapted its descriptions of a team of SAR veterans, a team with mixed expertise, and a team with unorthodox skills. The agent successfully generated a Search Plan involving all of the teams and their members, and also generated a plan for each team. You can view an example in `example_search_plan_with_search_team_info.md`.  

Secondly, I added an `unknown_information` field to the schemas for terrain and weather, and included a sentence in the prompt telling the LLM to describe unknown information. I wanted to do something simple, while still encouraging the LLM to say that it doesn't know something instead of hallucinating. I tested this with `test_terrain_data_unknown` and `test_weather_data_unknown`, where I gave vague information and checked the unknown information. This worked well---one example output was "Unknown elevation and specific obstacles." for terrain and "Specific details about the inclement weather (type of weather, duration, intensity) are unknown, including temperature and wind speed. Placeholders are used for temperature and windspeed." for weather. This information would be part of the context for plan generation. Finally, I ran the `test_create_search_plan_with_search_team_info()` test again, this time with the `unknown_information` field. The output can be found in `example_search_plan_with_search_team_info_and_unknowns.md`. Although all of the terrain and weather information was specified in this test, the LLM added the "Adaption Plan" section and a sentence at the end saying that the plan will be adapted based on the Incident Commander's guidance and field reports. This was a nice improvement to see because it shows that the LLM is anticipating that the plan will be revised when new information becomes available.

### Next Steps
If I had more time, here are the next steps I would take:
1. Improve testing. The 2 tests for generating a Search Plan go through the entire process, from the natural language input to generating a plan based on the knowledge base. To save energy and test only one thing at a time, it would be better to use a fixed `KnowledgeBase` instance for `test_create_search_plan()`, and a fixed `KnowledgeBase` instance and plan for `test_create_search_plan_with_search_team_info()`. The test suite could also use tests for errors because there are many functions that could raise an error.
2. Implement functionality to update the Search Plan based on new information from the Incident Commander or a Search Team Leader. This is a good suggestion from Joel, and it would make the agent robust to changes during the SAR operation.
3. Find an easier way to write the schemas for the LLM structured output. It was pretty annoying to type out all the nested dictionaries.
4. Test the agent's scalability by giving it a large knowledge base or generating a more detailed Search Plan. The LLM would probably struggle to remember things if it received a lot of knowledge in one prompt. Techniques like RAG could improve performance when there is a lot of information to consider in the Search Plan. An easier improvement to make would be generating the per-team Search Plans one at a time instead of as an array, to hopefully encourage the LLM to give more detailed instructions to each team.
