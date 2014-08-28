var http_request = function(service, type, args, callback){
	$.ajax({
		url: services.services[service],
        type: type,
        async: false,
        cache: false,
        timeout: 30000,
        data: args,
        contentType: 'application/json;charset=UTF-8',
        error: function (jsonerror) {
            console.error(jsonerror);
            return null;
        },
		success: function(data){
			callback(data);
		}
	});
}

// function jsonStringify(obj) {
//     try
//     {
//             return JSON.stringify(obj);
//     }
//     catch(err)
//     {
//             var t = typeof (obj);
//         if (t != "object" || obj === null) {
//             // simple data type  
//             if (t == "string") obj = '"'+obj+'"';
//             return String(obj);
//         }
//         else {
//             // recurse array or object  
//             var n, v, json = [], arr = (obj && obj.constructor == Array);
//             for (n in obj) {
//                 v = obj[n]; t = typeof(v);
//                 if (t == "string") v = '"'+v+'"';
//                 else if (t == "object" && v !== null) v = jsonStringify(v);
//                 json.push((arr ? "" : '"' + n + '":') + String(v));
//             }
//             return (arr ? "[" : "{") + String(json) + (arr ? "]" : "}");
//         }
//     }
// }