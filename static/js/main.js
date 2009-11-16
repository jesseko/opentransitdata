// © Front Seat Management 2007

//*********** Utility functions ***********
		function getUrlParam( name, doEscapeCleaning, doAddressCleaning) {  
			name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");  
			var regexS = "[\\?&]"+name+"=([^&#]*)";  
			var regex = new RegExp( regexS );  
			var results = regex.exec( window.location.href );  
			if( results == null ) {   
				return "";  
			}
			else {
				var ret = results[1];
				if (doEscapeCleaning) ret = cleanEscapes(ret);		
				if (doAddressCleaning) ret = cleanAddress(ret);
				return ret;
			}
		}
		
		function cleanEscapes(address) {
			address = unescape(address);
			address = replaceAll( address, "+", " " );		
			return address;
		}
		
		function cleanAddress(address) {
			address = replaceAll( address, "&", " and " );
			//address = replaceAll( address, "#", " " );
			return address;
		}
		
		function replaceAll (strOrig, strTarget, strSubString) {
			var intIndexOfMatch = strOrig.indexOf( strTarget );
			while (intIndexOfMatch != -1) {
				strOrig = strOrig.replace( strTarget, strSubString )
				intIndexOfMatch = strOrig.indexOf( strTarget );
			}
			return strOrig;
		}
		
		function urlify(name, value, excludeNulls) {
			return (value == null && excludeNulls) ? "" : name + "=" + encodeURIComponent(value);
		}
		
		function sluggify(string) {
			string = replaceAll( string, " ", "-" );
			string = replaceAll( string, "'", "" );
			return string.toLowerCase();
		}
		
		// if str is not a string, returns ""
		function safeString(str, addLeadingSpace, addTrailingSpace){
			if (typeof str != "string")
				return "";
			if (addLeadingSpace) str = "x" + str;
			if (addTrailingSpace) str = str + "x";
			return str;
		}
		
		function trimURL(url) {
			var i = url.indexOf("://");
			if (i != -1)
				return url.substr(i+3);
		}
		
		function forEach(array, fn, objThis) {
			objThis = objThis || this;
			var len = array.length;
			for (var n = 0; n < len; n++) {
				var r = fn.call(objThis, array[n], n);
				if (r !== undefined)
					return r;
			}
		}
		
		function paramIsSet(param) {
			return (typeof param != "undefined");
		}

		function defaultIfNotSet(param, defaultVal) {
			return (typeof param != "undefined") ? param : defaultVal;
		}
		
		function trackEvent(control, action, label, value) {
			//alertThese("Track Event", control, action, label, value);
			if(pageTracker)
				pageTracker._trackEvent(control, action, label, value);
		}

		function trackNavigation(url, component, action, label) {
			if (component && action)
				trackEvent(component, action, safeString(label) );
			if (url)
				document.location = url;
		}
		
		function trackNavigationNewWindow(url, component, action, label) {
			if (component && action)
				trackEvent(component, action, safeString(label) );
			if (url)
				window.open( url, "newwin" );
		}
		function isNumeric(str){
			var numericExpression = /^[0-9]+$/;
			if (str.match(numericExpression))
				return true;
			return false;
		}

		function leadsWithNumber(str){
			var numericExpression = /^[0-9]+$/;
			if (str.substr(0,1).match(numericExpression))
				return true;
			return false;
		}
		
		function getLeadingNumber(str){
			if (!leadsWithNumber(str))
				return false
			var r = str.match(/[\d\.]+/g);
			if (r && r[0])
				return Number(r[0]);
			return false;
		}

		
//*********** JS OOP ******************
	Function.prototype.inheritsFrom = function( parentClassOrObject ){ 
		if ( parentClassOrObject.constructor == Function ) 
		{ 
			//Normal Inheritance 
			this.prototype = new parentClassOrObject;
			this.prototype.constructor = this;
			this.prototype.parent = parentClassOrObject.prototype;
		} 
		else 
		{ 
			//Pure Virtual Inheritance 
			this.prototype = parentClassOrObject;
			this.prototype.constructor = this;
			this.prototype.parent = parentClassOrObject;
		} 
		return this;
	}
	
