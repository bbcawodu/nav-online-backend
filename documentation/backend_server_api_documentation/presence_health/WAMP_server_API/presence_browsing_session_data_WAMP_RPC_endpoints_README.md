# Browsing Session Data WAMP Server API README  - Presence Health
### The websocket uri for the WAMP server is: ws://patient-assist-backend.herokuapp.com/ws
### All WAMP components/enpoints are in the realm: presence_health_realm

![Browsing Session Data ERD - Presence Health](../../../db_erds/presence_health/presence_browsing_session_data_erd.jpg)

## [Current list of intent keywords](http://picbackend.herokuapp.com/v2/cta/?intent=all)

## Procedure Endpoint: Create row in the presence_browsing_session_data table
## URI: create_browsing_session_data_row
    ```
    This procedure creates a new row in the presence_browsing_session_data table of the database and returns the db id of the
    newly created entry.
    
    Procedure uri: 'create_browsing_session_data_row'
    
    Takes no params
      
    :return: Returns an object that has a property, kwargs. That property will have the following properties:
            id: (type: Integer) Database id of newly created presence health browsing data row
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
                               realm: 'presence_health_realm'}
                            );
                            
            connection.onopen = function (session) {
               var dl = [];
            
               dl.push(session.call('create_browsing_session_data_row').then(
                  function (res) {
                     console.log("Result: DB ID:" + res.kwargs.id);
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

## Procedure Endpoint: Submit Browsing Data Information for Presence Health
## URI: submit_browsing_data
    ```
    This procedure takes a given id corresponding to a row in the presence_browsing_session_data table along with
    client browsing data information, updates the row with that info, and returns relevant updated field data from that
    row.
    
    Procedure uri: 'submit_browsing_data'
    
    :param args: Argument list. Accepts only one argument
                 [browsing_data_json]
                 browsing_data_json: A JSON formatted object that has the following mandatory keys
                                     id: (type: String) id of presence health browsing data row
                                     keyword: (type: String) name corresponding the given browsing data. Currently only accepts 'oncology'
                                     keyword_clicks: (type: Integer) number of clicks corresponding to given keyword
                                     keyword_hover_time: (type: Float) length of hover time corresponding to given keyword
    :return: Returns an object that has a property, kwargs. That property will have the following properties:
            id: (type: Integer) Database id of newly created presence health browsing data row
            oncology_clicks: (type: Integer) Total number of clicks corresponding to the 'oncology' keyword
            oncology_hover_time: (type: Float) Total amount of time corresponding to the 'oncology' keyword
            
    Possible Errors:
    'patient_assist_backend.submit_browsing_data_presence_health' accepts exactly 1 argument, browsing data.
    browsing data must be a unicode objector string object.
    Decoding browsing data JSON has failed
    No Presence Health Browsing data entry found for id
    More than one Presence Health Browsing data entry found for id
    'id' must be a unicode or string object
    'id' key is not present in browsing data JSON object.
    'keyword' must be a unicode or string object.
    'keyword' must be in the following list of accepted keywords: ['oncology', etc.]
    'keyword' key is not present in browsing data JSON object.
    'keyword_clicks' must be an integer.
    'keyword_clicks' must be an positive.
    'keyword_clicks' key is not present in browsing data JSON object.
    'keyword_hover_time' must be a floating point.
    'keyword_hover_time' must be positive
    'keyword_hover_time' key is not present in browsing data JSON object.
    
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
                               realm: 'presence_health_realm'}
                            );
                            
            connection.onopen = function (session) {
               var dl = [];
            
               var browsing_data_obj = {"id": 16,
                                        "keyword": "oncology",
                                        "keyword_clicks": 2,
                                        "keyword_hover_time": 3.2};
               dl.push(session.call('submit_browsing_data', [JSON.stringify(browsing_data_obj)]).then(
                  function (res) {
                     console.log("Result: clicks:" + res.kwargs.oncology_clicks + ", hover time: " + res.kwargs.oncology_hover_time);
                  },
                  function (err) {
                     console.log("Error:", err.error, err.args, err.kwargs);
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

## Procedure Endpoint: Read row from presence_browsing_session_data table of the database
## URI: read_browsing_session_data_row
    ```
    This procedure reads/queries the presence_browsing_session_data table of the database for a row that has a matching
    value in the id field for the given id parameter.
    
    Procedure uri: 'read_browsing_session_data_row'
    
    :param args: Argument list. Accepts only one argument
                 [id]
                 id: (type: Integer) Database id of desired row.
      
    :return: Returns an object that has a property, kwargs. That property will have the following properties:
             id: (type: Integer) id of presence_browsing_session_data row
             keyword_clicks: (type: Integer) number of clicks corresponding to given keyword
             keyword_hover_time: (type: Float) length of hover time corresponding to given keyword
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
                               realm: 'presence_health_realm'}
                            );
                            
            connection.onopen = function (session) {
               var dl = [];
               var id = 1;
            
               dl.push(session.call('read_browsing_session_data_row', [id]).then(
                  function (res) {
                     console.log("Result: id:" + res.kwargs.id +
                         ", clicks:" + res.kwargs.oncology_clicks +
                         ", hover time: " + res.kwargs.oncology_hover_time +
                     ", date_created: " + res.kwargs.date_created +
                     ", date_last_updated: " + res.kwargs.date_last_updated);
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
    
## Procedure Endpoint: Read current browsing intent of row from presence_browsing_session_data table of the database
## URI: read_current_browsing_intent
    ```
    This procedure calculates and returns the current browsing intent of a row in the presence_browsing_session_data
    table of the database for the given id parameter.
    
    Procedure uri: 'read_current_browsing_intent'
    
    :param args: Argument list. Accepts only one argument
                 [id]
                 id: (type: Integer) Database id of desired row.
      
    :return: Returns an object that has a property, kwargs. That property will have the following properties:
             id: (type: Integer) id of presence_browsing_session_data row
             current_intent: (type: String) current browsing intent of given row
             cta_url: (type: String) URL for Call to Action for current browsing intent
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
                               realm: 'presence_health_realm'}
                            );
                            
            connection.onopen = function (session) {
               var dl = [];
               var id = 1;
            
               dl.push(session.call('read_current_browsing_intent', [id]).then(
                  function (res) {
                     console.log("Result: DB ID:" + res.kwargs.id + ", current_intent: " + res.kwargs.current_intent + ", cta_url: " + res.kwargs.cta_url);
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
