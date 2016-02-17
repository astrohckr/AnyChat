(function () {
    var userId = window.localStorage.getItem('user_id');
    var crsf = $('input[name=csrfmiddlewaretoken]').val();

    // post gps location, if not then lookup ip on the server
    navigator.geolocation.getCurrentPosition(function (position) {
        $.post('/login/', {
            csrfmiddlewaretoken: crsf,
            lat: position.coords.latitude,
            lon: position.coords.longitude,
            userId: userId
        }, function (response) {
            window.localStorage.setItem('user_id', response);
        });
    });
})();
