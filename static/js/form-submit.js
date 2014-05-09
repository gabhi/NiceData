//AJAX FORM REQUEST
    $(document).ready(function() {
        var options = {
            target: '#ShowImage',
            beforeSubmit: checkFormValues
        };
        $("#GenImgForm").ajaxForm(options);
        $("#tabularsection").hide();
        return false;
    });

    //Intercept submit, hide text on submit
    function checkFormValues(formData,jqForm,options){
        var formIsValid = true;
        
        if(($('#tickerIn').val().length === 0)||($('#start_date').val().length === 0) || ($('#end_date').val().length === 0) ){
            alert("Please fill in all required fields.");
            return false;
        }

        //Else all is well, also update the jqGrid
        var start = $('#start_date').val().split('/').join('-');
        var end = $('#end_date').val().split('/').join('-');
        var newUrl = "/generate-data/"+$('#tickerIn').val()+".json?start="+start+"&end="+end;
        $("#tabulardata").jqGrid().setGridParam({url : newUrl}).trigger("reloadGrid");
        $("#tabularsection").show();
        $('#NoImageText').hide();
        return true;
    }
//END AJAX FORM REQUEST
//DATE PICKER 
    //Restrict dates to previous dates only
    var nowTemp = new Date();
    var yesterday = new Date(nowTemp.getFullYear(),nowTemp.getMonth(),nowTemp.getDate()-1,0,0,0,0);

    $('#start_date').datepicker({
        format: "yyyy/mm/dd",
        maxDate: -1,
        onRender: function(date){
            //Ensure that the date is valid
            return date.valueOf() > yesterday.valueOf() ? 'disabled' : '';
        }
    });
    $('#end_date').datepicker({
        format: "yyyy/mm/dd",
        maxDate: -1,
        onRender: function(date){
            return date.valueOf() > yesterday.valueOf() ? 'disabled' : '';
        }
    });
    $('#start_date').on('changeDate', function(ev){
        $(this).datepicker('hide');
    });
    $('#end_date').on('changeDate', function(ev){
        $(this).datepicker('hide');
    });
//END DATE PICKER
//TABULAR STOCK DATA

$('#tabulardata').jqGrid({
    url:null,
    datatype: "json",
    colNames:['Date','Close'],
    colModel: [
        {name:'date',index:'date',width:300},
        {name: 'close',index: 'close', width:100}
    ],
    rowNum:10,
    rowList:[10,20,30,100,1000],
    pager:'#pager',
    sortname:'date',
    viewrecords:true,
    sortorder:'desc',
    caption:'Stock Closing Price'
});
$('#tabulardata').jqGrid('navGrid','#pager',{
    edit:false,
    add:false,
    del:false,
    search:false,
    refresh:false,
    pgbuttons:false,
    pgtext:null,
    viewrecords:false,
    loadtext: "Loading..."
});

/*
$('#tabulardata').jqGrid({
    datatype: 'local',
    colNames: ['id', 'name'],
    colModel: [
        { name: 'id', index: 'id', width: 100 },
        { name: 'name', index: 'name', width: 300 }
    ],
    rowNum: 9999,
    sortname: 'name',
    viewrecords: true,
    sortorder: 'asc',
    data: [{"id":"924c18a4-cad6-4b6a-97ef-f9ca61614530","name":"Pathway 1"},{"id":"54897f40-49ab-4abd-acac-6047006c7cc7","name":"Pathway 2"},{"id":"61542c48-102f-4d8e-ba9f-c24c64a20d28","name":"Pathway 3"},{"id":"c4ca9575-7353-4c18-b38a-33b383fcd8b2","name":"Pathway 4"}]
});*/
