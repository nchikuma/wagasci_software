(function(){
 var menu = document.getElementById('tab-links');
 var content = document.getElementById('tab_content');
 var menus = menu.getElementsByTagName('a');
 var current;
 for (var i = 0, l = menus.length;i < l; i++){
 tab_init(menus[i], i);
 }

 function tab_init(link, index){
 var id = link.hash.slice(1);
 var tab = document.getElementById(id);
 if (!current){ 
 current = {tab:tab, menu:link};
 tab.style.display = 'block';
 link.className = 'active';
 } else { 
 tab.style.display = 'none';
 } 

 link.onclick = function(){
   current.tab.style.display = 'none';
   current.menu.className = '';
   tab.style.display = 'block';
   link.className = 'active';
   current.tab = tab;
   current.menu = link;
   return false;
 };
 }
})();


var file = document.querySelector('#getfile');

file.onchange = function (){
  var fileList = "log/slowmonitor.log"; //file.files;
  var reader = new FileReader();
  reader.readAsText(fileList[0]);
  reader.onload = function  () {
    document.querySelector('#preview').textContent = reader.result;
  };
};
