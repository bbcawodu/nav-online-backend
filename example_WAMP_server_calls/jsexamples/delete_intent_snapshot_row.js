try {
   var autobahn = require('autobahn');
   var when = require('when');
} catch (e) {
   // When running in browser, AutobahnJS will
   // be included without a module system
   var when = autobahn.when;
}

// dynamic connection uri based on file location
var wsuri;
if (document.location.origin == "file://") {
   wsuri = "ws://127.0.0.1:8080/ws";

} else {
   wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
               document.location.host + "/ws";
}

var connection = new autobahn.Connection({
   url: wsuri,
   realm: 'presence_health_realm'}
);
console.log(wsuri);

connection.onopen = function (session) {
   var dl = [];

   var browsing_session_id_json = {
       "id": '3'
   };

     dl.push(session.call('delete_browsing_intent_snapshot_row', [JSON.stringify(browsing_session_id_json)]).then(
        function (res) {
         console.log("Result: id:" + res.kwargs.id);
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
