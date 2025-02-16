# Operations Section Chief Agent
Author: Andrew Cheung


## Description
The Operations Section Chief Agent receives mission objectives and knowledge base information from the Incident Commander, which are all given as natural language strings. Then, it uses the information to generate a search plan.

Notes about the agent:
* The code is located in `src/sar_project/agents/operations_section_chief_agent.py`, and the tests are in `tests/test_operations_section_chief_agent.py`. You can run the tests with `pytest -rP` to have the search plan printed to stdout.
* The agent's `process_request()` method takes `message` as a parameter, which must be a dictionary. It requires a `source` key in the dictionary, which must be either `incident_commander` or `search_team_leader`. 
* Other supported keys in the `message` dictionary are: `location` (required for incident_commander messages), `terrain_data`, `weather_data`, `resource_status`, and `mission_objectives`.
* The `terrain_data`, `weather_data`, `resource_status`, and `mission_objectives` values in the `message` dictionary should be natural language strings. The agent uses Google Gemini's Structured Output feature to convert the values into JSON, which is parsed and put into the knowledge base.
* The `process_request()` method returns a dictionary, whose keys may include: `knowledge_base_updated` (a boolean), `mission_objectives_understood` (a boolean), and `search_plan` (a string describing the agent's search plan).
* The `search_team_leader` communication is not yet implemented, but my current idea is to specify the number of search teams in the plan creation prompt, and then send the relevant part to each Search Team Leader.


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
