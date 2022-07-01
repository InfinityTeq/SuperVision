// 
//  TrafficMap.js
//  (ATMS) Montgomery County Department of Transportation (MCDOT)
//  
//  Created by Craig Hoover obo The NERDS Group on 2012-08-06.
//  Copyright 2012 Montgomery Country Department of Transportation (MCDOT). All rights reserved.


// extend Javascript Number object
if (typeof (Number.prototype.toRad) === "undefined") {
    Number.prototype.toRad = function () {
        return this * Math.PI / 180;
    }
}

TrafficMap =
{
    instance: null,
    userLat: null,
    userLng: null,
    bounds: null,
    listings: [],
    radius: 26,
    circle: null,
    providers: ['DDOT'],     // single default provider 
    //   providers : ['Montgomery County', 'VDOT'], // for multiple providers by default
    center: null,
    markers: [],
    onClick: function () { },
    county: { lat: 38.891961, lng: -77.014981 },
    init: function () {
        TrafficMap.userLat = TrafficMap.county.lat;
        TrafficMap.userLng = TrafficMap.county.lng;

        var element = document.getElementById("canvas");
        var options = { mapTypeId: google.maps.MapTypeId.ROADMAP };
        var listings = TrafficMap.findRadialListings(TrafficMap.userLat, TrafficMap.userLng, TrafficMap.radius);

        if (TrafficMap.providers.length > 0) {
            var i = listings.length;
            var found = [];

            while (i--) {
                for (var p = 0; p < TrafficMap.providers.length; p++) {
                    // console.log(listings[i].provider)

                    if (listings[i].provider == TrafficMap.providers[p]) {
                        found.push(listings[i]);
                    }
                }
            }
            listings = found;
        }


        // reset previous map
        try {
            TrafficMap.instance.destroy();
            TrafficMap.circle.setMap(null);
            TrafficMap.bounds = null;
            TrafficMap.markers = [];
            element.innerHTML = '';
        } catch (e) { }

        // establish center if user coords are provided
        if (TrafficMap.userLat && TrafficMap.userLng) {
            options.center = new google.maps.LatLng(TrafficMap.userLat, TrafficMap.userLng);
        }

        // create map
        TrafficMap.instance = new google.maps.Map(element, options);
        TrafficMap.bounds = new google.maps.LatLngBounds();

        // store zoom when idle
        google.maps.event.addListenerOnce(TrafficMap.instance, "idle", function () {
            TrafficMap.zoom = TrafficMap.instance.getZoom();
        });

        // drop center point if user coords are provided
        if (options.center) {
            var myloc = { title: 'My Location', position: new google.maps.LatLng(TrafficMap.userLat, TrafficMap.userLng), map: TrafficMap.instance };
            TrafficMap.center = new google.maps.Marker(myloc);
        }

        // bind info window
        TrafficMap.infowindow = new google.maps.InfoWindow({ maxWidth: 200 });

        // populate listings
        for (var i = 0; i < listings.length; i++) {
            var listing = listings[i];
            // if (listing.id == 200124)
                TrafficMap.addCamera(listing);
        }

        //if(options.center) TrafficMap.addRadiusCircle();

    },
    marker:
   {
       getIcon: function (index) {
           var index = index || 1;

           return new google.maps.MarkerImage('/images/video' + index + '.png',
            new google.maps.Size(32, 32),
            new google.maps.Point(0, 0),
            new google.maps.Point(0, 32)
         );
       },
       getShadow: function () {
           return new google.maps.MarkerImage('/images/mm_20_shadow.png',
            new google.maps.Size(22, 20),
            new google.maps.Point(0, 0),
            new google.maps.Point(0, 20)
         );
       }
   },
    clearCameras: function () {
        if (TrafficMap.markers) {
            for (k in TrafficMap.markers) {
                TrafficMap.markers[k].setMap(null);
                TrafficMap.markers[k] = null;
                delete (TrafficMap.markers[k]);
            }
        }
    },
    addCamera: function (obj) {
        if (!TrafficMap.instance) return;

        // plant the marker
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(obj.lat, obj.lng),
            map: TrafficMap.instance,
            icon: TrafficMap.marker.getIcon(obj.pindex),
            title: obj.name,
            content: '<h3>' + obj.name + '</h3><div class="image"><a title="' + obj.name + '" href="javascript:CameraImage.load(' + obj.id + ')"><img src="' + obj.smallimage + '"/></a></div>',
            shadow: TrafficMap.marker.getShadow()
        });

        // add a cameraId to our marker
        marker.cameraId = obj.id;
        TrafficMap.markers.push(marker);

        // create mouseover marker event
        google.maps.event.addListener(marker, 'click', function () {
            TrafficMap.infowindow.close(TrafficMap.instance, this);
            TrafficMap.infowindow.setContent('<div class="specialinfo">' + this.content + '</div>');
            TrafficMap.infowindow.open(TrafficMap.instance, this);
        });

        // add click event
        (function (id) {
            google.maps.event.addListener(marker, 'click', function () {
                TrafficMap.onClick.call(this, id);
            });
        })(obj.id);

        // fit map bounds
        var myLatLng = new google.maps.LatLng(obj.lat, obj.lng);
        TrafficMap.bounds.extend(myLatLng);
        TrafficMap.instance.fitBounds(TrafficMap.bounds);
    },
    findRadialListings: function (lat, lng, distance, listings) {
        var listings = listings || TrafficMap.listings;
        var i = listings.length;
        var tmp = listings.slice(0); // clone array
        var dist = distance || TrafficMap.radius;
        var found = [];

        if (!lat || !lng) return tmp;

        while (i--) {
            tmp[i].distance = TrafficMap.calcDistance(lat, lng, tmp[i].lat, tmp[i].lng);
            if (tmp[i].distance <= dist) {
                found.push(tmp[i]);
            }
        }
        delete (tmp);

        // sort listings by closest
        found.sort(function (obj1, obj2) {
            return obj1.distance - obj2.distance;
        });

        return found;
    },
    removeRadiusCircle: function () {
        TrafficMap.circle.setMap(null);
        TrafficMap.circle = null;
    },
    addRadiusCircle: function () {
        // Add circle overlay and bind to marker
        TrafficMap.circle = new google.maps.Circle({
            map: TrafficMap.instance,
            radius: TrafficMap.radius * 1609.34, // miles * meters
            fillColor: '#FFCC66',
            fillOpacity: 0.35,
            strokeWeight: 0
        });
        TrafficMap.circle.bindTo('center', TrafficMap.center, 'position');
        bounds = TrafficMap.circle.getBounds();
        TrafficMap.instance.fitBounds(bounds);
    },
    calcDistance: function (lat1, lng1, lat2, lng2) {
        lat1 = parseFloat(lat1);
        lat2 = parseFloat(lat2);
        lng1 = parseFloat(lng1);
        lng2 = parseFloat(lng2);

        var R = 6378.137; // average earth radius
        var dLat = (lat2 - lat1).toRad();
        var dLon = (lng2 - lng1).toRad();
        var lat1 = lat1.toRad();
        var lat2 = lat2.toRad();

        var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(lat1) * Math.cos(lat2);
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;  // returns in miles
    },
    adjustRadius: function (radius) {
        TrafficMap.circle.setRadius(radius);
    },
    getCurrentPosition: function (callback) {
        TrafficMap.userLat = TrafficMap.county.lat;
        TrafficMap.userLng = TrafficMap.county.lng;

        /*
        if(navigator.geolocation)
        {
        navigator.geolocation.getCurrentPosition(function(pos){
        TrafficMap.userLat = parseFloat(pos.coords.latitude);
        TrafficMap.userLng = parseFloat(pos.coords.longitude);
        if(callback) callback.call();
        });
        }  
        */
        if (callback) callback.call();
    }
};


