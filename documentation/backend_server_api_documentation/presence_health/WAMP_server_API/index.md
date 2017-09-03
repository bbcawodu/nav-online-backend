# WAMP Server API README - Presence Health
- These WAMP enpoints let you save and access the browsing data on a session by session basis collected from the patient
assist tool in our database in soft real time.
- The websocket uri for the WAMP server is: ws://patient-assist-backend.herokuapp.com/ws
- All WAMP components/enpoints are in the realm: presence_health_realm

## Database ERD
- Entity Relational Diagram for the database that the Presence Health backend servers use.

    ### [Complete Browsing Data Database ERD - Presence Health](../../../db_erds/presence_health/full_db_erd.jpg)

## WAMP (Real time) Endpoints
- Documentation for WAMP Endpoints that provide the API for reading/writing browsing data collected from the patient
assist tool installed on the Presence Health website.

    ## WAMP Endpoint: Browsing Session Data - Presence Health
    - These WAMP endpoints provide the API to read/query from and write to the Browsing Session Data table for Presence Health
    
        ### [Browsing Session Data WAMP RPC Endpoints README](presence_browsing_session_data_WAMP_RPC_endpoints_README.md)
    
    ## WAMP Endpoint: Browsing Intent Snapshot - Presence Health
    - IN DEVELOPMENT
    - These WAMP endpoints provide the API to read/query from and write to the Browsing Intent Snapshot table for Presence Health
    
        ### [Browsing Intent Snapshot WAMP RPC Endpoints README](presence_browsing_intent_snapshot_WAMP_RPC_endpoints_README.md)
    
    ## WAMP Endpoint: CTA Shown To User - Presence Health
    - IN DEVELOPMENT
    - These WAMP endpoints provide the API to read/query from and write to the CTA Shown To User table for Presence Health
        
        ### [CTA Shown To User WAMP RPC Endpoints README](presence_cta_shown_to_user_WAMP_RPC_endpoints_README.md)
    
    ## WAMP Endpoint: Conversation Workflow Snapshot - Presence Health
    - IN DEVELOPMENT
    - These WAMP endpoints provide the API to read/query from and write to the Conversation Workflow Snapshot table for Presence Health
        
        ### [Conversation Workflow Snapshot WAMP RPC Endpoints README](presence_conversation_workflow_snapshot_WAMP_RPC_endpoints_README.md)
    
    ## WAMP Endpoint: Scheduled Appointment With Navigator - Presence Health
    - IN DEVELOPMENT
    - These WAMP endpoints provide the API to read/query from and write to the Scheduled Appointment With Navigator table for Presence Health
    
        ### [Scheduled Appointment With Navigator WAMP RPC Endpoints README](presence_scheduled_appointment_WAMP_RPC_endpoints_README.md)
