function initialize() {
	  //VARIABLES
	  var input = /** @type {HTMLInputElement} */(document.getElementById('id_lugar'));
	  var input2 = /** @type {HTMLInputElement} */(document.getElementById('id_lugar2'));
	  var autocomplete, autocomplete2;
	  var infowindow = new google.maps.InfoWindow();

	  // GEOLOCALIZACION
	  
	  if(ubicacion_dinamica==false){
		  autocomplete= new google.maps.places.Autocomplete(input, {types: ['(cities)'],componentRestrictions: {country: "es"}});
		  autocomplete2= new google.maps.places.Autocomplete(input2, {types: ['(cities)'],componentRestrictions: {country: "es"}});
	  }
	  
	
	  else if(navigator.geolocation) {
		 navigator.geolocation.getCurrentPosition(setBounds);
  	   }
	  else {
		  autocomplete= new google.maps.places.Autocomplete(input, {types: ['(cities)'],componentRestrictions: {country: "es"}});
		  autocomplete2= new google.maps.places.Autocomplete(input2, {types: ['(cities)'],componentRestrictions: {country: "es"}});

	  }
	  
	  function setBounds(position){
	  	var mi_posicion= new google.maps.LatLngBounds(
			new google.maps.LatLng(position.coords.latitude, position.coords.longitude)
		);
	  	var options = {
	  		  bounds: mi_posicion,
	  		  types: ['(cities)'],
	  		  componentRestrictions: {country: "es"}
	  	};
	  	autocomplete= new google.maps.places.Autocomplete(input, options);
	  	autocomplete2= new google.maps.places.Autocomplete(input2, options);

	  }
	  
	  //Listener 
	  
	  google.maps.event.addListener(autocomplete, 'place_changed', function() {
	    infowindow.close();
	    input.className = '';
	    var place = autocomplete.getPlace();
	    if (!place.geometry) {
	      // Inform the user that the place was not found and return.
	      input.className = 'notfound';
	      return;
	    }

	    // If the place has a geometry, then present it on a map.

	    var address = '';
	    if (place.address_components) {
	      address = [
	        (place.address_components[0] && place.address_components[0].short_name || ''),
	        (place.address_components[1] && place.address_components[1].short_name || ''),
	        (place.address_components[2] && place.address_components[2].short_name || '')
	      ].join(' ');
	    }

	    infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + address);
	  });
	  google.maps.event.addListener(autocomplete2, 'place_changed', function() {
		    infowindow.close();
		    input.className = '';
		    var place = autocomplete2.getPlace();
		    if (!place.geometry) {
		      // Inform the user that the place was not found and return.
		      input.className = 'notfound';
		      return;
		    }

		    // If the place has a geometry, then present it on a map.

		    var address = '';
		    if (place.address_components) {
		      address = [
		        (place.address_components[0] && place.address_components[0].short_name || ''),
		        (place.address_components[1] && place.address_components[1].short_name || ''),
		        (place.address_components[2] && place.address_components[2].short_name || '')
		      ].join(' ');
		    }

		    infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + address);
		  });
	 
	}
	//ARRANCA
google.maps.event.addDomListener(window, 'load', initialize);
