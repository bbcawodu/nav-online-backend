## Connecting to Patient Assist Backend README

### Connecting to Patient Assist Backend
- In order to connect to the patient assist backend, you must use the WAMP protocol. There are several libraries 
  available for different programming languages. Here are a few:
  - Autobahn|Python: autobahn.ws/python/
  - Autobahn|JS: http://autobahn.ws/js/
- Once you have chosen a library and a programming language, you can connect to the components of the backing using the
  Websocket uri, "ws://patient-assist-backend.herokuapp.com/ws". All components are in the realm, "patient_assist_realm."