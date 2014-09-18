// Widget
$(document).ready(function() {
	(function( $ ) {
	  $.widget( "photoDiary.myMap", {
		    // These options will be used as defaults
		    options: {
		    	mapParams: {
					zoom: 12,
					streetViewControl: false,
					center: new google.maps.LatLng(40.43545,-3.69278),
					mapTypeId: google.maps.MapTypeId.TERRAIN,
				},
				mapClick: function(widget, event){},
				markerClick: function(widget, marker, event){},
				markerDragend: function(widget, marker, event){},
				boundChange: function(event){},
				domready: function(event){},
				markerDraggable: false,
				geoLocation: false,
				contextGalery: '',
				searchDiv: '',
				callback: function(widget){}
		    },


		 	_init: function() {
		 		var widget = this;
		 		var mapDiv = widget.element[0];
		 		var update_timeout = null;

				widget.map = new google.maps.Map(mapDiv, widget.options.mapParams);

				// Set user current position
				if(widget.options.geoLocation){
					if (navigator.geolocation) {
			 			var success = function(position){
			 				widget.map.setCenter(new google.maps.LatLng(position.coords.latitude, position.coords.longitude), 13);
			 			};
			 			var error = function(error){
			 				alert('error: ' + msg);
			 			}
						navigator.geolocation.getCurrentPosition(success, error);
					} else {
						alert('geolocation not supported');
					}
				}

				// Adding click event by paramenters
				google.maps.event.addListener(widget.map, 'click', function(event){
					// When infowindow is open
					if (widget.infowindow.getMap()){
						widget.infowindow.close();
						widget.unselectMarker();
					} else{ // When infowindow is close
						update_timeout = setTimeout(function(){
					        widget.options.mapClick(widget, event);
					    }, 200);
					}
				});

				google.maps.event.addListener(widget.map, 'dblclick', function(event){
					clearTimeout(update_timeout);
				});

				// Events to change bounds(change Zoom)
				google.maps.event.addListener(widget.map, 'bounds_changed', function(event){
				    widget.options.boundChange(event);
				});
				// It waits until map is displayed totally
				google.maps.event.addListenerOnce(widget.map, 'idle', function(){
				    widget.options.callback(widget);
				});

				// Create a info window to display marker info
				widget.infowindow = new google.maps.InfoWindow();

				google.maps.event.addListener(widget.infowindow, 'domready', function(){
					widget.options.domready(widget);
				});

				google.maps.event.addListener(widget.infowindow, 'closeclick', function(){
					widget.unselectMarker();
				});

				/**************************************
					AUTOCOMPLETE PREDICTIBLE
				**************************************/
				$('input', $(widget.options.searchDiv)).attr('id','searcher');
				widget.autocomplete = new google.maps.places.Autocomplete(document.getElementById('searcher'));
				google.maps.event.addListener(widget.autocomplete, 'place_changed', function(){
					var place = widget.autocomplete.getPlace();
					var location = place.geometry.location;
					widget.map.setOptions({
						zoom: 14,
						center: location
					});
				});


			    widget.coordinates();
		 	},

		    map: null,
		    autocomplete: null,
		    infowindow: null,
		    selectedMarker: null,
		    markersArray: [],
		    icons: {
		    	blue : '/media/common/resources/blue-dot.png',	
		    	red : '/media/common/resources/red-dot.png'
		    },

		    coordinates: function(args){
				var widget = this;
				http_request('get_coordinates', 'GET', {}, function(data){
					if(!$P.empty(data)){
						$.each(data, function(key, item){
							widget.addMarker({
								location : new google.maps.LatLng(item.lat, item.lng),
								id: item.id,
								title: item.title
							});
						});
					}
				});
			},

		    addMarker: function (args) {
		    	if($P.empty(args)){
		    		return;
		    	}
		    	var widget = this;
				var marker = new google.maps.Marker({
					position: args['location'],
					map: widget.map,
					draggable: false,
					zIndex: id = args['id'],
					title: args['title'],
					icon: widget.icons['red'],
					animation: google.maps.Animation.DROP,
				});
				
				marker.draggable = widget.options.markerDraggable;

				google.maps.event.addListener(marker, 'click', function(event){
					widget.infowindow.close();
					widget.options.markerClick(widget, marker, event);
					widget.infowindow.open(widget.map, marker);
				});

				google.maps.event.addListener(marker, "dragend", function(event){
					widget.options.markerDragend(widget, marker, event);
				});

			  	var index = widget.markersArray.push(marker);
			  	return marker;
			},

			delMarker: function(id){
				var widget = this;
				$.each(widget.markersArray, function(key, item){
					if(item.getZIndex() == id){
						widget.selectedMarker = null;
						item.setMap(null);
					}
				});
			},

			unselectMarker: function(){
				var widget = this;
				$(widget.options.contextGalery).empty();
				widget.selectMarker(undefined);
			},

			selectMarker: function(id){
				var widget = this;
				$.each(widget.markersArray, function(key, item){
					if(item.getZIndex() == id){
						widget.selectedMarker = item;
						item.setIcon(widget.icons['blue']);
					} else{
						item.setIcon(widget.icons['red']);	
					}
				});
			},

			getBounds: function(){
				return this.map.getBounds();
			},

		 	// Set up the widget
		    _create: function() {
		    	// console.log('create ', this.options)
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
