
function getTableValue(filename) {
    if ( $.fn.dataTable.isDataTable( '#example' ) ) {
      t = $('#example').DataTable();
   }
    else {
        //alert("initilize...");
        t = $('#example').DataTable( {
    "dom":'lrtip',
    stateSave: true,
      "columns": [
            {
                "className":      'details-control',
                "orderable":      false,
                "data":           null,
                "defaultContent": ""
            },
           {"data": "id" } ,
           {"data": "date" } ,
           {"data": "author" } ,
           {"data": "category" } ,
           {"data": "subject" } ,
           {"data": "content" } 
        ],
        "order": [[1, 'asc']],
  "columnDefs":[
  
{
        "targets":[1],
        "width":"10%"
    },
{
        "targets":[4],
        "width":"20%"
    },
{
        "targets":[6],
        "visible": false
    }
]
        } );//initialize datatables
   
    // Add event listener for opening and closing details
 $('#example tbody').on('click', 'tr td.details-control', function () {
         var tr = $(this).closest('tr');
        var row = t.row( tr );
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            //alert(row.data());
            tr.addClass('shown');
        }
    } );

        //
    }//end if else
    if(!filename)return;
    var child=null;
    var id;
    var date;
    var author="";
    var category="";
    var subject="";
    var content="";
    var docelem;
    
xmlhttp = new XMLHttpRequest();
    //xmlhttp.open("GET",filename,false);
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 ) {
            if (xmlhttp.status == 200) {
                docelem = xmlhttp.responseXML.documentElement;
                  var nodes = docelem.getElementsByTagName("elog_id");
                var nlength = nodes.length;
                for (i = 0; i < nlength; i++) {
                    id = nodes[i].textContent;
                }
                var nodes = docelem.getElementsByTagName("date");
                for (i = 0; i < nodes.length; i++) {
                    date = nodes[i].textContent;
                }
                var nodes = docelem.getElementsByTagName("author");
                var nlength = nodes.length;
                for (i = 0; i < nlength; i++) {
                    author = nodes[i].textContent;
                }
                var nodes = docelem.getElementsByTagName("category");
                for (i = 0; i < nodes.length; i++) {
                    category = nodes[i].textContent;
                }
                var nodes = docelem.getElementsByTagName("subject");
                for (i = 0; i < nodes.length; i++) {
                    subject = nodes[i].textContent;
                }
                var nodes = docelem.getElementsByTagName("content");
                for (i = 0; i < nodes.length; i++) {
                    content = nodes[i].textContent.replace(/;/g,"<br>")+"<br>";;
                }
                t.row.add( {
                "child"   : child,        
                "id"      :    id,
                "date"    :  date,
                "author"  :  author,
                "category":  category,
                "subject" :   subject,
                "content" :   content    
                        } ).draw(false  );
            } else {// status 200 if
                alert("status = " + xmlhttp.status);
            }
        }
    };
    xmlhttp.open("GET",filename,false);
    xmlhttp.send();
}

function get_latestid(){
    logfile = "e_log/elog_id.txt";
    var xmlHttp = new XMLHttpRequest();
    id="";
    xmlHttp.onreadystatechange = function(){
        if(xmlHttp.readyState==4 && xmlHttp.status==200){
            id = xmlHttp.responseText;
        }
    }
    xmlHttp.open("get",logfile,false);
    xmlHttp.send();

    //alert(id);
        return id;
}


function GetFileName(ifile){
    if(ifile<10)var filename = "e_log/elog_"+(("00000000")+ifile).substr(-8)+".xml";
    if(ifile<100)var filename = "e_log/elog_"+(("0000000")+ifile).substr(-8)+".xml";
    return filename;
}

function writeText(){

    var filename=[];
    var Nfile=get_latestid();
    //alert("!!");
    //alert(Nfile);
    for(var ifile=0;ifile<Nfile;ifile++){
        filename[ifile] = GetFileName(ifile);
        //alert(filename[ifile]);

        getTableValue(filename[ifile]);
    }

      table = $('#example').DataTable();
table
    .order( [ 1, 'desc' ] )
    .draw();

}
function addChild(){
 //alert("aaa!!");
    $('#example tbody').on('click', 'td.details-control', function () {
         var tr = $(this).closest('tr');
        var row = table.row( tr );
 
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            tr.addClass('shown');
        }
    } );
}




function filter(){
    $('input.global_filter').on( 'keyup click', function () {
        filterGlobal();
    } );
 
    $('input.column_filter').on( 'keyup click', function () {
        filterColumn( $(this).parents('td').attr('data-column') );
    } );

}

function addRow(classname,array,tableID){
    var tableRef = document.getElementById(tableID);
    var newrow = tableRef.insertRow(-1);
    var newcell=newrow.insertCell(-1);
    newcell.className = classname;
    newcell.innerHTML = array;
}

function searchChange(parts){                                       
    fname=parts.options[parts.selectedIndex].value;
    //alert(fname);
    if(fname==0){$("#filter_global").hide();}
    if(fname==1){$("#filter_col1").hide();}
    if(fname==2){$("#filter_col2").hide();}
    //if(fname==0){document.imgsmp_ps.src=img0_ps.src;}
    //if(fname==1){document.imgsmp_ps.src=img1_ps.src;}
    //if(fname==2){document.imgsmp_ps.src=img2_ps.src;}
    //if(fname==3){document.imgsmp_ps.src=img3_ps.src;}                           
  }          



/* Formatting function for row details - modify as you need */
function format ( d ) {
    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td>Author name:</td>'+
            //'<td>'+d.name+'</td>'+
            '<td>'+d.author+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Content:</td>'+
            //'<td>'+d.extn+'</td>'+
            '<td>'+d.content+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Extra info:</td>'+
            '<td>And any further details here (images etc)...</td>'+
        '</tr>'+
    '</table>';
}


 function filterGlobal () {
    $('#example').DataTable().search(
        $('#global_filter').val()
       // $('#global_regex').prop('checked'),
       // $('#global_smart').prop('checked')
    ).draw();
}
 
function filterColumn ( i ) {
    $('#example').DataTable().column( i ).search(
        $('#col'+i+'_filter').val()
        //$('#col'+i+'_regex').prop('checked'),
        //$('#col'+i+'_smart').prop('checked')
    ).draw();
}
 
