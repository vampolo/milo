
	function panel_down(url, text){
		var content = text;
		var url_address = url;
		$('#communication-panel-content span').replaceWith('<span>'+content+'</span>');
		$('#agree_button').attr('href', url_address);
		$('#communication-panel').slideDown('slow');
	}
	
	function panel_down_wizard(url, text){
		var content = text;
		var url_address = url;
		$('#communication-panel-content span').replaceWith('<span>'+content+'</span>');
		$('#agree_button').attr('href', url_address);
		$('#communication-panel').slideDown('slow');
	}
		
	function panel_up(){
		$('#communication-panel').slideUp('slow');
	}
	
	function help(){
		$().slideDown('fast');
	}

$(document).ready(function() 
{	
	
	$('#filters_step2').accordion({ 
    header: 'div.title', 
    active: false, 
    clearStyle: true,
    collapsible: true
	});
	
	$("#Q1_yes").click(function () {
		$("#step5-rate1").show("fast", function () {
		/* use callee so don't have to name the function */
		$(this).next("#step5-rate1").show("fast", arguments.callee);
		$("#step5-question2").hide("fast");
		$("#step5-rate2").hide("fast");
		$("#video-container-wizard").hide("fast");
	});
	});

	$("#Q1_no").click(function () {
		$("#step5-rate1").hide("fast");
		$("#next-final-step").hide("fast");
		$("#step5-question2").show("fast", function () {
		/* use callee so don't have to name the function */
		$(this).next("#step5-question2").show("fast", arguments.callee);
	});
	});
	
	$(".rate-step5").click(function () {
		$("#next-final-step").show("fast", function () {
		/* use callee so don't have to name the function */
		$(this).next("#next-final-step").show("fast", arguments.callee);
	});
	});
	
	
	$("#Q2_no").click(function () {
		$("#next-final-step").hide("fast");
		$("#step5-rate2").hide("fast");
		$("#video-container-wizard").show("fast", function () {
		/* use callee so don't have to name the function */
		$(this).next("#video-container-wizard").show("fast", arguments.callee);
	});
	});
	
	$("#Q2_yes").click(function () {
		$("#step5-rate2").show("fast", function () {
		/* use callee so don't have to name the function */
		$(this).next("#step5-rate2").show("fast", arguments.callee);
		$("#video-container-wizard").hide("fast");
		$("#next-final-step").hide("fast");
	});
	});
	
	$("#step5-rate2").click(function () {
		$("#next-final-step").hide("fast");
		$("#video-container-wizard").show("fast", function () {
		/* use callee so don't have to name the function */
		$(this).next("#video-container-wizard").show("fast", arguments.callee);
	});
	});
	
	$( "#tabs" ).tabs();
	
	$('.help_button').click(function() {
		$('#rated-movies-help').slideDown('slow');
	});
	
	$('.hide_button').click(function() {
		$('#rated-movies-help').slideUp('slow');
	});
	
	//Sorting Tables
	
	$("#surveys_table").tablesorter(); 
    $("#users_table").tablesorter(); 
    
	//fix for chrome
	$("input[type='text']").bind('focus', function() {
	$(this).css('background-color', '#3E4852');
	});
	
	$("input[type='password']").bind('focus', function() {
	$(this).css('background-color', '#3E4852');
	});
	
	
	$(".options-style div").hover(function() {
	  $(this).next("span").animate({opacity: "show", top: "-15"}, "slow");
	}, function() {
	  $(this).next("span").animate({opacity: "hide", top: "-25"}, "fast");
	});
	
	$(".options-style div").draggable({
	helper:'clone',
	cursor: 'hand'
	});
	
	
	$(".my-profile-style").droppable(
		{
		accept: '.options-style div',
		drop: function(ev,ui){
			var droppedItem = $(ui.draggable);
			$(this).append(droppedItem);		
			}
			
		}
	);
	
	$(".my-profile-style div").draggable({
	helper:'clone'
	});
	
	$(".my-profile-liked-style div").draggable({
	helper:'clone'
	});
	
	$(".my-profile-liked-style").droppable(
		{
		accept: '.my-profile-disliked-style div',
		drop: function(ev,ui){
			var droppedItem = $(ui.draggable);
			$(this).append(droppedItem);		
			}
			
		}
	);
	
	$(".my-profile-disliked-style div").draggable({
	helper:'clone'
	});
	
	$(".my-profile-disliked-style").droppable(
		{
		accept: '.my-profile-liked-style div',
		drop: function(ev,ui){
			var droppedItem = $(ui.draggable);
			$(this).append(droppedItem);		
			}
			
		}
	);
	
	$(".trash").droppable(
		{
		accept: '.my-profile-style div, .my-profile-disliked-style div, .my-profile-liked-style div',
		drop: function(ev,ui){
				var removedItem = $(ui.draggable);
				if(removedItem.parent().attr('id') == 'my-genres')			
				$('#genre-options').append(removedItem);
				else{
					if(removedItem.parent().attr('id') == 'my-actors')			
					$('#actors-options').append(removedItem);
					else{
						if(removedItem.parent().attr('id') == 'my-directors')			
						$('#directors-options').append(removedItem);
						else{
						removedItem.remove();
						}
					}
				}
			}
		}
	);	
	
});
