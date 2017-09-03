# Scheduled Appointment With Navigator HTTP REST Endpoint README - Presence Health

![Scheduled Appointment With Navigator ERD - Presence Health](../../../db_erds/presence_health/presence_scheduled_appointment_erd.jpg)

### IN DEVELOPMENT
## Scheduled Appointment With Navigator: Read Method Endpoint
- To read/query rows in the presence_scheduled_appointment table of the database, make a GET request to
http://patient-assist-backend.herokuapp.com/v1/presence_health/presence_scheduled_appointment/
    - Results returned in the response body will be filtered by the parameters given in the query string of the request url.
    - The parameters given in the REQUIRED query string can be divided into 2 categories: "primary" and "secondary"
    
    - "primary" parameters - One and exactly one of these parameters are required in every request query string.
        - "id" corresponds to the id column of the presence_scheduled_appointment table.
            - Must be an integer
            - Can be multiple values separated by commas.
            - passing "all" as the value will return all presence_scheduled_appointment rows.
        - "browsing_session_id" corresponds to the id column of the presence_browsing_session_data table that a presence_scheduled_appointment row is related to.
            - Must be an integer
            - Can be multiple values separated by commas.
            - passing "all" as the value will return all presence_scheduled_appointment rows.
        - "intent" corresponds to the intent_of_appointment column of the presence_scheduled_appointment table.
            - Must be an ascii string that has all non-ascii characters url encoded
        - "first_name" corresponds to the navigator_first_name column of the presence_scheduled_appointment table.
            - Must be a string
            - Can be multiple values separated by commas.
        - "last_name" corresponds to the navigator_last_name column of the presence_scheduled_appointment table.
            - Must be a string
            - Can be multiple values separated by commas.
        - "email" corresponds to the navigator_email column of the presence_scheduled_appointment table.
            - Must be a string
            - Can be multiple values separated by commas.
        - SPECIAL CASE: Only "first_name" and "last_name" can be given simultaneously as parameters.
            - When "first_name" and "last_name" are given at the same time, only one value of each permitted.
            
    - "Secondary" parameters - Any number of these parameters can be added to a request query string.
        - "min_date" - Minimum date for the appointment_date column of the presence_scheduled_appointment table
            - Must be given in "YYYY-MM-DD" format
        - "max_date" - Maximum date for the appointment_date column of the presence_scheduled_appointment table
            - Must be given in "YYYY-MM-DD" format
    
- The response body will be JSON formatted text with the following format:
    ```
    {
        "Data": [
            {
                'navigator_first_name': String,
                'navigator_last_name': String,
                'navigator_email': String,
                'appointment_date': String,
                'intent_of_appointment': String,
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
  
- If there ARE NO errors parsing the request body and rows in the presence_scheduled_appointment table of the database ARE found:
    - The value for the "Errors" key in the response root object will an empty array
    - The value for the "Error Code" key in the response root object will be 0. 
- If there ARE errors parsing the request body or rows in the presence_scheduled_appointment of the database ARE NOT found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" object.
        -Each item in the array is a string corresponding to an error parsing the JSON Body doc.
    - An empty array will be the value for the "Data" key.
