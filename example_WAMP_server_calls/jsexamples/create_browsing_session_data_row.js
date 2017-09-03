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

     dl.push(session.call('create_browsing_session_data_row').then(
        function (res) {
           console.log("Result: DB ID:" + res.kwargs.id);
           localStorage.setItem("pic_patient_assist_cookie_id", res.kwargs.id);
        }
     ));

     when.all(dl).then(function () {
        console.log("All finished.");
        connection.close();
     });


};

connection.open();
