img0_ps=new Image()
img0_ps.src="log/lambda_history1.png"
img1_ps=new Image()
img1_ps.src="log/lambda_history2.png"
img2_ps=new Image()
img2_ps.src="log/lambda_history3.png"
img3_ps=new Image()
img3_ps.src="log/lambda_history4.png"
img0_ws=new Image()
img0_ws.src="log/waterlevel_history1.png"
img1_ws=new Image()
img1_ws.src="log/waterlevel_history2.png"
img2_ws=new Image()
img2_ws.src="log/waterlevel_history3.png"
img3_ws=new Image()
img3_ws.src="log/waterlevel_history4.png"
img0_ts=new Image()
img0_ts.src="log/temperature_history1.png"
img1_ts=new Image()
img1_ts.src="log/temperature_history2.png"
img2_ts=new Image()
img2_ts.src="log/temperature_history3.png"
img3_ts=new Image()
img3_ts.src="log/temperature_history4.png"

var logtxt=["slowmonitor.log","alarm.log","decode.log","temperature.log"];


function imgChange_ps(parts){
  fname=parts.options[parts.selectedIndex].value;
  if(fname==0){document.imgsmp_ps.src=img0_ps.src;}
  if(fname==1){document.imgsmp_ps.src=img1_ps.src;}
  if(fname==2){document.imgsmp_ps.src=img2_ps.src;}
  if(fname==3){document.imgsmp_ps.src=img3_ps.src;}
}
function imgChange_ws(parts){
  fname=parts.options[parts.selectedIndex].value;
  if(fname==0){document.imgsmp_ws.src=img0_ws.src;}
  if(fname==1){document.imgsmp_ws.src=img1_ws.src;}
  if(fname==2){document.imgsmp_ws.src=img2_ws.src;}
  if(fname==3){document.imgsmp_ws.src=img3_ws.src;}
}
function imgChange_ts(parts){
  fname=parts.options[parts.selectedIndex].value;
  if(fname==0){document.imgsmp_ts.src=img0_ts.src;}
  if(fname==1){document.imgsmp_ts.src=img1_ts.src;}
  if(fname==2){document.imgsmp_ts.src=img2_ts.src;}
  if(fname==3){document.imgsmp_ts.src=img3_ts.src;}
}
function showLog(logNo){
  logfile = "log/"+logtxt[logNo-1];
  if(confirm("Do you want to open " + logfile + "?")){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function(){
      if(xmlHttp.readyState==4 && xmlHttp.status==200){
        document.getElementById("log_disp").innerHTML = xmlHttp.responseText;
      }
    }
    xmlHttp.open("get",logfile,true);
    xmlHttp.send();
  }
}


window.onload = function(){
  imgChange_ps(document.form_ps.period_ps);
  imgChange_ws(document.form_ws.period_ws);
}


