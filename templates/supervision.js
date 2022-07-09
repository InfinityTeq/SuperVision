// SuperVision
// Created by : C0SM0

// live updates
L.Control.Liveupdate = L.Control.extend({

    timer: false,
    
    options: {
        position: 'topleft',
        title: {
            'false': 'Start live updates',
            'true': 'Stop live updates'
        },
        is_updating: true,
        update_map: false,  // callback function
        interval: 10000
    },
    
    onAdd: function (map) {
        this.container = L.DomUtil.create('div', 'leaflet-control-liveupdate leaflet-bar leaflet-control');
    
        this.link = L.DomUtil.create('a', 'leaflet-control-liveupdate-button leaflet-bar-part', this.container);
        this.link.href = '#';
    
        this._map = map;
        this._setUpdating(this.options.is_updating);
        map.liveUpdateControl = this;
    
        L.DomEvent.on(this.link, 'click', this._click, this);
        return this.container;
    },
    
    _click: function (e) {
        L.DomEvent.stopPropagation(e);
        L.DomEvent.preventDefault(e);
        this.toggleUpdating();
    },
    
    _toggleTitle: function() {
        this.link.title = this.options.title[this.isUpdating()];
    },
    
    isUpdating: function () {
        return this._isUpdating || false;
    },
    
    _setUpdating: function (updating) {
        this._isUpdating = updating;
        if (updating) {
            L.DomUtil.addClass(this.container, 'leaflet-liveupdate-on');
        } else {
            L.DomUtil.removeClass(this.container, 'leaflet-liveupdate-on');
        }
        this._toggleTitle();
    },
    
    toggleUpdating: function () {
        if (this.isUpdating ()) {
            this.stopUpdating ();
            a = 'stopped';
        }
        else {
            this.startUpdating ();
            a = 'started';
        }
        if (this._map.messagebox) {
            this._map.messagebox.show('Live updates ' + a);
        }
        return this;
    },
    
    startUpdating: function () {
    
        var map = this._map;
        var update_map = this.options.update_map;
        var _this = this;
    
        this._setUpdating(true);
        update_map(this);
        this.timer = setInterval(function() {
            update_map(_this);
        }, this.options.interval);
        return this;
    },
    
    stopUpdating: function () {
        this._setUpdating(false);
        clearInterval(this.timer);
        this.timer = false;
        return this;
    },
    
    updateNow: function () {
        var update_map = this.options.update_map;
        update_map(this);
        return this;
    }
    
});
    
L.control.liveupdate = function (options) {
return new L.Control.Liveupdate(options);
};

// get indexes from xml data
function get_indexes (filepath, item, index_range) {
    let xmlContent = '';

    fetch(filepath).then((response)=> {
        response.text().then((xml)=>{
            xmlContent = xml;

            let parser = new DOMParser();
            let xmlDOM = parser.parseFromString(xmlContent, 'application/xml');
            let content = xmlDOM.querySelectorAll(item);

            content.forEach(XmlNode => {
                for (var i = 0; i < index_range; i++) {
                    var element = XmlNode.children[i].innerHTML;

                    // display elements and their index
                    console.log(element);
                    console.log(i);
                }
            })
        })
    })
}

// plot vehicle data
transit = [];
function add_transit (icon_name, filepath, item, name, id_index, lat_index, lon_index) {
    for (var i=0; i<transit.length; i++) {
        MAP.removeLayer(transit[i]);
    }
    transit = [];

    let xmlContent = '';

    fetch(filepath).then((response)=> {
        response.text().then((xml)=>{
            xmlContent = xml;

            let parser = new DOMParser();
            let xmlDOM = parser.parseFromString(xmlContent, 'application/xml');
            let content = xmlDOM.querySelectorAll(item);

        content.forEach(XmlNode => {
            var id = XmlNode.children[id_index].innerHTML;
            var latitude = XmlNode.children[lat_index].innerHTML;
            var longitude = XmlNode.children[lon_index].innerHTML;
            var num_of_vehicles = transit.length;

            var options = { 
                title: id,
                clickable: true,
                draggable: false
            }


            var vehicle = new L.Marker([latitude, longitude], options, popup=name);

            // var icon = L.AwesomeMarkers.icon(
            //     {"extraClasses": "fa-rotate-0", "icon": "bus", "iconColor": "white", "markerColor": "blue", "prefix": "glyphicon"}
            // );

            var icon = L.icon({
                iconUrl: '/assets/' + icon_name + '.png',
                iconSize: [40, 40],
                popupAnchor: [-3, -76],
            })

            vehicle.setIcon(icon);
            
            transit.push(vehicle);
            MAP.addLayer(transit[num_of_vehicles]);

            })
        })
    })     
}

// live updates on map
L.control.liveupdate ({
    update_map: function () {
        // TODO: make this better
        xml_list = ARRAY;

        for (var i = 0; i <xml_list.length; i++){
            var filename = xml_list[i];
            var filepath = 'xml/' + filename;

             console.log(filepath);
           
            var args = filename.split("-");
            var icon_name = args[0];
            var item = args[1];
            var name = args[2];
            var id = args[3];
            var lat = args[4];
            var lon = args[5].split(".")[0];

            add_transit(icon_name, filepath, item, name, id, lat, lon)
        }

        console.log('updated')
    },
    position: 'topleft',
    interval: 10000
})
.addTo(MAP)
.startUpdating();