//------------------------select SVGs -------------------------//


var svg1 = d3.select("#choroplethSVG");
var div = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);// Select canvases
var choroplethSVG = d3.select("#choroplethSVG")
var g = choroplethSVG.append("g")

//------------------------PREPARATION (global vars)-------------------------//


var	margin = {top: 30, right: 40, bottom: 30, left: 70},
    //width = 600 - margin.left - margin.right,
    width = 600,
    //height = 330 - margin.top - margin.bottom;
    height = 330;
var xCoordForLegend = width - margin.left;
var buyRent;
var minAppr = 0;
var maxAppr = 0;
var apprRateArray = []
var colorZip;
var projNew;
var zipCityDict = {};   
var selectedLocation;
var buyPrice = "$0"
var rentPrice = "$0"
var colorShade;
var cleanedApprRate;
var allCAData;
var enteredData = ""
var enteredString = ""
var numRange = []
var rangeSlices

var legend 



//------------------------LOAD DATA-------------------------//

// load in buy,rent and appr rate data, and define the color scale
d3.json("static/maps/UI_output.json", function(d) {
    console.log("[in buyRent json d function ]" +d)
		  return {
		    //buy: +buy,
		    //rent: +rent
		 };
		}).then(function(data) {
		    buyRent = data;
		    //console.log("thenfunction buyrent(keys): " + d3.values(buyRent))
            d3.values(buyRent).forEach(function(d2) {
                apprRateArray.push(cleanApprRate(d2.appr_rate))
                minAppr = d3.min(apprRateArray)
                maxAppr = d3.max(apprRateArray)
                colorZip = d3.scaleThreshold()
                    .domain(d3.range(minAppr,maxAppr))
                    .range(d3.schemeBlues[9])
            })
            })
     


// load in the latitude and longitude for the zipcodes (for map projection)
var zipLatLong = d3.map() ; // array of dicts; e.g. [{"zipcode":75074, "lat":-84, "long":-44}]
    d3.tsv("static/maps/zips.tsv", function(d) {
        //console.log("line is: ", d)
        d.lat = +d.lat;
        d.lon = +d.lon;
        zipLatLong.set(d.zip, d)
    })



// loading california data with a promise. we will use this promise to wait until data is loaded
// before executing certain code (otherwise javascript attempts to thread and render code simultaneaouly
// and you find variables attempted to be used BEFORE the browser has executed on the code to create them

var californiaDataLoadPromise = [
d3.json("static/maps/zips_california_topo-v2.json")
];


//------------------------SET UP MAP PARAMETERS-------------------------//

// define initial default projection, centered at californias lat,long: -120,37
var projectionCA1 = d3.geoMercator()
					   .center([ -120, 37 ])
					   //.translate([ width/2, height/2 +40 ])
                       .translate([ width/2, height/2 ])
					   .scale([ width*2.5 ]);

var fullStateProjection = d3.geoPath().projection(projectionCA1);




//------------------------HELPER FUNCTIONS-------------------------//
function cleanApprRate(d) {
    // takes in the app rate in "2.78%" format from Skye/Sylvias code and 
    // returns a float (2.78)
    // also it chops off the prediction outliers (anything <0 and >20) 
    //as that is throwing off the color shading
    var cleaned = parseFloat(d.substring(0, d.length - 1))

    if (cleaned < 0) {
        cleaned = 0.1
    } else if (cleaned > 20) {
        cleaned = 15
    }
    return parseFloat(cleaned);
}




//------------------------MAIN: RENDER THE MAPS-------------------------//

Promise.all(californiaDataLoadPromise).then(ExecuteMeWhenDataIsLoaded)

// we execute the following code only after the data has been loaded. the promise ensures we 
// serialize these functions in the client browser instead of asynchronous execution.

