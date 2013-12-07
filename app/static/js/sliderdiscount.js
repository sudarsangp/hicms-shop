$(function() {
    $( "#slider-range-min" ).slider({
      range: "min",
      value: 10,
      min: 0,
      max: 50,
      slide: function( event, ui ) {
        $( "#discount" ).val(  ui.value );
      }
    });
    $( "#discount" ).val(  $( "#slider-range-min" ).slider( "value" )  );
  });