// Select canvases
var svg1 = d3.select("#choroplethSVG");

var	margin = {top: 30, right: 40, bottom: 30, left: 70},
	//width = 600 - margin.left - margin.right,
	width = 600,
    //height = 330 - margin.top - margin.bottom;
    height = 330;

    var buyRent;
    d3.json("static/maps/buy_rent_appr_formatted.json", function(d) {
        console.log("[buyRent]" +d)
			  return {
			    buy: +buy,
			    rent: +rent
			 };
			}).then(function(data) {
			    buyRent = data;
			    //console.log("thenfunction" + data)
                    //data.forEach(function(d){
                    //console.log("[buy]" +d.buy)
                    //    console.log("[rent]" +d.rent)
        })


//var div = d3.select("#choroplethSVG").append("div")
var div = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

var projNew;
const projectionUSA = d3.geoAlbersUsa()
     .translate([width/2, height/2])    /* translate to center of screen */
     .scale(700); /* scale things down so see entire US */

			var projectionCA1 = d3.geoMercator()
								   .center([ -120, 37 ])
								   //.translate([ width/2, height/2 +40 ])
                                   .translate([ width/2, height/2 ])
								   .scale([ width*2.5 ]);

    var geoPauth = d3.geoPath().projection(projectionCA1);
    var zipCityDict = {};

    var choroplethSVG = d3.select("#choroplethSVG")
        //.attr("width", width)
        //.attr("height", height);
    var g = choroplethSVG.append("g")
    var allCAData;
    var zipLatLong = d3.map() ; // arrary of dicts; e.g. [{"zipcode":75074, "lat":-84, "long":-44}]
    d3.tsv("static/maps/zips.tsv", function(d) {
        //console.log("line is: ", d)
        d.lat = +d.lat;
        d.zip = d.zip;
        d.lon = +d.lon;
        /*var eachDict = {};
        eachDict["zipcode"] = +d[2];
        eachDict["lat"] = +d[1];
        eachDict["long"] = +d[0];
         */
        zipLatLong.set(d.zip, d)
    })
