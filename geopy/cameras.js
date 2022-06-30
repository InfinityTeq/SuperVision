// const fs = require('fs');
import fs from 'fs';

fs.readFile('./maryland.kml', 'utf8', (err, data) => {
    if (err){
        console.error(err);
        return;
    }

    console.log(data);

    // <!-- <p id="output"></p> -->

// var strXML = '<?xml version="1.0" encoding="utf-8"?><Events><EventItem id="101"><Country>India</Country><Phone Link="12345">homes</Phone></EventItem></Events>'; 
// var doc;


// if(window.ActiveXObject)  
// {  
//     doc = new ActiveXObject('Microsoft.XMLDOM'); // For IE6, IE5  
//     doc.async = 'false';  
//     doc.loadXML(strXML);  
// }  
// else  
// {  
//     var parser = new DOMParser();  
//     doc = parser.parseFromString(strXML, 'text/xml'); // For Firefox, Chrome etc  
// }  
  
// var x = doc.getElementsByTagName("EventItem");  
// for (i = 0;i < x.length; i++)  
// {  
//    alert(x[i].getElementsByTagName("Country")[0].childNodes[0].nodeValue); // India  
//    var poc = x[i].getElementsByTagName("Phone")[0].getAttribute('Link');// 12345  
// }

window.onload = function() {

//   document.getElementById('output').innerHTML = poc;
  document.getElementById('output').innerHTML = data;
};
})
