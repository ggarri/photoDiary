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
			get_coordinates: 'get_coordinates',
			get_coordinate_by_id: 'get_coordinate_by_id',
			set_coordinate: 'set_coordinate',
			set_coordinate_photo: 'set_coordinate_photo',
			set_coordinate_title: 'set_coordinate_title',
			del_coordinate_by_id: 'del_coordinate_by_id',
			del_coordinate_photo: 'del_coordinate_photo',
			get_coordinate_photos: 'get_coordinate_photos',
			get_coordinatesearch: 'get_coordinatesearch'
		},
		myPeople: {
			search_by_name: 'search_by_name',
			add_friend: 'add_friend',
			del_friend: 'del_friend',
			get_friends: 'get_friends',
			get_requests: 'get_requests',
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