// Widget
$(document).ready(function() {
	(function( $ ) {
	  $.widget( "photoDiary.selfAutocomplete", {
		    // These options will be used as defaults
		    options: {
		    	search_quantity: 10,
		    	service: null,
		    	params: {},
		    	accesor : [],
		    	label: '',
		    	key: '',
		    	pathLabel: '',
		    	pathKey: '',
		    	callback: function(data){ }
		    },

		 	_init: function() {
		 		var widget = this;
		    	if(! widget.options.service in http_request){
		    		return;
		    	}
	    		
		    	widget.element.each(function(key, item){
		    		$(item).autocomplete({
				        minLenght: 3,
				        delay: 300,
				        source: function(request, response) {
				                // var name = request.term;
				                // var params = $P.implode(', ', widget.options.params);
				                var service = widget.options.service;
				                var params = $P.array_merge(widget.options.params, {'name':request.term})
				                http_request(service, 'GET', params, function(result){
				                	widget._sourceCallback(result, response, widget);
				                });
				                // eval ('http_request[service](' 
				                // 		+ params + ', function(result){ widget._sourceCallback(result, response, widget);}'+
				                // 	');');

				        },
				        select: function (event, ui) {
				        	widget._selectCallBack(ui, widget, item);
				        	widget.options.callback(ui.item);
				        	return false;
				        }
			    	});
		    	});
		 	},


		 	_sourceCallback: function(result, response, widget) {
				result = widget._accesor(result, widget.options.accesor, false);
        		response(
        			$.map(result, function(item) {
        				var data = { 'item' : item}
        				if(!$P.empty(widget.options.label)){
        					data['label'] = widget._accesor(item, widget.options.label);
        				}
        				if(!$P.empty(widget.options.key)){
        					data['key'] = widget._accesor(item, widget.options.key);
        				}
        				return data;
        			})
        		);
        	},


        	_selectCallBack : function(ui, widget, item){
        		if(!$P.empty(widget.options.pathLabel)){
        			var label = $.trim(ui.item.label);
        			$(item).val(label);
        		}
        		if(!$P.empty(widget.options.pathKey)){
        			var key = ui.item.key;
        			$(item).siblings(widget.options.pathKey).val(key);	
        		}
        	},


        	_accesor: function(item, accesor){
        		var result = '';
        		if(typeof accesor == 'object'){
					var item2 = $.extend(true, {}, item);
					$.each(accesor, function(key, value){
						if(value in item2){
							item2 = item2[value];
						}
					});
					result = item2;
				} else{
					result = item[accesor];
				}
		 		return result;
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
