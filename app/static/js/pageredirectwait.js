$(document).ready(function() { 
    $('#submittrans').click(function() { 
        $.blockUI({ css: { 
            border: 'none', 
            padding: '15px', 
            backgroundColor: '#000', 
            '-webkit-border-radius': '10px', 
            '-moz-border-radius': '10px', 
            opacity: .5, 
            color: '#fff' 
        } , message: '<h1>Page Redirection in progress...</h1>' }); 
 
        //setTimeout($.unblockUI, 2000); 
    }); 
}); 
