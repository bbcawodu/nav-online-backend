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
   realm: 'patient_assist_realm'}
);
console.log(wsuri);

// localStorage.removeItem("pic_patient_assist_cookie_id");
var cookie_id = localStorage.getItem("pic_patient_assist_cookie_id");

connection.onopen = function (session) {
   // var dl = [];
   //
   // if (cookie_id == null){
   //     dl.push(session.call('patient_assist_backend.presence_health.create_browsing_data_instance').then(
   //        function (res) {
   //           console.log("Result: DB ID:" + res.kwargs.id + ", Cookie ID: " + res.kwargs.cookie_id);
   //           localStorage.setItem("pic_patient_assist_cookie_id", res.kwargs.cookie_id);
   //        }
   //     ));
   // }
   //
   // else{
   //     var browsing_data_obj = {"cookie_id": cookie_id,
   //                           "keyword": "oncology",
   //                           "keyword_clicks": 2,
   //                           "keyword_hover_time": 3.2};
   //
   //     dl.push(session.call('patient_assist_backend.presence_health.submit_browsing_data', [JSON.stringify(browsing_data_obj)]).then(
   //        function (res) {
   //           console.log("Result: clicks:" + res.kwargs.oncology_clicks + ", hover time: " + res.kwargs.oncology_hover_time);
   //        },
   //        function (err) {
   //           console.log("Error:", err.error, err.args, err.kwargs);
   //        }
   //     ));
   //
   //     // dl.push(session.call('patient_assist_backend.presence_health.disable_cta_updates', [cookie_id]).then(
   //     //    function (res) {
   //     //       console.log("Result: Cookie ID:" + res.kwargs.cookie_id + ", Sending Browsing Data?: " + res.kwargs.sending_browsing_data);
   //     //    },
   //     //    function (err) {
   //     //       console.log("Error:", err.error, err.args, err.kwargs);
   //     //    }
   //     // ));
   // }
   //
   // when.all(dl).then(function () {
   //    console.log("All finished.");
   //    connection.close();
   // });

   session.call('patient_assist_backend.presence_health.enable_cta_updates', [cookie_id]).then(
      function (res) {
         console.log("Result: Cookie ID:" + res.kwargs.cookie_id + ", Sending Browsing Data?: " + res.kwargs.sending_browsing_data);
      },
      function (err) {
         console.log("Error:", err.error, err.args, err.kwargs);
      }
    );

   function onevent1(args, kwargs) {
      console.log("Result: call to action url:" + kwargs.cta_url);
   }

   var sub_url = 'patient_assist_backend.presence_health.new_ctas.' + cookie_id;
   console.log(sub_url);
   session.subscribe(sub_url, onevent1);
};

connection.open();
