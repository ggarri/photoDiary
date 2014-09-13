/**

 * Main render function
 * @param view path to file with the template
 * @param container css path to the element where the template will be renderized
 * @param data data to fill the template
 * @param pre_callback callback to modify the data before the renderization
 * @param post_callback callback to modify the html output before appending it to the iface
 * @return
 */
(function( $ ) {
	$.widget( "photoDiary.render", {
	    // These options will be used as defaults
	    options: { 
	    	withAppend: false,
			view: '', 
			callback: function() {
				
			}
	    },

	 	_init: function() {
	    	var widget = this;
	    	$.get(this.options.view, function(html) {
				widget.element.each(function(key, element) {
		    		if (widget.options.withAppend) {
		    			$(element).append(html);
		    		} else {
		    			$(element).empty().append(html);
		    		}
				});
	    		widget.options.callback();
	    	});		
	 	},
	});
}(jQuery) );
