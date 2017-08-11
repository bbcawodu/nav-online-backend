# Conversation Workflow Snapshot HTTP REST Endpoint README - Presence Health

![Conversation Workflow Snapshot ERD - Presence Health](../../db_erds/presence_health/conversation_workflow_snapshot_erd.jpg)

## IN DEVELOPMENT
### Conversation Workflow Snapshot: Read Method Endpoint
- To read/query rows in the conversation_workflow_snapshot table of the database, make a GET request to
http://patient-assist-backend.herokuapp.com/v1/conversation_workflow_snapshot/
    - Results returned in the response body will be filtered by the parameters given in the query string of the request url.
    - The parameters given in the REQUIRED query string can be divided into 2 categories: "primary" and "secondary"
    
    - "primary" parameters - One and exactly one of these parameters are required in every request query string.
        - "id" corresponds to the id column of the conversation_workflow_snapshot table.
            - Must be an integer
            - Can be multiple values separated by commas.
            - passing "all" as the value will return all conversation_workflow_snapshot rows.
        - "browsing_session_id" corresponds to the id column of the presence_browsing_session_data table that a conversation_workflow_snapshot row is related to.
            - Must be an integer
            - Can be multiple values separated by commas.
            - passing "all" as the value will return all conversation_workflow_snapshot rows.
        - "calculated_intent" corresponds to the calculated_intent column of the conversation_workflow_snapshot table.
            - Must be an ascii string that has all non-ascii characters url encoded
        - "workflow_name" corresponds to the workflow_name column of the conversation_workflow_snapshot table.
            - Must be an ascii string that has all non-ascii characters url encoded
            
    - "Secondary" parameters - Any number of these parameters can be added to a request query string.
        - "min_keyword_clicks" corresponds to the minimum value for the 'keyword'_clicks column of the conversation_workflow_snapshot table where 'keyword' is the corresponding intent keyword.
            - Must be an integer.
        - "min_'keyword'_hover_time" corresponds to the minimum value for the 'keyword'_hover_time column of the conversation_workflow_snapshot table where 'keyword' is the corresponding intent keyword.
            - Must be a float.
        - "min_date" - Minimum date for the date_created column of the conversation_workflow_snapshot table
            - Must be given in "YYYY-MM-DD" format
        - "max_date" - Maximum date for the date_created column of the conversation_workflow_snapshot table
            - Must be given in "YYYY-MM-DD" format
    
- The response body will be JSON formatted text with the following format:
    ```
    {
        "Data": [
            {
                "keyword_clicks": Integer,
                "keyword'_hover_time": Float,
                'workflow_name': String,
                'workflow_version': String,
                'calculated_intent': String,
                'intent_formula_version': String,
                "session_time": Float,
                "conversation_progress": Float,
                "total_steps": Integer,
                'date_created': String,
                "id": Integer,
                "browsing_session_id": Integer,
            },
            ...,
            ...,
            ...,
        ],
        "Status": {
            "Version": 1.0,
            "Error Code": Integer,
            "Errors": Array
        }
    }
    ```
  
- If there ARE NO errors parsing the request body and rows in the conversation_workflow_snapshot table of the database ARE found:
    - The value for the "Errors" key in the response root object will an empty array
    - The value for the "Error Code" key in the response root object will be 0. 
- If there ARE errors parsing the request body or rows in the conversation_workflow_snapshot of the database ARE NOT found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" object.
        -Each item in the array is a string corresponding to an error parsing the JSON Body doc.
    - An empty array will be the value for the "Data" key.
