$(document).ready(function() 
{	
	$('.star').hover(function() {
		$(this).prevAll().andSelf().addClass('hover');
	},function() {
	$(this).siblings().andSelf().removeClass('hover');
	});
});
