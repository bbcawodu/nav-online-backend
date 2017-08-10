## Connecting to Patient Assist Browsing Data Backend Servers README

### Ways to Connect to the Patient Assist Backend
- There are 2 primary ways to connect to the patient assist backend through the web; using the HTTP protocol and using the WAMP (Web Application Messaging Protocol) protocol.
    - **HTTP Protocol Server**
        - Connecting to the HTTP protocol server gives access to RESTful web service endpoints that allow you to read
        browsing data for partner hospitals that was collected from the patient assist tool.
        - The primary use case for these endpoints is to provide the data used in the 'Intent, Utilization, and Capacity'
        dashboard.
        - To access an in browser, dashboard view of the stored browsing data on the Patient Assist Backend, visit
        "http://patient-assist-backend.herokuapp.com/admin"
    - **WAMP Protocol Server**
        - Connecting to the WAMP protocol server  gives real time(soft) access to the browsing data database using WAMP's
        remote procedure call(RPC) and pubsub protocols.
        - The primary use case for these endpoints is to save and access the browsing data collected from the patient
        assist tool in our database, on a session by session basis, in soft real time.
        - **WAMP protocol docs**
            - In order to have real-time(soft) web access to the patient assist browsing data backend, you must connect
            to this server and use the WAMP protocol endpoints and services that are provided. There are several
            libraries that provide a WAMP implementation available for different programming languages.
            Here are a few:
                  - Autobahn|Python: http://autobahn.ws/python/
                  - Autobahn|JS: http://autobahn.ws/js/
            - Once you have chosen a library and a programming language, you can connect to our server using the
            websocket uri, "ws://patient-assist-backend.herokuapp.com/ws". All WAMP components are in the realm,
            "patient_assist_realm."