function ExecuteMeWhenDataIsLoaded([allCAData]) {

    var input = d3.select("#myInput")
        .on("click", change)
        .on("change", change)

    var reset = d3.select("#resetButton")
        .on("click", function(d) {
            console.log("button clicked");
            enteredData = ""
            enteredString = ""
            g.selectAll("*").remove();
            DisplayLegend()
            DisplayMap(allCAData,fullStateProjection,undefined)
            
        })
        

    DisplayMap(allCAData,fullStateProjection,undefined);
    DisplayLegend()

    function DisplayMap(allCAData, projection,d) {
        // the main Display function, displaying a map and sets the zoom parameters based on the projection

        if ((input.property("value") != "") & (typeof d == 'undefined')) {
            //someone entered the location in the field, nothing was clicked
            console.log("[DisplayMap], data in field is: "+input.property("value")+ ",no zip clicked")
            enteredString = input.property("value");
            enteredData = enteredString.substr(enteredString.length - 5);
        } else if ((input.property("value") != "") & (typeof d != 'undefined')) {
            // while there is value in the field, someone clicked, so we give precedence to the clicked zip
            console.log("[DisplayMap], old data in field is: "+input.property("value")+ ",but user clicked on zip: " +d.properties.zip)
            enteredData = d.properties.zip
        } else if ((input.property("value") == "") & (typeof d != 'undefined')) {
            // there was nothing entered in field, but d is defined, which means we received
            // location via the click on the map
            console.log("[DisplayMap], no data in field, user clicked on zip: " +d.properties.zip)
            enteredData = d.properties.zip
        } 

        g.selectAll("path")
            .data(topojson.feature(allCAData, allCAData.objects.zip_codes_for_the_usa).features)
            //.data(topojson.feature(data, data.objects.Californiageo).features)
            .enter()
            .append("path")
            .attr("stroke", "black")
            //.attr("stroke", "#333")
            .attr("fill", function(d) {
                if (d.properties.zip == enteredData) {
                    if (typeof lastSelectedObject != 'undefined') {
                        console.log("[DisplayMap], enteredData " + enteredData + " matches zip")
                        console.log("[DisplayMap] last sel was: "+lastSelectedObject +" , resetting!")
                        lastSelectedObject.style("stroke", "black")
                            .attr("stroke-width", 1)
                            //.attr("fill", d3.rgb(128,128,128))
                    }
                   sel = d3.select(this);
                   lastSelectedObject = sel;
                   console.log("[DisplayMap] sel: "+sel)


                   selectedLocation = d.properties.name + ", CA, " + d.properties.zip

                   if (buyRent[d.properties.zip] == undefined) {
                        buyPrice = "$0";
                        rentPrice = "$0";
                    } else {
                        buyPrice = buyRent[d.properties.zip].buy;
                        rentPrice = buyRent[d.properties.zip].rent;
                    }

                   d.fx = d.x;
                   d.fy = d.y;
                   sel.style("stroke", "orange")
                        .attr("stroke-width", 3)
                        .style("fill", function(d) {
                           return d3.rgb(255,255,255);
                        })

                    //console.log("zoomed inside the fill loop, zip was: "+d.properties.zip+", zipcolor: "+zipColor)
                   fillSelectedLocation(selectedLocation)
                   fillRentEstimate(buyPrice)
                   fillSaleEstimate(rentPrice)
                } else {
                    // check if buyRent has the zip code if not, make colorNumber grey , ie d3.rgb(128,128,128)
                    if (buyRent[d.properties.zip] == undefined) {
                        //colorShade = d3.rgb(128,128,128)
                        colorShade = "#d3d3d3"
                    } else {
                        cleanedApprRate = cleanApprRate(buyRent[d.properties.zip].appr_rate);
                        colorShade = colorZip(cleanedApprRate)
                        //console.log("the colorShare is: " + colorShade)
                    }
                }
                return colorShade
                //return d3.rgb(128,128,128)
            })
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
            .attr("d", projection)
            .on("mouseover", function (d) {

                var buyPrice, rentPrice
                console.log("zipcode: " + d.properties.zip + ", city: " + d.properties.name)
                if (buyRent[d.properties.zip] == undefined) {
                    buyPrice = "$0";
                    rentPrice = "$0";
                    apprRate = "n/a"
                } else {
                    buyPrice = buyRent[d.properties.zip].buy;
                    rentPrice = buyRent[d.properties.zip].rent;
                    apprRate = buyRent[d.properties.zip].appr_rate;
                }
                div.transition()
                    .duration(200)
                    .style("opacity", 0.9);
                div.html(
                    "zipcode: " + d.properties.zip + "<br/>" +
                    "city: " + d.properties.name + "<br/>" +
                    "buy: " + buyPrice + "<br/>" +
                    "rent: " +  rentPrice  + "<br/>" +
                    "appr_rate: " +  apprRate
                )
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY + 28) + "px");
            })
            .on("mouseout", function (d) {
                div.transition()
                    .duration(500)
                    .style("opacity", 0)
            })
            //.on("click", zipClicked);
            .on("click", change);
    }


    function calculateZoomedProjection(zipcode) {
            latitude  = zipLatLong["$"+zipcode].lat;
            longitude = zipLatLong["$"+zipcode].lon
            console.log("[calculateZoomedProjection] zip code: " + zipcode)
            g.selectAll("*").remove();
            console.log("[calculateZoomedProjection] latitude: ", latitude)
            console.log("[calculateZoomedProjection] ongitude: ", longitude)

            projNew = d3.geoMercator()
            .center([ Math.round(longitude), Math.round(latitude) ])
            .translate([ width/2, height/2 ])
            .scale([ width*50.5 ]);

           return d3.geoPath().projection(projNew)
    }

    function change(d) {
       var latitude, longitude;
       console.log("in change()")
       console.log("[change]: input value: "+ input.property("value"))
      //xxx
        if ((input.property("value") != "") & (typeof d == 'undefined')) {
            //someone entered the location in the field, nothing was clicked
            console.log("[change], data in field is: "+input.property("value")+ ",no zip clicked")
            enteredString = input.property("value");
            enteredData = enteredString.substr(enteredString.length - 5);
        } else if ((input.property("value") != "") & (typeof d != 'undefined')) {
            // while there is value in the field, someone clicked, so we give precedence to the clicked zip
            console.log("[change], old data in field is: "+input.property("value")+ ",but user clicked on zip: " +d.properties.zip)
            enteredData = d.properties.zip
        } else if ((input.property("value") == "") & (typeof d != 'undefined')) {
            // there was nothing entered in field, but d is defined, which means we received
            // location via the click on the map
            console.log("[change], no data in field, user clicked on zip: " +d.properties.zip)
            enteredData = d.properties.zip
        } else if ((input.property("value") == "") & (enteredData == "") & (typeof d == 'undefined')) {
            // nothing entered in the field, no d set , thus nothing clicked
            // means if change was called it was called from the input selection with nothing in the field
            // time to reset the map..
            console.log("[change], no value entered in input field, and no zip clicked")
            g.selectAll("*").remove();
            DisplayMap(allCAData,fullStateProjection,undefined)
            DisplayLegend()

        }


       console.log("change(): enteredData: " + enteredData);
       zipRegex = /[0-9]{5}/;

        if (zipRegex.test(enteredData)) {
            console.log("change(): someone clicked on zip: " + enteredData)
            // someone entered data in the field above

            // Show inputs for financial calculations
            finInputs = document.getElementById('financialInputs');            
            finInputs.style.display = "block";
            showingSliders = showSliders(showingSliders);

            zipZoomedProjection = calculateZoomedProjection(enteredData)
            DisplayMap(allCAData,zipZoomedProjection,d);
            DisplayLegend()

     
       }
    }

