# Smart Help Desk Dashboard User Stories - Presence Health

## User Persona
- As Sally Stakeholder, a stakeholder at Presence Health, I can visit the Smart Help Desk application to view consumer
intent, utilization, and capacity data collected by the patient assist plugin installed on the Presence Health website.
    - Smart Help Desk application wireframe - Presence Health:
        ![Smart Help Desk application wireframe - Presence Health](smart_help_desk_dashboard_wireframe.jpg)

    ### Acceptance Stories
    - Acceptance stories for Sally Stakeholder
    
        #### Scenario 1: Sally Stakeholder has authorized login credentials and visits the Smart Help Desk.
        - Given [context] And [some more context]… When [event] Then [outcome] And [another outcome]…

## System Personae
- As the Smart Help Desk application, an HTTP server with login based user authentication, I provide a web based
Graphical User Interface (GUI) that allows Presence Health Stakeholders to view consumer intent, utilization, and
capacity data collected by the patient assist plugin installed on the Presence Health website. I obtain the intent,
utilization, and capacity data for the GUI from the HTTP REST endpoints provided by the Patient Assist Browsing Data
HTTP server.
    - Smart Help Desk application wireframe - Presence Health:
        ![Smart Help Desk application wireframe - Presence Health](smart_help_desk_dashboard_wireframe.jpg)

    ### Acceptance Stories
    - Acceptance stories for Smart Help Desk application.
    
        #### Scenario 1: Smart Help Desk is visited with authorized login credentials.
        - Given [context] And [some more context]… When [event] Then [outcome] And [another outcome]…
        
- As the Patient Assist Browsing Data HTTP server, I provide RESTful HTTP endpoints that read browsing session and other 
related data collected from the patient assist plugin for Presence Health. These endpoints can be used to provide the 
data that the Smart Help Desk Application needs to populate its web based Graphical User Interface (GUI).
    - Patient Assist Browsing Data HTTP Server Documentation - Presence Health:
        - [Patient Assist Browsing Data HTTP Server Documentation - Presence Health](../../backend_server_api_documentation/presence_health/HTTP_server_API/index.md)