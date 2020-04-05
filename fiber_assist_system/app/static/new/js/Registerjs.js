window.onload = init

function init(){
	hides();
}

function hides(){
	$(function(){	
		$('#divchanged1').hide();
		$('#divchanged2').hide(); 
        $("#chooseid").change(function(){
			var a = $(this).children('option:selected').val()
			if(a == '-1') {	
				$('#divchanged1').hide();
				$('#divchanged2').hide();
			}
			if(a == '0') {
				$('#divchanged1').show();
				$('#divchanged2').hide(); 
			}
			if(a == '1') {
				$('#divchanged1').hide();
				$('#divchanged2').hide();
			}
			if(a == '2') {
				$('#divchanged2').show();
				$('#divchanged1').hide(); 
			}
		});
	});
}
