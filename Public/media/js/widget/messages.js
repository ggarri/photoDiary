(function( $ ) {
  $.widget( "photoDiary.messages", {
	    // These options will be used as defaults
	    options: {
	    	time: 1.5,
	    	data: {},
	    	callback: function(data){ }
	    },

	 	_init: function() {
	 		var widget = this;
	 		widget._top = parseInt($('#messages').css("top"));
	 		window.onscroll = function (oEvent) {
			  $(window).bind('scroll', function(){ 
			  	$('#messages').css("top", $(window).scrollTop() + widget._top);
			  });
			}
	 	},

	 	_top : 40,
	 	_display: false,

	 	_form : function(args){
	 		if( typeof(args['description']) == 'object'){ // If there are several messages
 				$.each(args['description'], function(key,item){
 					var _event = 'keypress';
 					var obj = $('#id_'+key, $(args['context']));
 					if(obj != undefined){ // There is input item with this name in the view currently
 						$(obj).addClass('warning');
 						$('span.warning', $(obj).parent()).html(item[0]);
 						$(obj).unbind(_event).bind(_event, function(){
 							$(obj).removeClass('warning');
 							$('span.warning', $(obj).parent()).empty();
 							$(this).unbind(_event); // Just one first time
 						});
 					}
 				});
 			}
	 	},

	 	_processVO: function(args){
	 		var widget = this;
	 		var content = document.createElement('div');
	 		// If the format JSON doesn't have a basic structure, then this is incorrect
	 		if(!'type' in args || !'description' in args || !'context' in args){
	 			return;
	 		}

	 		if(args['type'] == true){ // Success outcome
	 			$(content).addClass('success');
	 		} else if(args['type'] == false){ // Error outcome
	 			$(content).addClass('error');	
	 		} else if(args['type'] == 'error_form'){ // Error messages on form
	 			widget._form(args);
	 			return;
	 		}
 			
 			if( typeof(args['description']) == 'object'){ // If there are several messages
 				var ul = document.createElement('ul');
 				// There is not a input item with this name in the view currently. Then, the message is show in popover
 				$.each(args['description'], function(key,item){
 					var obj = $('#id_'+key, $(args['context']));
					var li = document.createElement('li');
 					var b = document.createElement('b');
 					$(b).html(key +': '); // Name of parameter for the message
 					$(li).append(b);
 					$(li).append(item[0]); // Display just the first message
 					$(ul).append(li);
 				});
 				$(content).append(ul);
 			} else{ // Just a simple message
 				$(content).html(args['description']);
 			}

 			return content;
	 	},

	 	show: function(args) {
	 		var widget = this;
	 		var context; // Default value is HTML global content
	 		('context' in args) ? context = args['context'] : context = 'html';
	 		args = $P.array_merge(args, {'context':context});

	 		var content = widget._processVO(args);
	 		
	 		widget.element.each(function(key, item){
	 			$(item).empty(); // Clear container
	 			if(!$P.empty(content)){
	 				$(item).append(content); // Adds the content from ARGS
	 				if(!widget._display){ // Flag to manage message trafic
			 			$(item).show('blind',{}, 'fast', function(){
			 				widget._display = true;
			 				setTimeout(function(){
			 					$(item).hide('blind', {}, 'fast', function(){
			 						widget._display = false;
			 					});
			 				}, widget.options.time*1000); // From milliseconds to seconds
			 			});
			 		}
		 		}
	 		});
	 	},

	    // Set up the widget
	    _create: function() {
	    	
	    },
	 
	    // Use the _setOption method to respond to changes to options
	    _setOption: function( key, value ) {
	      switch( key ) {
	        case "clear":
	          // handle changes to clear option
	        break;
	    }
	 
	      // In jQuery UI 1.8, you have to manually invoke the _setOption method from the base widget
	      $.Widget.prototype._setOption.apply( this, arguments );
	      // In jQuery UI 1.9 and above, you use the _super method instead
	      //this._super( "_setOption", key, value );
	    },
	 
	    // Use the destroy method to clean up any modifications your widget has made to the DOM
	    destroy: function() {
	      // In jQuery UI 1.8, you must invoke the destroy method from the base widget
	      $.Widget.prototype.destroy.call( this );
	      // In jQuery UI 1.9 and above, you would define _destroy instead of destroy and not call the base method
	    },

		
	});	
}(jQuery) );
