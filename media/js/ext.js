
function getElementPosition(theElement){
  var posX = 0;
  var posY = 0;

  while(theElement != null){
    posX += theElement.offsetLeft;
    posY += theElement.offsetTop;
    theElement = theElement.offsetParent;
  }

   return {x:posX,y: posY};
}

window.addEvent('domready',function() {
	setTimeout(function() { if ($('user-messages')) $('user-messages').morph({height: 0,opacity:0}) },2000)
});

window.addEvent('domready',function() {

	nowtime = new Date()
	document.getElements('.ddate').each(function(element) {
	
		date_inner = new Date(element.innerHTML.replace(/-/g,'/'));
		diff_date = nowtime - date_inner;
		diff_date = diff_date / 1000;
	
		start_date = element.innerHTML;

		if (diff_date < 60) { // mniej niz 60 sekund
			 element.innerHTML = 'mniej niż minute temu'
	    } else if ( diff_date < 60*60) { // mniej niz godzina
	        _minutes = Math.floor(diff_date/60)
	        element.innerHTML = _minutes + ' minut temu'
        } else if ( diff_date < 60*60*24 ) { // mniej niz dzien
	        _minutes = Math.floor(diff_date/60);
    	    _hours = Math.floor(_minutes/60);
    	    _minutes = _minutes - _hours*60;

    	    element.innerHTML = _hours+' godzin '+_minutes+' minut temu';
    	}
	});


});
