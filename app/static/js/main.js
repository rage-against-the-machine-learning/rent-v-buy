// Select canvases
var svg1 = d3.select("#choroplethSVG");

var	margin = {top: 30, right: 40, bottom: 30, left: 70},
	//width = 600 - margin.left - margin.right,
	width = 600,
    //height = 330 - margin.top - margin.bottom;
    height = 330;

const projectionUSA = d3.geoAlbersUsa()
     .translate([width/2, height/2])    /* translate to center of screen */
     .scale(700); /* scale things down so see entire US */

			var projectionCA = d3.geoMercator()
								   .center([ -120, 37 ])
								   .translate([ width/2, height/2 +40 ])
								   .scale([ width*2.5 ]);

    var geoPauth = d3.geoPath().projection(projectionCA);

    var choroplethSVG = d3.select("#choroplethSVG")
        //.attr("width", width)
        //.attr("height", height);
    var g = choroplethSVG.append("g")
    var allCAData;
    //var objectName = "California.geo"
    //d3.json("static/maps/zips_us_topo.json").then(function(data){
        //d3.json("static/maps/California.topo.json").then(function(data){
            d3.json("static/maps/California.topo_backup.json").then(function(data){
                // the backup file changes the object name from California.geo to Californiageo so the data() doesn't error out
            allCAData = data
            console.log(data)
            //Promise.all(promises).then(function(data) {
            g.selectAll("path")
                //.data(topojson.feature(data, data.objects.zip_codes_for_the_usa).features)
                .data(topojson.feature(data, data.objects.Californiageo).features)
                .enter()
                .append("path")
                .attr("stroke", "#333")
                .attr("class", "counties")
                .attr("class", "zip")
                .attr("data-zip", function(d) {return d.properties.id; })
                //.attr("data-zip", function(d) {return d.properties.zip; })
                //.attr("data-state", function(d) {return d.properties.state; })
                //.attr("data-name", function(d) {return d.properties.name; })
                .attr("d", geoPauth);
        }) ;

const MAX_BEDROOMS = 5
var bedroomSlider = d3
    .sliderBottom()
    .min(1)
    .max(MAX_BEDROOMS)
    .step(1)
    .ticks(MAX_BEDROOMS)
    //.displayvalue(true)
    .on('onchange', val => {
        console.log("number of bedrooms selected: ",val)
    })

  	var gBedroomSlider = d3
        .select('div#bedroomSlidah')
	    .append('svg')
	    .attr('width', 300)
	    .attr('height', 100)
	    .append('g')
	    .attr('transform', 'translate(30,30)')

        gBedroomSlider.call(bedroomSlider);

const SQFT_INCREMENT = 500
var sqftSlider = d3
    .sliderBottom()
    .min(1500)
    .max(6000)
    .step(SQFT_INCREMENT)
    .on('onchange', val => {
        console.log("sqft selected: ",val)
    })


  	var gSqftSlider = d3
        .select('div#sqFootageSlidah')
	    .append('svg')
	    .attr('width', 300)
	    .attr('height', 100)
	    .append('g')
	    .attr('transform', 'translate(30,30)')

        gSqftSlider.call(sqftSlider);