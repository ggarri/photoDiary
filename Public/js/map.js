function init(){
	main_menu('.main-menu', '.myMap');

	// Initial message widget content
	$('#messages').messages();
	$('.info-btn').popover({'placement': 'bottom'});

	var context = '.fields';
	var map = $(".map_canvas").myMap({
		contextGalery: '.marker-galery',
		markerDraggable: true,
		searchDiv: '.searcher',
		geoLocation: true,
		mapClick: function(widget, event){
			var data = {
				'lat': event.latLng.lat(),
				'lng': event.latLng.lng()
			};
			http_request('setCoordinate', 'POST', data, function(data){
				$('#messages').messages('show', {type:true, description:'Coordinate added correctly'});
				var marker = widget.addMarker({
					location : event.latLng,
					id: data['id']
				});
				google.maps.event.trigger(marker, 'click');
			});
		},
		markerDragend: function(widget, marker, event){
			console.log(marker);
			var data = {
				'lat': event.latLng.lat(),
				'lng': event.latLng.lng(),
				'id': marker.zIndex
			}
			http_request('setCoordinate', 'POST', data, function(data){
				$('#messages').messages('show', {type:true, description:'Marker spot updated correctly'});
			});
		},
		markerClick: function(widget, marker, event){
			var id = marker.zIndex;
			widget.selectMarker(id);
			http_request('getCoordinateById', 'GET', {'id':id, 'view':'Map/markerInfo.html'}, function(data){
				// Service returns a warning message
				if(typeof(data) == 'object'){ 
					$('#messages').messages('show', data);
					return;
				}

				widget.infowindow.setContent(data);	
				$(widget.options.contextGalery).myGalery({
					serviceAdd: {
						service: 'setCoordinatePhoto', 
						params:{
							coordinateId: id	
						}
					},
					serviceGet: {
						service: 'getCoordinatePhotos',
						params:{
							coordinateId: id,
							view: 'common/galery.html'
						}
					},
					serviceDel: {
						service: 'delCoordinatePhoto', 
						params:{
							coordinateId: id	
						}
					},
					droppableArea: ['.tmp-galery'],
					context: context,
					reducePercentage: 1,
					insertItemModes: ['drop-area']
				});
			});
		},
		domready: function(widget){
			var id = widget.selectedMarker.zIndex;
			var context = '.marker-info';
			$('button.del', $(context)).unbind('click').click(function(ev){
				ev.stopPropagation();
				http_request('delCoordinateById', 'POST', {'id': id}, function(data){
					$(widget.options.contextGalery).empty();
					$('#messages').messages('show', {type:true, description:'Coordinate deleted correctly'});
					widget.delMarker(data['id']);
					$(context).empty();
				});
			});
			$('.title[contentEditable="true"]', $(context)).blur(function(){
				var title = $(this).html();
				http_request('setCoordinateTitle', 'POST', {'id':id, 'title':title}, function(data){
					$('#messages').messages('show', {type:true, description:'Title saved correctly'});
				});
			});
		}
	});

	// Displaying temporal galery in the bottom
	$('.tmp-galery').myGalery({
		serviceAdd: {
			service: 'add_tmp_photo',
			params: {}
		},
		serviceGet:{
			service: 'get_tmp_photos',
			params: {view: 'common/galery.html'}
		} ,
		serviceDel: {
			service: 'del_tmp_photo',
			params: {}
		},
		context: '#main-area',
		droppableArea: ['.marker-galery'],
		reducePercentage: 1,
		insertItemModes: ['selector', 'drop-area']
	});
	
}