//*********** String List ***************
	function StringList() {
		this.list = [];
		
		this.length = function() { return this.list.length }
		this.get = function(i) { return this.list[i] }
		this.indexOf = function(str) {
			for (var i = 0; i<this.list.length; i++){
				if (this.list[i] == str)
					return i;
			}
			return -1;
		}
		this.isInList = function(str) { return (this.indexOf(str) != -1) }
		this.addIfUnique = function(str) { if (!this.isInList(str)) this.list.push(str) }
		this.add = function(str) { this.list.push(str) }
	}
	
//*********** Selectively suppress errors ***********			
		function suppressErrors() {
			window.onerror = function(){return true;};
		}
		function restoreErrors() {
			window.onerror = function(){return false;};
		}
		
//*********** RESULT PROCESSING HELPERS ***********
		function sortAmenityResults( array, limit ) {
			if( array.length <= 1 )
				return array;
			array.sort( function (a,b) { return a.getDispDist() - b.getDispDist(); } );
			return dedupeAmenities(array, limit);		
		}
		
		
		function sortAmenityResultsSnapDist( array, limit ) {
			if( array.length <= 1 )
				return array;
			array.sort( function (a,b) { return a.getSnapDistance() - b.getSnapDistance(); } );
			return dedupeAmenities(array);			
		}
		
		function dedupeAmenities(array, limit){
			var dupeFree = [];
			dupeFree.push(array[0]);
			for (var i=1; i<array.length; i++) {
				if ( array[i].getName() != array[i-1].getName() && array[i].getStreetAddress() != array[i-1].getStreetAddress() )
					dupeFree.push(array[i]);
			}
			if ( !limit || limit >= dupeFree.length) { return dupeFree};
			return dupeFree.slice(0,limit);
		}
		
		function labelResults(newResults, resultSetIndex){
			for (var i=0; i<newResults.length; i++) {
				newResults[i].resultSetIndex = resultSetIndex;
				newResults[i].resultIndex = i;
			}
		}
		
		//converts meters to miles or kilometers
		function convertMeters(meters, units) {
			if (units == UNITS_MI)
				return meters/1609.34;
			return meters/1000; //return KM
		}
			
		function convertMetersForDisplay(meters, units, addLabel, roundToPlaces, clipLeadingZero) {
			var d = convertMeters(meters, units);
			if (roundToPlaces) d = roundNumber(d, roundToPlaces);
			
			if ( d <= 0 && roundToPlaces == 1 ) 
				d = "0.0";
			else if ( d <= 0 && roundToPlaces == 2 ) 
				d = "0.01";			
			
			dStr = String(d);
			if (addLabel) dStr += (units == UNITS_MI) ? MILES_LABEL : KILOMETERS_LABEL;
			if (clipLeadingZero) dStr = ( dStr.substr(0,1) == "0" ) ? dStr.substr(1) : dStr;
			return dStr;
		}

    function positive_mod(a, b)
        {
            /* always returns a positive value regardless of the sign of a */
            if (a < 0.0)
            {
                return b + (a % b);
            }
            else
            {
                return a % b;
            }
        }

        GRID_SIZE = 0.0015;
        HALF_GRID_SIZE = GRID_SIZE / 2.0;
		
		function snapToGrid(coord)
        {
            coord = coord * 1.0;            
            distanceToGrid = positive_mod(coord, GRID_SIZE);            

            //snap up or down, depending which is closer
            if (distanceToGrid < HALF_GRID_SIZE)
            {
                coord = coord - distanceToGrid;
            }
            else
            {
                coord = coord + GRID_SIZE - distanceToGrid;
            }
            
			return (Math.round(coord*10000.0))/10000.0;
		}

