$(document).ready(function() {
	(function( $ ) {
		$.widget( "photoDiary.myGalery", {
			options: {
				getParamsByFunc: function(){ return {}; },
				serviceGet: { service:'', params:'', params_callback: function(){ return {}; } },
				serviceDel: { service:'', params:''},
				serviceAdd: { service:'', params:''},
				insertItemModes: [],
				clickPhoto: function(canvas, e){},
				draggable: true,
				droppableArea: '',
				reducePercentage: 1.0
			},

			_sections: {
			    selectorHTML: '<section class="file-icon" rel="popover" ' + 
			    'data-content="Click here to upload your photos in this temporal gallery, then drag them to drop area of marker selected."'+
			    'data-original-title="Multiple file uploader"></section>',
			    iframeHTML: '<iframe class="upload_frame" name="upload_frame" height="0" width="0" frameborder="0" scrolling="yes"></iframe>',
			    formHTML: '<form class="uploader_form" method="post" action="" enctype="multipart/form-data"  target="upload_frame">'+
					'<input type="file" multiple="multiple" name="files" id="upload_field" accept="jpg|png|jpge"/>'+
					'</form>'

			},

			_init: function() {
				var widget = this;

				var display = document.createElement('section');
				$(display).addClass('display');


				/************************************
	 			// CREATING UPLOADING AREA
	 			************************************/

	 			var uploader = document.createElement('section');
	 			$(uploader).addClass('uploader');

	 			/************************************
	 			// FILE UPLOADER BY IFRAME
	 			************************************/

	 			if($P.in_array('selector', widget.options.insertItemModes)){
	 				var serviceAdd = services.services[widget.options.serviceAdd['service']];

	 				// Adding HTML requiered for
	 				$(uploader).append(widget._sections['selectorHTML']);
	 				$(uploader).append(widget._sections['iframeHTML']);
			 		$(uploader).append(widget._sections['formHTML']);

			 		$('.uploader_form', $(uploader)).attr('action', serviceAdd);

					$(".upload_frame", $(uploader)).load(function(event) {
						$.post(serviceAdd, null, function(attachment){
					       widget.updateGalery(display);
					    },'json');
					});

					$("#upload_field", $(uploader)).unbind('change').change(function(){
						// function gen_uuid() {
				  //   	    var uuid = ""
					 //        for (var i=0; i < 32; i++) {
					 //            uuid += Math.floor(Math.random() * 16).toString(16);
					 //        }
					 //        return uuid
					 //    }
					 //    var uuid = gen_uuid();

		    //         	var freq = 1000; 

			   //          function update_progress_info() {
			   //              $.getJSON('/photos/upload_progress/', {'X-Progress-ID': uuid}, function(data, status){
			   //              	console.log(data);
			   //                  if (data) {
			   //                  	console.log(data);
			   //                  }
			   //                  window.setTimeout(update_progress_info, freq);
			   //              });
			   //          };
			   //          // window.setTimeout(update_progress_info, freq);

						
						// var action = $('.uploader_form', $(uploader)).attr('action');
						// $('.uploader_form', $(uploader)).attr('action', action +'?X-Progress-ID='+uuid);

						$('.uploader_form', $(uploader)).submit();
						// var action = $('.uploader_form', $(uploader)).attr('action',action);
					});

					// Links events to the widget.
					$('.file-icon', $(uploader)).click(function(){
				   		$("#upload_field").trigger('click')
				   	});
	 			} 

				/************************************
	 			// DROPABLE AREA
	 			************************************/
	 			if($P.in_array('drop-area', widget.options.insertItemModes)){
	 			// 	var dropArea = document.createElement('section');
					// $(dropArea).addClass('drop-area');
	 				$(display).droppable({
		                accept: function(c){
		                	// Checks if the ui-photo belongs to droppable areas
		                	var correct = false;
		                	$.each(widget.options.droppableArea, function(key, area){
		                		if( $P.in_array(c[0], $('.tumbPhoto', $(area)))){
			                		correct = true;
			                	}
		                	});		            	
		                	return correct;
		                },
		                // hoverClass: "dropElhover",
		                drop: function(ev, ui) {
		                	var params = $P.array_merge(widget.options.serviceAdd['params'], {'id': ui.draggable[0]['id']});

		                	http_request(widget.options.serviceAdd['service'], 'POST', params, function(data){
		                		$('#messages').messages('display', {type:true, description:'Photo moved correctly'});
		                		widget.updateGalery(display);
		                		$.each(widget.options.droppableArea, function(key, area){
		                			$(area).myGalery('updateGalery' ,$('.display', $(area) ) );
		                		});
		                	});
		                }
					});
					// $(uploader).append(dropArea);
	 			}

	 			/************************************
	 			// INSERTING SECTIONS IN EACH CONTEXT
	 			************************************/

		 		widget.element.each(function(key, content){
		 			// Creating the template for every galery components
		 			$(content).empty();
		 			$(content).addClass('ui-galery');
		 			if($P.in_array('selector', widget.options.insertItemModes)){
		 				$(content).append(uploader);
		 			}
		 			$(content).append(display);
		 			$('.file-icon', $(content)).popover({'placement':'left'});
		 			widget.updateGalery(display);
		 		});
			},

			updateGalery: function(content){
				var widget = this;
				var hasBin = false;
				var params;
				
				// Just if there is a delete service is include bin button in the photos
				if(!$P.empty(widget.options.serviceDel['service'])){
					hasBin = true;
				}
				
				if(widget.options.serviceGet['params_callback']){
					params = $P.array_merge(widget.options.serviceGet['params'], widget.options.serviceGet['params_callback']());	
				} else{
					params = widget.options.serviceGet['params'];
				}

				http_request(widget.options.serviceGet['service'], 'GET', params, function(data){
					// Data returns all the picture rendered in a view, then this is inserted in the display area.
					$(content).html(data);
					// Each picture(canvas) is declare as my own widget to make its manipulatin easier.
					$('.tumbPhoto', $(content)).each(function(key, item){
						$(item).myPhoto({
							draggable: widget.options.draggable,
							click: widget.options.clickPhoto,
							reducePercentage: widget.options.reducePercentage,
							droppableArea: widget.options.droppableArea,
							hasBin: hasBin
						});
					});
					
					// Binds the deleting service
					$('canvas.bin', $(content)).each(function(key, bin){
			 			$(bin).unbind('click').bind('click', function(){
			 				var id = $(this).parent().attr('id');
			 				var params = $P.array_merge(widget.options.serviceDel['params'], { id: id });
			 				http_request(widget.options.serviceDel['service'], 'POST', params, function(data){
			 					$('#messages').messages('display', {type:true, description:'Photo removed correctly'});
			 					widget.updateGalery(content);
			 				});
			 			});
					});
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
});