var selObject;
var eachDict = {};
    var selectedLocation;
    var buyPrice = "$0"
    var rentPrice = "$0"
    //var objectName = "California.geo"

    function zipClicked(d) {
if (typeof lastSelectedObject != 'undefined') {
    console.log("last sel was: "+lastSelectedObject)
    lastSelectedObject.style("stroke", "black")
        .attr("stroke-width", 1)
        .attr("fill", d3.rgb(128,128,128))
}
        sel = d3.select(this);
        lastSelectedObject = sel;

        console.log("we are in the zipClicked? what is sel: "+sel)
        selectedLocation = d.properties.name + ", CA, " + d.properties.zip
                console.log("zipcode: " + d.properties.zip + ", city: " + d.properties.name)
                if (buyRent[d.properties.zip] == undefined) {
                    buyPrice = "$0";
                    rentPrice = "$0";
                } else {
                    buyPrice = buyRent[d.properties.zip].buy;
                    rentPrice = buyRent[d.properties.zip].rent;
                }
        console.log("zip area clicked! location selected: " + selectedLocation);
            d.fx = d.x;
    d.fy = d.y;
        //sel.selectAll("g")
            //.enter()
            //.append("path")
            sel.style("stroke", "orange") //q2d2 Mark pinned nodes to visually distinguish them from unpinned nodes,
            .attr("stroke-width", 3) // q2d2
        .attr("fill", function(d) {
            console.log("truly are we in the selectPath? what is sel: "+sel)
            return d3.rgb(255,255,255);
        })
        fillSelectedLocation(selectedLocation)
        fillRentEstimate(rentPrice)
        fillSaleEstimate(buyPrice)
    }

    function fillSelectedLocation(d) {
        sel = d3.select("#selectedLocationDiv")
        sel.selectAll("*").remove();

            sel.append("text")
                .attr("font-family", "sans-serif")
                .style("font-size", "18px")
                .text(d)

        //xxx
//selectedLocationDiv
    }

        function fillSaleEstimate(d) {
        sel = d3.select("#saleEstimateDiv")
        sel.selectAll("*").remove();

            sel.append("text")
                .attr("font-family", "sans-serif")
                .style("font-size", "18px")
                .text(d)

        //xxx
//selectedLocationDiv
    }


        function fillRentEstimate(d) {
        sel = d3.select("#rentEstimateDiv")
        sel.selectAll("*").remove();

            sel.append("text")
                .attr("font-family", "sans-serif")
                .style("font-size", "18px")
                .text(d)

        //xxx
//selectedLocationDiv
    }

    d3.json("static/maps/zips_california_topo-v2.json").then(function(data) {
        //d3.json("static/maps/zips_california.json").then(function(data) {
        var zip0;
        //d3.json("static/maps/California.topo.json").then(function(data){
        //d3.json("static/maps/California.topo_backup.json").then(function(data){
        // the backup file changes the object name from California.geo to Californiageo so the data() doesn't error out
        allCAData = data
        //console.log(data)
        //Promise.all(promises).then(function(data) {
        g.selectAll("path")
            .data(topojson.feature(data, data.objects.zip_codes_for_the_usa).features)
            //.data(topojson.feature(data, data.objects.Californiageo).features)
            .enter()
            .append("path")
            .attr("stroke", "black")
            //.attr("stroke", "#333")
            .attr("fill", d3.rgb(128,128,128))
            .attr("class", "counties")
            .attr("class", "zip")
            //.attr("data-zip", function(d) {return d.properties.id; })
            .attr("data-zip", function (d) {
                return d.properties.zip;
            })
            .attr("data-state", function (d) {
                return d.properties.state;
            })
            .attr("data-name", function (d) {
                zipCityDict[d.properties.zip] = d.properties.name;
                return d.properties.name;
            })
            .attr("d", geoPauth)
            .on("mouseover", function (d) {

                var buyPrice, rentPrice
                console.log("zipcode: " + d.properties.zip + ", city: " + d.properties.name)
                if (buyRent[d.properties.zip] == undefined) {
                    buyPrice = "$0";
                    rentPrice = "$0";
                } else {
                    buyPrice = buyRent[d.properties.zip].buy;
                    rentPrice = buyRent[d.properties.zip].rent;
                }
                div.transition()
                    .duration(200)
                    .style("opacity", 0.9);
                div.html(
                    "zipcode: " + d.properties.zip + "<br/>" +
                    "city: " + d.properties.name + "<br/>" +
                    "buy: " + buyPrice + "<br/>" +
                    "rent: " +  rentPrice
                )
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY + 28) + "px");
            })
            .on("mouseout", function (d) {
                div.transition()
                    .duration(500)
                    .style("opacity", 0)
            })
            .on("click", zipClicked);
            //.on("click", zipClicked);
         /*   .on("click", function(d) {
                console.log(d.properties.zip + "Clicked! anony");
                d.selectAll("path")
            .style("stroke", "black") //q2d2 Mark pinned nodes to visually distinguish them from unpinned nodes,
            .attr("stroke-width", 3) // q2d2
                //zipClicked(d)
            })
        */

       var input = d3.select("#myInput")
      //.on("cut", function() { setTimeout(change, 10); })
      //.on("paste", function() { setTimeout(change, 10); })
           .on("click", change)
      .on("change", change)



   function change() {
       var latitude, longitude;
       console.log("in change()")
      //xxx
       var enteredString = input.property("value");
       var enteredData = enteredString.substr(enteredString.length - 5);
       // Add mapping here
       console.log("Received from autocomplete: " + enteredData);
       zipRegex = /[0-9]{5}/;
       if (zipRegex.test(enteredData)) {
           latitude  = zipLatLong["$"+enteredData].lat;
           longitude = zipLatLong["$"+enteredData].lon
           console.log("you entered the zip code: " + enteredData)
           g.selectAll("*").remove();
           console.log("latitude: ", latitude)
           console.log("longitude: ", longitude)

           projNew = d3.geoMercator()
           .center([ Math.round(longitude), Math.round(latitude) ])
           .translate([ width/2, height/2 ])
           .scale([ width*50.5 ]);

           // Show inputs for financial calculations
           finInputs = document.getElementById('financialInputs');            
           finInputs.style.display = "block";
           show_sliders();

       geoPauth2 = d3.geoPath().projection(projNew)


           g.selectAll("path")
            .data(topojson.feature(allCAData, allCAData.objects.zip_codes_for_the_usa).features)
            .enter()
            .append("path")
            .style("stroke", "black")


            //sel.style("stroke", "orange") //q2d2 Mark pinned nodes to visually distinguish them from unpinned nodes,
            //.attr("stroke-width", 3)
            //.attr("stroke", "#ff0")
            .attr("fill", function(d) {
                   if (d.properties.zip == enteredData) {
                       selectedLocation = d.properties.name + ", CA, " + d.properties.zip
                       fillSelectedLocation(selectedLocation)
                       fillRentEstimate(buyRent[d.properties.zip].buy)
                       fillSaleEstimate(buyRent[d.properties.zip].rent)
                       //selectedLocation = d;
                       //zipColor = d3.rgb(255,255,255)
                   if (typeof lastSelectedObject != 'undefined') {
                console.log("zoomedIn: last sel was: "+lastSelectedObject +" , resetting!")
                    lastSelectedObject.style("stroke", "black")
                        .attr("stroke-width", 1)
                        .attr("fill", d3.rgb(128,128,128))
}
                       sel = d3.select(this);
                       lastSelectedObject = sel;
                       d.fx = d.x;
                       d.fy = d.y;
                       sel.style("stroke", "orange")
                           .attr("stroke-width", 3)
                           .style("fill", function(d) {
                               return d3.rgb(255,255,255);
                           })

                       console.log("zoomed inside the fill loop, zip was: "+d.properties.zip+", zipcolor: "+zipColor)

                   } else {
                       zipColor = d3.rgb(128,128,128)
                   }
                   return zipColor;
               })
            .attr("class", "counties")
            .attr("class", "zip")
            .attr("data-zip", function (d) {
                console.log("inside zipcode iteration, d: " + d)
                return d.properties.zip;
            })
            .attr("data-state", function (d) {
                return d.properties.state;
            })
            .attr("data-name", function (d) {
                return d.properties.name;
            })
            .attr("d", geoPauth2)
            .on("click", zipClicked)
            .on("mouseover", function (d) {
                var buyPrice, rentPrice
                console.log("zipcode: " + d.properties.zip + ", city: " + d.properties.name)
                                if (buyRent[d.properties.zip] == undefined) {
                    buyPrice = "$0";
                    rentPrice = "$0";
                } else {
                    buyPrice = buyRent[d.properties.zip].buy;
                    rentPrice = buyRent[d.properties.zip].rent;
                }
                div.transition()
                    .duration(200)
                    .style("opacity", 0.9);
                div.html(
                    "zipcode: " + d.properties.zip + "<br/>" +
                    "city: " + d.properties.name + "<br/>" +
                                        "buy: " + buyPrice + "<br/>" +
                    "rent: " +  rentPrice
                )
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY + 28) + "px");

            })
            .on("mouseout", function (d) {
                div.transition()
                    .duration(500)
                    .style("opacity", 0);
            })


       } else if (enteredData == "") {
                g.selectAll("*").remove();
                        g.selectAll("path")
            .data(topojson.feature(data, data.objects.zip_codes_for_the_usa).features)
            //.data(topojson.feature(data, data.objects.Californiageo).features)
            .enter()
            .append("path")
            .attr("stroke", "#333")
            .attr("class", "counties")
            .attr("class", "zip")
            .attr("fill", d3.rgb(128,128,128))
            //.attr("data-zip", function(d) {return d.properties.id; })
            .attr("data-zip", function (d) {
                return d.properties.zip;
            })
            .attr("data-state", function (d) {
                return d.properties.state;
            })
            .attr("data-name", function (d) {
                return d.properties.name;
            })
            .attr("d", geoPauth)
            .on("mouseover", function (d) {
                console.log("zipcode: " + d.properties.zip + ", city: " + d.properties.name)
                                if (buyRent[d.properties.zip] == undefined) {
                    buyPrice = "$0";
                    rentPrice = "$0";
                } else {
                    buyPrice = buyRent[d.properties.zip].buy;
                    rentPrice = buyRent[d.properties.zip].rent;
                }
                div.transition()
                    .duration(200)
                    .style("opacity", 0.9);
                div.html(
                    "zipcode: " + d.properties.zip + "<br/>" + +
                    "city: " + d.properties.name +
                                                            "buy: " + buyPrice + "<br/>" +
                    "rent: " +  rentPrice
                )
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY + 28) + "px");
            })

       } else {
           console.log("you entered city: " + enteredData)
               // write code to find all the zip codes for the city and ask customer to choose from one?
       }


    /* var zip1 = input.property("value");
    if (zip0 === zip1) return;
    zip0 = zip1;

    // Select old canvases to remove after fade.
    var canvas0 = d3.selectAll("canvas");

    // Add a new canvas, initially with opacity 0, to show the new zipcodes.
    var canvas1 = d3.select("#choroplethSVG").insert("canvas", "input")
        .attr("width", width)
        .attr("height", height)
        .style("opacity", 0);

    var context = canvas1.node().getContext("2d");
    context.fillStyle = "#fff";
    context.fillRect(0, 0, width, height);

    // Render the inactive zipcodes.
    context.globalAlpha = .4;
    context.fillStyle = zip1 ? "#aaa" : (zip1 = "*", "#000");
    zipcodes.forEach(function(d) {
      for (var i = 0, n = zip1.length; i < n; ++i) {
        if (d.zip[i] !== zip1[i]) {
          context.fillRect(d.x, d.y, 1, 1);
          return;
        }
      }
    });

    // Render the active zipcodes.
    context.globalAlpha = 1;
    context.fillStyle = "#f00";
    zipcodes.forEach(function(d) {
      for (var i "$=" 0, n = zip1.length; i < n; ++i) {
        if (d.zip[i] !== zip1[i]) {
          return;
        }
      }
      context.fillRect(d.x, d.y, 1, 1);
    });

    // Use a transition to fade-in the new canvas.
    // When this transition finishes, remove the old canvases.
    canvas1.transition()
        .duration(350)
        .style("opacity", 1)
        .each("end", function() { canvas0.remove(); });

     */
  }

    }); // d3.json end

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
	    .attr('transform', 'translate(60,30)')

        gBedroomSlider.call(bedroomSlider);


const SQFT_INCREMENT = 500
var sqftSlider = d3
    .sliderBottom()
    .width(300)
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
	    .attr('transform', 'translate(60,30)')

        gSqftSlider.call(sqftSlider);

function estimateSaleAndRent() {
    console.log("in the estimate fn:")
}
