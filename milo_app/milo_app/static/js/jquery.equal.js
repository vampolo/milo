jQuery(document).ready(function($) {
	function sortNumber(a,b)    {
	    return a - b;
	}
	
	function maxHeight() {
	    var heights = new Array();
	    $('div.gallery-item').each(function(){
	        $(this).css('height', 'auto');
	        heights.push($(this).height());
	        heights = heights.sort(sortNumber).reverse();
	        $(this).css('height', heights[0]);
	    });        
	}
	
	$(document).ready(function() {
	    maxHeight();
	})
	
	$(window).resize(maxHeight);
});