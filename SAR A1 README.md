# Operations Section Chief Agent
Author: Andrew Cheung


## Description
The Operations Section Chief Agent receives mission objectives from the Incident Commander and gives instructions to Search Team Leaders in order to achieve the mission objectives.


## Necessary Environment Variables
* GOOGLE_API_KEY: API key for Google Gemini
* DEPLOYMENT_NAME=SAR_Project


## Message Format
* The self.process_message() function has a <i>message</i> parameter, which must be a dictionary. The dictionary must have a "source" key, and its value must be either "incident_commander" or "search_team_leader".
