var directionsDisplay;
var directionsService = new google.maps.DirectionsService();
var map;
var re = /\[(.*?)\]/;

$(document).on('ready', function() {
  directionsDisplay = new google.maps.DirectionsRenderer();
  var mapOptions = {
    center: new google.maps.LatLng(37.333351,-4.5765007),
    zoom: 8,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };

  map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
  directionsDisplay.setMap(map);

  $('.formCtweets').on('submit', function(){
    var geo = $('#selectCity').val();
    var data = {'geo': geo}
    console.log(geo);
    $.ajax({
      type: 'GET',
      url: '/data',
      data: 'geo='+geo,
      success: function(resp){
        console.log(resp);
        $.each(resp, function(index){
          var lon = resp[index].coordinates[0];
          var lat = resp[index].coordinates[1];
          var myLatlng = new google.maps.LatLng(lat, lon);

          var contentString = '<div><h4><a target="_blank" href="http://twitter.com/"'+resp[index].name+'>'+resp[index].name+
                '</a><small> '+resp[index].date+'</small></h4><p>'+resp[index].tweet+'</p></div>';
          var infowindow = new google.maps.InfoWindow({
            content: contentString
          });

          var marker = new google.maps.Marker({
            position: myLatlng,
            map: map,
            title: resp[index].name
          });

          google.maps.event.addListener(marker, 'click', function() {
            infowindow.open(map,marker);
          });
        });
      }
    });
    return false;
  });

});
