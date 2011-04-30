$(document).ready(function() 
{
	$( "#tabs" ).tabs();
	
	//fix for chrome
	$("input[type='text']").bind('focus', function() {
	$(this).css('background-color', '#3E4852');
	});
	
	$("input[type='password']").bind('focus', function() {
	$(this).css('background-color', '#3E4852');
	});
	
});
