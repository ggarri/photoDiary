$(document).ready(function() {
	(function( $ ) {
		$.widget( "photoDiary.myPhoto", {
			options: {
				click: function(photo, e){},
				draggable: true,
				reducePercentage: 1.0,
				droppableArea: [],
				hasBin: false
			},

			_init: function() {
				var widget = this;
		 		widget.element.each(function(key, container){
		 			$(container).addClass('ui-photo');
		 			var photo = $('.photo', $(container));

		 			widget.src = $(photo).attr('src');
		 			max_width = parseInt($(container).css('width'));
		 			max_height = parseInt($(container).css('height'));

		 			// Keeping aspect ratio of photo
		 			old_width = $(photo).attr('width');
		 			old_height = $(photo).attr('height');
		 			if(old_height > old_width){
		 				new_width = (old_width/old_height * max_height) * widget.options.reducePercentage;
		 				new_height= max_height * widget.options.reducePercentage;	
		 			} else{
		 				new_width = max_width * widget.options.reducePercentage;
		 				new_height= (old_height/old_width * max_width) * widget.options.reducePercentage;	
		 			}
		 			$(photo).attr('width',  new_width);
		 			$(photo).attr('height', new_height);
		 			if(new_width > max_width){
		 				$(container).css('width',  new_width);
		 			}
		 			if(new_height > max_height){
		 				$(container).css('height',  new_height);
		 			}

		 			// console.log(max_width, max_height);
		 			// console.log(old_width, old_height);
		 			// console.log(new_width, new_height);
		 			// Putting on the bin in the ui-photo
		 			var bin = $('.bin', $(container));
		 			if(widget.options.hasBin){
			 			var bin_width = parseInt($(bin).css('width'));
			 			var bin_height = parseInt($(bin).css('height'));
			 			var offset = $(photo).offset();
			 			$(bin).css('top',-new_height);
			 			$(bin).css('left',new_width-bin_width);	
			 			// $(bin).css('top',0);
			 			// $(bin).css('left',0);	
		 			} else{
		 				$(bin).remove();
		 			}

		 			// Declare photo as draggable
		 			if(widget.options.draggable){
						$(container).attr('draggable','true');
						$(container).draggable({
							helper: 'clone',
							start: function(event, ui) {
								// Show the drop-area which accept from this galery its ui-photos.
								// $.each(widget.options.droppableArea, function(key, area){
								// 	if(!$P.empty($('.file-icon', $(area)))){
								// 		$('.file-icon', $(area)).hide();
				    //             		$('.drop-area', $(area)).show();
				    //             	}
			     //            		// $('.uploader', $(photo).closest('.ui-galery')).hide();
								// });
							},
							stop: function(event, ui) {
								// $.each(widget.options.droppableArea, function(key, area){
								// 	if(!$P.empty($('.file-icon', $(area)))){
								// 		$('.file-icon', $(area)).show();
				    //             		$('.drop-area', $(area)).hide();
				    //             	}
			     //            		// $('.uploader', $(photo).closest('.ui-galery')).show();
								// });
							}
						});
					}
					$(container).unbind('click').click(function(e){
						widget.options.click($(photo), e);
					});
		 			
		 		});
			},

			// Set up the widget
		    _create: function() {
		    	
		    },

		    src: 'unknown',
		    selected: false,

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
});
