function showLog(index) {
  
  var xmlhttp = new XMLHttpRequest();
var docelem;
  xmlhttp.onreadystatechange = function () {
    if (xmlhttp.readyState == 4) {
      if (xmlhttp.status == 200) {
        //var elem = document.getElementById("output");
        docelem = xmlhttp.responseXML.documentElement;
        var elem = document.getElementById("elog");
        //var nodes = docelem.getElementsByTagName("e_log");
        //for (i = 0; i < nodes.length; i++) {
        //  elem.innerHTML += nodes[i].tagName + ":" + nodes[i].textContent + "<br/>";
        //}

        elem.innerHTML = "\n";
        var nodes = docelem.getElementsByTagName("elog_id");
        for (i = 0; i < nodes.length; i++) {
          if(i==0)elem.innerHTML += "======" + nodes[i].tagName + "======" + "\n";
          elem.innerHTML += nodes[i].textContent + "\n";
        }

        var nodes = docelem.getElementsByTagName("date");
        for (i = 0; i < nodes.length; i++) {
          if(i==0)elem.innerHTML += "======" + nodes[i].tagName + "======" + "\n";
          elem.innerHTML += nodes[i].textContent + "\n";
        }
        var nodes = docelem.getElementsByTagName("category");
        for (i = 0; i < nodes.length; i++) {
          if(i==0)elem.innerHTML += "======" + nodes[i].tagName + "======" + "\n";
          elem.innerHTML += nodes[i].textContent + "\n";
        }
        var nodes = docelem.getElementsByTagName("subject");
        for (i = 0; i < nodes.length; i++) {
          if(i==0)elem.innerHTML += "======" + nodes[i].tagName + "======" + "\n";
          elem.innerHTML += nodes[i].textContent + "\n";
        }
        var nodes = docelem.getElementsByTagName("content");
        for (i = 0; i < nodes.length; i++) {
          if(i==0)elem.innerHTML += "======" + nodes[i].tagName + "======" + "\n";
          elem.innerHTML += nodes[i].textContent.replace(/;/g,"\n") + "\n";
        }

      } else {
        alert("status = " + xmlhttp.status);
      }
    }
  }
    if(index<10)var filename = "e_log/elog_"+(("00000000")+index).substr(-8)+".xml";
    if(index<100)var filename = "e_log/elog_"+(("0000000")+index).substr(-8)+".xml";
  xmlhttp.open("GET",filename,true);
  xmlhttp.send();
}


//function get_latestid(){
//  logfile = "e_log/elog_id.txt";
//  var xmlHttp = new XMLHttpRequest();
//  var id = "";
//  xmlHttp.onreadystatechange = function(){
//    if(xmlHttp.readyState==4 && xmlHttp.status==200){
//      id = xmlHttp.responseText;
//    }
//  }
//  xmlHttp.open("get",logfile,true);
//  xmlHttp.send();
//
//  alert(id)
//  return id;
//}

function showLogByID(){
  //var index = document.getElementById("elog_id").value;
  var index = document.getElementById("elog_id").value;
  showLog(index);
}

function showLatestLog(){
  var id = Number(get_latestid())-1;
  //alert(id);
  showLog(id);
}


function backMon(){
  window.location.href="https://www-he.scphys.kyoto-u.ac.jp/member/ingrid/wagasci_monitor/";
}