//------------------------ DISPLAY THE BUY AND RENT AMOUNTS-------------------------//

    function fillSelectedLocation(d) {
        sel = d3.select("#selectedLocationDiv")
        sel.selectAll("*").remove();

        sel.append("text")
            .attr("font-family", "sans-serif")
            .style("font-size", "18px")
            .text(d)
    }

    function fillSaleEstimate(d) {
        sel = d3.select("#saleEstimateDiv")
        sel.selectAll("*").remove();
        sel.append("text")
            .attr("font-family", "sans-serif")
            .style("font-size", "18px")
            .text(d)
    }

    function fillRentEstimate(d) {
        sel = d3.select("#rentEstimateDiv")
        sel.selectAll("*").remove();
        sel.append("text")
            .attr("font-family", "sans-serif")
            .style("font-size", "18px")
            .text(d)
    }



//------------------------ THE LEGEND FUNCTION-------------------------//

function DisplayLegend() {
    legend = g.append('g')
        .attr('class', 'legend')
        .attr("transform", "translate(" + xCoordForLegend  + "," + margin.top + ")")
        .style('fill', "grey");

    legend.selectAll("*").remove();
    numRange = []
    colorRange = 5
    console.log("[Legend] called , colorRange = " + colorRange)
    rangeSlices = Math.round(maxAppr)/colorRange
    //nineRange = d3.range(1,10);
    d3.range(1,colorRange+1).forEach(function(d,i) {
        //console.log("i: ", i)
        if (i == 0) {
            numRange.push(Math.round(minAppr));
        } else {
            //numRange.push(numRange[i-1]+rangeSlices)
            numRange.push(Math.round(rangeSlices*i));
        }
    })


    legend.selectAll("circle")
        .data(numRange) // enter the data
        .enter()
        .append("circle")
        .attr('cx', 0)
        .attr('cy', function(d, i){
            radius = i*18
            console.log("[DisplayLegend] circle radius: " + radius)
            return  radius;
        })
        .attr("r", 7)
        .attr("stroke", "white")
        .style('fill', function(d){
            colorShade = colorZip(d)
            console.log("[DisplayLegend] circle colorShade: " + colorShade)
            return colorShade
                 });

    legend.selectAll('text')
        .data(numRange)
        .enter()
        .append('text')
        .text(function(d,i){
            if (i == 0) {
                return d+"-"+numRange[1]+"%";
            } else if (i == numRange.length-1) {
                return ">" +d+"%";
            } else {
                return d+"-"+numRange[i+1]+"%";
            }

            
            
        })
        .attr('x', 18)
        .attr('y', function(d,i) {
            return i*18+5;
        })

    eqTitle = g.append("text")
        .attr("x", (width - 90)) 
        //.attr("x", xCoordForGatechID)             
        .attr("y", (margin.bottom / 3))
        //.attr("y", yCoordForGatechID)
        .attr("text-anchor", "center")
        .style('fill', "grey")  
        .style("font-size", "10px")
        .text("Appreciation Rate");

    eqNote = g.append("text")
        .attr("x", (width - 90)) 
        //.attr("x", xCoordForGatechID)             
        .attr("y", (120+ margin.bottom / 3))
        //.attr("y", yCoordForGatechID)
        .attr("text-anchor", "center")
        .style('fill', "grey")  
        .style("font-size", "10px")
        .text("Grey = no data");
}

   
       
} // closing promises bracket