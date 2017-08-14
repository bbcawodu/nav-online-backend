## Scheduled Appointment With Navigator WAMP Server API README - Presence Health
### The websocket uri for the WAMP server is: ws://patient-assist-backend.herokuapp.com/ws
### All WAMP components/enpoints are in the realm: patient_assist_realm

![Scheduled Appointment With Navigator ERD - Presence Health](../../db_erds/presence_health/scheduled_appointment_with_navigator_erd.jpg)

### IN DEVELOPMENT
## Procedure Endpoint: Create row in the scheduled_appointment_with_navigator table of the database
## URI: patient_assist_backend.presence_health.create_scheduled_appointment_with_navigator_record
    ```
    This procedure creates a new row in the scheduled_appointment_with_navigator table of the database and adds a many to
    one relationship to the presence_browsing_session_data row whose id field matches the given browsing_session_id parameter.
    
    Procedure uri: 'patient_assist_backend.presence_health.create_scheduled_appointment_with_navigator_record'
    
    :param args: Argument list. Accepts only one argument
                 [browsing_session_id]
                 browsing_session_id: (type: Integer) Database id of presence_browsing_session_data row to establish relation to.
      
    :return: Returns an object that has a property, kwargs. That property will have the following properties:
            id: (type: Integer) Database id of new scheduled_appointment_with_navigator row.
            browsing_session_id: (type: Integer) Database id of presence_browsing_session_data row that the new scheduled_appointment_with_navigator row is related to.
            appointment_date: (type: String) Date of appointment with navigaror in "YYYY-MM-DD" format.
            navigator_first_name: (type: String) First name of the navigator that scheduled appointment is with.
            navigator_last_name: (type: String) Last name of the navigator that scheduled appointment is with.
            navigator_email: (type: String) Email of the navigator that scheduled appointment is with.
            intent_of_appointment: (type: String) Intent keyword of the scheduled appointment.
    ```

- Example Javascript Call
    ```
    <!DOCTYPE html>
    <html>
       <body>
          <h1>Example Client Side Calls to Patient Assist Backend</h1>
          <p>Open JavaScript console to watch output.</p>
          <script src="https://autobahn.s3.amazonaws.com/autobahnjs/latest/autobahn.min.jgz"></script>
          <script>
          try {
               var autobahn = require('autobahn');
               var when = require('when');
            } catch (e) {
               // When running in browser, AutobahnJS will
               // be included without a module system
               var when = autobahn.when;
            }
            
            var wsuri = "ws://patient-assist-backend.herokuapp.com/ws";
            var connection = new autobahn.Connection({
                               url: wsuri,
                               realm: 'patient_assist_realm'}
                            );
                            
            connection.onopen = function (session) {
               var dl = [];
               var browsing_session_id = 1;
            
               dl.push(session.call('patient_assist_backend.presence_health.create_scheduled_appointment_with_navigator_record', [browsing_session_id]).then(
                  function (res) {
                     console.log("Result: db id:" + res.kwargs.id + 
                     ", browsing session id: " + res.kwargs.browsing_session_id +
                     ", appointment date: " + res.kwargs.appointment_date +
                     ", navigator first name: " + res.kwargs.navigator_first_name +
                     ", navigator last name: " + res.kwargs.navigator_last_name +
                     ", navigator email: " + res.kwargs.navigator_email +
                     ", intent of appointment: " + res.kwargs.intent_of_appointment);
                  }
               ));
            
               when.all(dl).then(function () {
                  console.log("All finished.");
                  connection.close();
               });
            };
            
            connection.open();
          </script>
       </body>
    </html>
    ```

### IN DEVELOPMENT
## Procedure Endpoint: Read rows from scheduled_appointment_with_navigator table of the database
## URI: patient_assist_backend.presence_health.read_scheduled_appointment_with_navigator_records
    ```
    This procedure reads/queries the scheduled_appointment_with_navigator table of the database for rows whose id field of
    the related presence_browsing_session_data row matches the given id parameter.
    
    Procedure uri: 'patient_assist_backend.presence_health.read_scheduled_appointment_with_navigator_records'
    
    :param args: Argument list. Accepts only one argument
                 [browsing_session_id]
                 browsing_session_id: (type: Integer) Database id of related presence_browsing_session_data row.
      
    :return: Returns an object that has a property, kwargs. That property will have a property, data, which is an array.
    Each object in that array will have the following properties:
            id: (type: Integer) Database id of scheduled_appointment_with_navigator row.
            browsing_session_id: (type: Integer) Database id of presence_browsing_session_data row that the scheduled_appointment_with_navigator row is related to.
            appointment_date: (type: String) Date of appointment with navigaror in "YYYY-MM-DD" format.
            navigator_first_name: (type: String) First name of the navigator that scheduled appointment is with.
            navigator_last_name: (type: String) Last name of the navigator that scheduled appointment is with.
            navigator_email: (type: String) Email of the navigator that scheduled appointment is with.
            intent_of_appointment: (type: String) Intent keyword of the scheduled appointment.
    ```

- Example Javascript Call
    ```
    <!DOCTYPE html>
    <html>
       <body>
          <h1>Example Client Side Calls to Patient Assist Backend</h1>
          <p>Open JavaScript console to watch output.</p>
          <script src="https://autobahn.s3.amazonaws.com/autobahnjs/latest/autobahn.min.jgz"></script>
          <script>
          try {
               var autobahn = require('autobahn');
               var when = require('when');
            } catch (e) {
               // When running in browser, AutobahnJS will
               // be included without a module system
               var when = autobahn.when;
            }
            
            var wsuri = "ws://patient-assist-backend.herokuapp.com/ws";
            var connection = new autobahn.Connection({
                               url: wsuri,
                               realm: 'patient_assist_realm'}
                            );
                            
            connection.onopen = function (session) {
               var dl = [];
               var browsing_session_id = 1;
            
               dl.push(session.call('patient_assist_backend.presence_health.read_scheduled_appointment_with_navigator_records', [browsing_session_id]).then(
                  function (res) {
                     var results = res.kwargs.data;
                     
                     for (i = 0; i < results.length; i++){
                         var scheduled_appointment_with_navigator_row_object = results[i];
                         
                         console.log("Result: db id:" + scheduled_appointment_with_navigator_row_object.id + 
                         ", browsing session id: " + scheduled_appointment_with_navigator_row_object.browsing_session_id +
                         ", appointment date: " + scheduled_appointment_with_navigator_row_object.appointment_date +
                         ", navigator first name: " + scheduled_appointment_with_navigator_row_object.navigator_first_name +
                         ", navigator last name: " + scheduled_appointment_with_navigator_row_object.navigator_last_name +
                         ", navigator email: " + scheduled_appointment_with_navigator_row_object.navigator_email +
                         ", intent of appointment: " + scheduled_appointment_with_navigator_row_object.intent_of_appointment);
                     }
                  }
               ));
            
               when.all(dl).then(function () {
                  console.log("All finished.");
                  connection.close();
               });
            };
            
            connection.open();
          </script>
       </body>
    </html>
    ```
