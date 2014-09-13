
/* GLOBAL VARIABLES */
var TEMPLATE_DIRS;
var $P;

$(document).ready(function() {
	$P = new PHP_JS()
	TEMPLATE_DIRS = 'templates/';
	services._init();
	init();
});