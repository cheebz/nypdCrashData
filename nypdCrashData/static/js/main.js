// main.js

var main = function () {

	mapboxgl.accessToken = mapbox_access_key;

	var filterGroup = document.getElementById('filter-group');
	
	var map = new mapboxgl.Map({
		container: 'map',
		style: 'mapbox://styles/mapbox/dark-v9',
		center: [-73.963761, 40.688357],
		zoom: 9.5
	});
			
	map.on('load', function() {
		// Add a new source from our GeoJSON data and set the
		// 'cluster' option to true. GL-JS will add the point_count property to your source data.
		map.addSource("crashes", {
			type: "geojson",
			data: crash_data_points,
			cluster: true,
			clusterMaxZoom: 14, // Max zoom to cluster points on
			clusterRadius: 50 // Radius of each cluster when clustering points (defaults to 50)
		});

		map.addLayer({
			id: "clusters",
			type: "circle",
			source: "crashes",
			filter: ["has", "point_count"],
			paint: {
				// Use step expressions (https://www.mapbox.com/mapbox-gl-js/style-spec/#expressions-step)
				// with three steps to implement three types of circles:
				//   * Blue, 20px circles when point count is less than 100
				//   * Yellow, 30px circles when point count is between 100 and 750
				//   * Pink, 40px circles when point count is greater than or equal to 750
				"circle-color": [
					"step",
					["get", "point_count"],
					"#51bbd6",
					100,
					"#f1f075",
					750,
					"#f28cb1"
				],
				"circle-radius": [
					"step",
					["get", "point_count"],
					20,
					100,
					30,
					750,
					40
				]
			}
		});

		map.addLayer({
			id: "cluster-count",
			type: "symbol",
			source: "crashes",
			filter: ["has", "point_count"],
			layout: {
				"text-field": "{point_count_abbreviated}",
				"text-font": ["DIN Offc Pro Medium", "Arial Unicode MS Bold"],
				"text-size": 12
			}
		});

		map.addLayer({
			id: "unclustered-point",
			type: "circle",
			source: "crashes",
			filter: ["!has", "point_count"],
			paint: {
				"circle-color": "#11b4da",
				"circle-radius": 6,
				"circle-stroke-width": 1,
				"circle-stroke-color": "#fff"
			}
		});
	});

	map.on('click', function(e) {
	  var features = map.queryRenderedFeatures(e.point, {
		layers: ["unclustered-point"]
	  });

	  if (!features.length) {
		return;
	  }

	  var feature = features[0];

	  var popup = new mapboxgl.Popup({ offset: [0, -15] })
		.setLngLat(feature.geometry.coordinates)
		.setHTML('<h3>' + feature.properties.title + '</h3><p>' + 'Cause: ' + feature.properties.description + '</p>')
		.setLngLat(feature.geometry.coordinates)
		.addTo(map);
	});
	
	
	
}

$(document).ready(main);