/**
* creates camera map with listings
* @param listings array of objects
* @param local - set 'true' to geolocate current position
*/


var CameraImage =
{
    refreshInterval: null,
    cacheInterval: null,
    pauseTimeout: null,
    pauseTimer: 60 * 1000, // 60 seconds
    current: null,
    cache: [],
    load: function (id) {
        // stop refreshes after set time
        clearTimeout(CameraImage.pauseTimeout);

        CameraImage.pauseTimeout = setTimeout(function () {
            clearInterval(CameraImage.refreshInterval);
            clearInterval(CameraImage.cacheInterval);
        }, CameraImage.pauseTimer);

        var i = TrafficMap.listings.length;
        var found = null;
        var sel = document.getElementById('cameras');

        // find our camera
        while (i--) {
            if (parseInt(TrafficMap.listings[i].id) == id) {
                found = TrafficMap.listings[i];
                break;
            }
        }

        if (found) {
            // reset all of our data
            CameraImage.current = found;
            CameraImage.cache = [];

            clearInterval(CameraImage.refreshInterval);
            clearInterval(CameraImage.cacheInterval);

            // find the camera
            for (var j = 0; j < sel.options.length; j++) {
                if (parseInt(sel.options[j].value) == parseInt(id)) {
                    sel.selectedIndex = j;
                    break;
                }
            }

            // get and cache the image
            var d = new Date();
            var img = new Image(352, 240);
            img.src = found.image + '&t=' + d.getTime();

            document.getElementById('intersect').innerHTML = found.name;
            document.getElementById('image').innerHTML = '<img id="camera-image" src="' + img.src + '" />';
            CameraImage.cache.push(img.src);

            // start a cache of images
            CameraImage.cacheInterval = setInterval(function () {
                var d = new Date();
                var img = new Image(352, 240);

                img.src = found.image + '&t=' + d.getTime();
                CameraImage.cache.push(img.src);

            }, parseInt(found.refresh));

            // start refresh after 1 second of caches are available
            setTimeout(function () {
                CameraImage.startRefresh(found.refresh);
            }, 1000);

        }
    },
    startRefresh: function (timer) {
        CameraImage.refreshInterval = setInterval(function () {
            document.getElementById('camera-image').setAttribute('src', CameraImage.cache[CameraImage.cache.length - 1]);
        }, timer);
    },
    stopRefresh: function () {
        clearInterval(CameraImage.cacheInterval);
        clearInterval(CameraImage.refreshInterval);
        clearTimeout(myTimea);
        clearTimeout(myTimeb);
    }
};


/*
* initialization function
* @param listings - array of JSON camera locations
* @param local - boolean to use browser geo location
* @return nothing
*/

function LoadCameras(listings) {
    var local = local || false;

    if (TrafficMap.instance) return;

    TrafficMap.listings = listings || [];
    TrafficMap.onClick = CameraImage.load;
    TrafficMap.init(true);

}

function UpdateProviders() {
    var inp = document.getElementById('providers').getElementsByTagName('input');
    var providers = [];

    for (var i = 0; i < inp.length; i++) {
        if (inp[i].checked) providers.push(inp[i].value);
    }

    TrafficMap.clearCameras();

    var listings = TrafficMap.findRadialListings(TrafficMap.userLat, TrafficMap.userLng, TrafficMap.radius);
    var matches = [];
    var i = listings.length;
    var count = 0;

    while (i--) {
        for (var p = 0; p < providers.length; p++) {
            if (listings[i].provider == providers[p]) {
                //if (listings[i].id == 200124)
                TrafficMap.addCamera(listings[i]);
                count++;
            }
        }
    }
    // console.log('displaying :' +count +' cameras')
}