//*********** DOM functions ***********
		
		function getValue(field){
			if (field && field.value) 
				return field.value;
			return null;
		}
		
		function setValue(field, value){
			if (field) 
				field.value = value;
		}
		
		function getElemInternal(handle){
			if ( typeof(handle) == "string" )
				return document.getElementById(handle);
			return handle;
		}
		
		function getElem(handle){
			if ( typeof(handle) == "string" )
				return document.getElementById(handle);
			return null;
		}
				
		function getHTML(handle){
			var elem = getElemInternal(handle);
			if (elem) 
				return elem.innerHTML;
			return null;
		}
		
		function setHTML(handle, html){
			var elem = getElemInternal(handle);				
			if (elem) {
				elem.innerHTML = html;
				return true;
			}
			return false;
		}
				
		function appendHTML(handle, html){
			var elem = getElemInternal(handle);				
			if (elem) {
				elem.innerHTML += html;
				return true;
			}
			return false;
		}
		
		function setStyle(handle, css){
			var elem = getElemInternal(handle);
			if (elem && typeof(css) == "string") 
				elem.style.cssText += ';' + css;
		}
		
		function getDocBody(){
			return document.getElementsByTagName('BODY')[0];
		}
		
		function addElemToDom(elem){
			getDocBody().appendChild(elem);
		}
		
//*********** Popup dialogs ***********

function showDialog(content, customClass, hasCloseBox){
	initDialog();
	startModal();

	var fullContent = (hasCloseBox) ? '<img class="close-box" onclick="hideDialog()" src="<?= $static_asset_host ?>images/closeBox.gif" />' : '';
	fullContent += content;
	
	getElem("ws-dialog").className = customClass;
	setHTML("ws-dialog", fullContent);
	setStyle("ws-dialog", "display:block;");
}
function hideDialog(){
	setStyle("ws-dialog", "display:none;");
	endModal();
}
function initDialog(){
	if (getElem("ws-dialog")!=null) return;
	var dialogDiv = document.createElement('div');
	dialogDiv.id = 'ws-dialog';
	addElemToDom(dialogDiv);	
}
//************* modal controls ***************
function startModal(){
	initModal()
	var popmask = getElem('popupMask');
	if(popmask && popmask.style.display == "none"){
		setStyle(popmask, "display:block;");
		setMaskSize();
		hideSelectBoxes();
	}
}
function endModal(){
	setStyle("popupMask", "display:none;");
	displaySelectBoxes();
}

function initModal(){
	if (getElem("popupMask")!=null) return;
	var popmask = document.createElement('div');
	popmask.id = 'popupMask';
	addElemToDom(popmask);	
	setStyle(popmask, "display:none;");
	window.onresize = setMaskSize;
	window.onscroll = setMaskSize;
}
function setMaskSize() {
	var theBody = getDocBody();
	var popmask = getElem('popupMask');
	//alert(Math.max(document.body.scrollTop,document.documentElement.scrollTop) + ", " + Math.max(document.body.scrollLeft,document.documentElement.scrollLeft));
	
 	popmask.style.top = Math.max(document.body.scrollTop,document.documentElement.scrollTop) + 'px';
 	popmask.style.left = Math.max(document.body.scrollLeft,document.documentElement.scrollLeft) + 'px';
	popmask.style.height = Math.max(getViewportHeight(),theBody.scrollHeight) + 'px';
	popmask.style.width = Math.max(getViewportWidth(),theBody.scrollWidth) + 'px';
}
function getViewportHeight() {
	if (window.innerHeight!=window.undefined) return window.innerHeight;
	if (document.compatMode=='CSS1Compat') return document.documentElement.clientHeight;
	if (document.body) return document.body.clientHeight; 
	return window.undefined; 
}
function getViewportWidth() {
	if (window.innerWidth!=window.undefined) return window.innerWidth; 
	if (document.compatMode=='CSS1Compat') return document.documentElement.clientWidth; 
	if (document.body) return document.body.clientWidth; 
}
//for legacy IE, which fails to bury the selects under the modal pane
function hideSelectBoxes() {
	if(navigator.appName == "Microsoft Internet Explorer" && parseFloat(navigator.appVersion.split("MSIE")[1]) < 7 ){
		var selects = document.getElementsByTagName("SELECT");
		for(var i = 0; i < selects.length; i++) {
			selects[i].style.visibility="hidden";
		}
	}
}
function displaySelectBoxes() {
	if(navigator.appName == "Microsoft Internet Explorer" && parseFloat(navigator.appVersion.split("MSIE")[1]) < 7 ){
		var selects = document.getElementsByTagName("SELECT");
		for(var i = 0; i < selects.length; i++) {
			selects[i].style.visibility="visible";
		}
	}
}
	
