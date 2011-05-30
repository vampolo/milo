$(document).ready(function() {

	$('ul.items>li.active>ul').slideDown();

	
	$(function() {
			   
		$('.items').click(clickFn);
		
	});
	
	function clickFn(e) {
		
		var $el = $(e.target);
		if (!$el.parent().children('ul').is(':visible')) {
			
			if ($el.parent().parent().is('ul.items')) {
				
				var $visibles=$('ul.items>li>ul:visible');
				if ($visibles.length>0){
					$visibles.slideUp('medium', function(){
						 $el.parent().children("ul").slideDown('slow');
						}
					);
				}
				else{
					$el.parent().children("ul").slideDown('slow');
				}

			}
			
		}
	
	}	

	function getEventTarget(e) {
		
		e = e || window.event;
		return e.target || e.srcElement;
		
	}

	$('.close').click(function() {
									 
		$(this).parents(".alert").animate({ opacity: 'hide' }, "slow");
		return false;
		
	});
	/*
	$('#survey_mng').click(function() {
											
		$('#milo_admin').removeClass('active');
		$(this).addClass('active');
		return false;
		
	});
	
	$('#milo_admin').click(function() {
											
		$('#survey_mng').removeClass('active');
		$(this).addClass('active');
		return false;
		
	});
	*/
	$('#tab1').click(function() {
									 
		$('#tab2').removeClass('active');
		$('#tab2_content').hide();
		$(this).addClass('active');
		$('#tab1_content').show();
		return false;
		
	});
	
	$('#tab2').click(function() {
									 
		$('#tab1').removeClass('active');
		$('#tab1_content').hide();
		$(this).addClass('active');
		$('#tab2_content').show();
		return false;
		
	});
	
	$(document).keyup(function(event) {
		if (event.keyCode == 13) {
			$(this).parents("form").submit();
			return false;
		}
	});
	
	$('.submit').click(function() {
									 
		$(this).parents("form").submit();
		return false;
		
	});
	
	$('.button').click(function(){
		$('#congrats').show('slow');
	});
	
});
