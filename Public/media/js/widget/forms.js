// $(document).ready(function() {
// 	(function( $ ) {
// 		$.widget( "photoDiary.myForm", {
// 			options: {
// 				_type: '',
// 				_id: '',
// 				myMap: '',
// 				callback: function(){}
// 			},

// 			types : {
// 				Coordinate : function(id, myMap, context){
// 					var widget = this;
// 					http_request.get_coordinate_by_id(id, 'Map/marker_form.html', function(data){
// 						$(context).html(data);
// 						$('button.del', $(context)).unbind('click').click(function(ev){
// 							http_request.del_coordinate_by_id(id, function(data){
// 								myMap.delMarker(data['id']);
// 								$(context).empty()
// 							});
// 						});
// 						widget.options.callback();
// 					});
// 				}
// 			},

// 			_init: function() {
// 				var widget = this;
// 				var _type = widget.options._type;
// 				var _id = widget.options._id;
// 				var myMap = widget.options.myMap;
// 				console.log(myMap);
// 				if(_type in widget.types){
// 					$.each(widget.element, function(key, item){
// 						widget.types[_type](_id, myMap, item);
// 					});
// 				}
// 			},

// 			// Set up the widget
// 		    _create: function() {
		    	
// 		    },

// 			// Use the _setOption method to respond to changes to options
// 		    _setOption: function( key, value ) {
// 		      	switch( key ) {
// 			        case "clear":
// 			          // handle changes to clear option
// 			        break;
// 			    }
// 			    // In jQuery UI 1.8, you have to manually invoke the _setOption method from the base widget
// 			    $.Widget.prototype._setOption.apply( this, arguments );
// 			    // In jQuery UI 1.9 and above, you use the _super method instead
// 			    //this._super( "_setOption", key, value );
// 		    },
		 
// 		    // Use the destroy method to clean up any modifications your widget has made to the DOM
// 		    destroy: function() {
// 		      // In jQuery UI 1.8, you must invoke the destroy method from the base widget
// 		      $.Widget.prototype.destroy.call( this );
// 		      // In jQuery UI 1.9 and above, you would define _destroy instead of destroy and not call the base method
// 		    },
// 		});	
// 	}(jQuery) );
// });