//*********** Error code ***********

		function reportError(err) {
			showMessage(err);
		}
		
		function alertThese(){
			//alert(Array.prototype.join.call(arguments, " :: "));
		}

		function logThese(){
			//console.log(Array.prototype.join.call(arguments, " :: "));
		}
//*********** Debugging code ***********
		function dbug(str) {
			//if (console && console.log)
				//console.log(str);
			appendHTML("dbug", "<br />" + str);
		}
				
/** Utility Functions **/
// rand - Generates random number from 1 to n, inclusive
function rand ( n ) {
	return ( Math.floor ( Math.random ( ) * n + 1 ) );
}
function byte2Hex(n) {
	var nybHexString = "0123456789ABCDEF";
	return String(nybHexString.substr((n >> 4) & 0x0F,1)) + nybHexString.substr(n & 0x0F,1);
}
function RGB2Color(r,g,b) {
	return '#' + byte2Hex(r) + byte2Hex(g) + byte2Hex(b);
}
//return a hex color based on a score according to our gradient
function getScoreColor(score) {
	var gradient = Array();
	gradient[0] = [223, 68, 51];
	gradient[1] = [235, 237, 129];
	gradient[2] = [173, 228, 108];
	gradient[3] = [78, 173, 66];

	if (score < 55)
		return getBlendedColor(gradient[0], gradient[1], score/0.55);				
	else if (score < 75)
		return getBlendedColor(gradient[1], gradient[2], (score-55)/0.2);				
	else if (score < 95)
		return getBlendedColor(gradient[2], gradient[3], (score-75)/0.2);				
	else
		return RGB2Color(78, 173, 66);				
}

function getBlendedColor(rgb1, rgb2, percent) {
	var r = rgb1[0] * (1-percent/100) + rgb2[0] * percent/100;
	var g = rgb1[1] * (1-percent/100) + rgb2[1] * percent/100;
	var b = rgb1[2] * (1-percent/100) + rgb2[2] * percent/100;
	return RGB2Color(r, g, b);			
}

// convert a number from 0-24 into a time formatted string, hours and minutes only, with am or pm appended
function convertToTime(num) {
	var hours = Math.floor(num);
	var minutes = String(extractMinutes(num));
	if (minutes.length == 1) minutes = "0" + minutes;

var label = (hours >= 12) ? "pm" : "am";
	if (hours == 24) {
		hours = 12; 
		label="am";
	}
	else if (hours == 0)
		hours = 12;
	else if (hours > 12)
		hours -= 12;

	return hours + ":" + minutes + label;
}
function extractMinutes(num){
	var hours = Math.floor(num);
	var minutes = Math.round( (num-hours)*60 );
	return minutes;
}
function extractHours(num){
	return Math.floor(num) % 24;
}
function roundNumber(num, dec) {
	var result = Math.round( num * Math.pow( 10,dec) ) / Math.pow(10,dec);
	return result;
}
function cleanNumber(number) {
	var result = number;
	result = result.replace("(","");
	result = result.replace(")","");
	result = result.replace("-","");
	result = result.replace(" ","");
	return result;
}
