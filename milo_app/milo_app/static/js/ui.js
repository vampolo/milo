
	function panel_down(url, text){
	var content = text;
	var url_address = url;
	$('#communication-panel-content span').replaceWith('<span>'+content+'</span>');
	$('#agree_button').attr('href', url_address);
	$('#communication-panel').slideDown('slow');
	}
		
	function panel_up(){
	$('#communication-panel').slideUp('slow');
	}
	

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
	
	
	$(".trash").droppable(
		{
		accept: '.my-profile-style div',
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
