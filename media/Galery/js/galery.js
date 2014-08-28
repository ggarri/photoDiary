function init(){
	main_menu('.main-menu', '.myGalery');

	// Initial message widget content
	$('#messages').messages();
	$('.info-btn').popover({'placement':'right'})

	var bounds;
	var map = $(".map_canvas").myMap({
		contextGalery: '.galery',
		editMode: false,
		searchDiv: '.searcher',
		markerClick: function(widget, marker, vent){
			$.each(widget.markersArray, function(key, item){
				item.setIcon(widget.icons['red']);
			});
			marker.setIcon(widget.icons['blue']);
			console.log(marker, marker.zIndex);
			http_request('getCoordinatePhotos', 'GET', {coordinateId : marker.zIndex}, function(data){
				$('.tumbPhoto .photo',$('.map-galery')).removeAttr('selected');
				$.each(data, function(key,item){
					$('.tumbPhoto[id='+item["id"]+'] .photo',$('.map-galery')).attr('selected', 'selected');
				});
			});
		},
		boundChange: function(event){ // When bound changed, the galery is updated
			$('.map-galery').myGalery('updateGalery', '.map-galery');			
		},
		callback: function(widget){
			$('.map-galery').myGalery({
				serviceGet: {
					service: 'getBoundPhotos',
					params_callback: function(){ // Get the current bounds in the map
						bounds = widget.map.getBounds();
						return {
							ca_b : bounds.getNorthEast().lat(),
							ca_j : bounds.getSouthWest().lat(),
							ea_b : bounds.getNorthEast().lng(),
							ea_j : bounds.getSouthWest().lng()
						}
					},
					params:{
						view: 'common/galery.html'	
					}
				},
				context: '#main-area',
				size: 90,
				progressBar: false,
				clickPhoto: function(canvas, event){
					var coordinateId = $(canvas).parent().attr('coordinateId');
					var photoId = $(canvas).parent().attr('id');
					$('.tumbPhoto .photo',$('.map-galery')).removeAttr('selected');
					widget.selectMarker(coordinateId);
					var data = {
						id : photoId,
						view : 'Galery/photoInfo.html'
					};
					http_request('getPhotoById', 'GET', data, function(data){
						var context = '.photo-info';
						// If it has been a error
						if(data == 'object'){
							$('messages').messages('show', data);
							return;
						}
						$(context).html(data);
						$('.tumbPhoto', $(context)).myPhoto();
						$('.save', $(context)).unbind('click').click(function(){
							var info = {
								id: $('.id', $(context)).val(),
								comment: $('.comment', $(context)).val(),
								title: $('.title', $(context)).html()
							}
							http_request('setPhotoById', 'POST', info, function(data){
								$('#messages').messages('show', data);
							});
						});
					});
				}
			});
		}
	});
}