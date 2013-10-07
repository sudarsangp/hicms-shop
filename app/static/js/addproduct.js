//console.log("test");
$(document).ready(function(){
        $('#manu-form').hide();
        $('#cat-form').hide();
        
        //console.log("inside test");
        
        $('#manu-id').change(function(){

                var manufacturerVal = $('#manu-id option:selected').text();
                  
                if(manufacturerVal == "None"){
                	$('#manu-form').show();
                        $("label[for=manufacturerForm-csrf_token]").hide();
                
                }
                             
                else{
                        $('#manu-form').hide();
                }
        });
        
                $('#cat-id').change(function(){

                var categoryVal = $('#cat-id option:selected').text();
                
                if(categoryVal == "None"){
                	$('#cat-form').show();
                        $("label[for=categoryForm-csrf_token]").hide();
                
                }
                             
                else{
                        $('#cat-form').hide();
                }
        });
        
        
});