//GLOBAL VARIABLES
var lastQuery = {ticker:"",url:""};
//AJAX FORM REQUEST
    $(document).ready(function() {
        var options = {
            target: '#ShowImage',
            beforeSubmit: checkFormValues,
            success: showResponse,
            error: ajaxErrorHandler
        };
        $("#GenImgForm").ajaxForm(options);
        $("#tabularsection").hide();

        return false;
    });

    //VALIDATION & UI TRANSITION
    function checkFormValues(formData,jqForm,options){
        var formIsValid = true;
        //$('#errorDisplay').hide();

        if(($('#tickerIn').val().length === 0)||($('#start_date').val().length === 0) || ($('#end_date').val().length === 0) ){
            alert("Please fill in all required fields.");
            return false;
        }
        //Else all is well, also update the jqGrid with new data
        var start = $('#start_date').val().split('/').join('-');
        var end = $('#end_date').val().split('/').join('-');
        var newUrl = "/generate-data/"+$('#tickerIn').val()+".json?start="+start+"&end="+end;
        lastQuery.ticker = $('#tickerIn').val();
        lastQuery.url = newUrl;
        $("#tabulardata").jqGrid().setGridParam({url : newUrl}).trigger("reloadGrid");
        $("#tabularsection").fadeIn('slow');
        $('#NoImageText').hide();
        $('#ShowImage').hide();
        $('.imageFrame').css('outline','none');
        return true;
    }
    //SUCCESS HANDLER
    function showResponse(responseText, statusText, xhr, $form)  {
        $('#ShowImage').fadeIn('slow');//Show our image
        return true;
    }
    //ERROR HANDLER
    function ajaxErrorHandler(request, status, error){
        console.log("Error passed to jq.");
        if(!$('.alert')[0]){
            $('#ImageFrame').prepend('<div class="alert alert-danger fade in"><b>Error!</b> Invalid ticker or date range specified.<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>');
        }
        //Else there is already an error being displayed
        $('#NoImageText').fadeIn('slow');

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
    pgbuttons:false,
    pgtext:null,
    sortname:'date',
    viewrecords:false,
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
$("#tabulardata").jqGrid('navButtonAdd','#pager',{
       caption:"Export to CSV",
       onClickButton : function () {
           $("#tabulardata").jqGrid('excelExport',{"url":null});
       }
});
//END TABULAR STOCK DATA
//EXPORT TO CSV
$('#exportBtn').click(function(){
    alert(tickerIn);
    if(lastQuery.url !== ""){
        $("#tabulardata").jqGrid('excelExport',{"url":lastQuery.url});
    }
    else{
        alert("Please perform a query first.");
    }
});
