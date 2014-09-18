var services = {
	paths : {
		getUserForm: 'getUserForm',
		setNewUser: 'setNewUser',
		login: 'login',
		getRegisterForm: 'getRegisterForm',
		photos: {
			get_tmp_photos : 'get_tmp_photos',
			add_tmp_photo: 'add_tmp_photo',
			del_tmp_photo: 'del_tmp_photo',
			get_bound_photos: 'get_bound_photos',
			get_photo_by_id: 'get_photo_by_id',
			set_photo_by_id: 'set_photo_by_id'
		},
		map : {
			getCoordinates: 'getCoordinates',
			getCoordinateById: 'getCoordinateById',
			setCoordinate: 'setCoordinate',
			setCoordinatePhoto: 'setCoordinatePhoto',
			setCoordinateTitle: 'setCoordinateTitle',
			delCoordinateById: 'delCoordinateById',
			delCoordinatePhoto: 'delCoordinatePhoto',
			getCoordinatePhotos: 'getCoordinatePhotos',
			getCoordinateSearch: 'getCoordinateSearch'
		},
		myPeople: {
			searchByName: 'searchByName',
			addFriend: 'addFriend',
			delFriend: 'delFriend',
			getFriends: 'getFriends',
			getRequests: 'getRequests',
			accept_request: 'accept_request',
			reject_request: 'reject_request',
		}

	},
	_init : function() {
		for (key in this.paths) {
			var value = this.paths[key];
			if(typeof(value) == 'string'){
				this.services[key] = value;
			} else{
				for (sKey in value) {
					var sValue = value[sKey];
					this.services[sKey] = '/' + key + '/' + sValue;
				}
			}
		}
	},
	/**
	 * Just to store services in their paths, don't delete
	 */
	services : {}
};