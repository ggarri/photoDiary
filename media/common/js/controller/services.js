var services = {
	paths : {
		getUserForm: 'getUserForm',
		setNewUser: 'setNewUser',
		login: 'login',
		getRegisterForm: 'getRegisterForm',
		photos: {
			getTmpPhotos : 'getTmpPhotos',
			addTmpPhoto: 'addTmpPhoto',
			delTmpPhoto: 'delTmpPhoto',
			getBoundPhotos: 'getBoundPhotos',
			getPhotoById: 'getPhotoById',
			setPhotoById: 'setPhotoById'
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
			acceptRequest: 'acceptRequest',
			rejectRequest: 'rejectRequest',
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