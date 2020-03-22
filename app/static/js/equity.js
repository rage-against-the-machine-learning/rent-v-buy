// Select canvases
var svg1 = d3.select("#canvas1");

var	margin = {top: 30, right: 40, bottom: 30, left: 70},
	width = 900 - margin.left - margin.right,
    height = 330 - margin.top - margin.bottom;

var	x = d3.scaleLinear().range([0, width]);
var	y = d3.scaleLinear().range([height, 0]);

var xAxis = d3.axisBottom().scale(x);
var yAxis = d3.axisLeft().scale(y);

var count = Object.keys(myData).length;

var maxEquity = d3.max(myData, function(d) { return Math.max(d.buy, d.rent)*1.2; });
var minEquity = d3.min(myData, function(d) { return Math.min(d.buy, d.rent)*0.8; });

x.domain([0, count-1]);
y.domain([minEquity, maxEquity]);

var	buyLine = d3.line()
	.x(function(d) { return x(d.month); })
	.y(function(d) { return y(d.buy); });
	
var	rentLine = d3.line()
	.x(function(d) { return x(d.month); })
    .y(function(d) { return y(d.rent); });

// Equity build-up plot
var g = svg1.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// X axis
g.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

g.append("text")             
    .attr("transform", "translate(" + (width/2) + " ," + (height + 30) + ")")
    .attr("class", "label")
    .style("text-anchor", "middle")
    .text("Month");

g.append("line")
    .attr("x1", 0)
    .attr("y1", 0)
    .attr("x2", width)
    .attr("y2", 0)
    .style("stroke", "gray")
    .style("stroke-width", 1)
    .style("stroke", "gray")
    .style("shape-rendering", "crispEdges");

// Y axis
g.append("g")
    .attr("class", "y axis")
    .call(yAxis);

g.append("text")
    .attr("transform", "rotate(-90)")
    .attr("class", "label")
    .attr("y", 3 - margin.left)
    .attr("x", 0 - (height / 2))
    .attr("dy", "1em")
    .style("text-anchor", "middle")
    .text("Equity build-up [US$]");

g.append("line")
    .attr("x1", width)
    .attr("y1", 0)
    .attr("x2", width)
    .attr("y2", height)
    .style("stroke", "gray")
    .style("stroke-width", 1)
    .style("stroke", "gray")
    .style("shape-rendering", "crispEdges");

// Shaded areas
g.append("rect")
    .attr("x", 0.)
    .attr("y", 0.)
    .attr("width", x(myData[payOff]["month"]))
    .attr("height", height)
    .style("opacity", 0.1)
    .style("fill", "firebrick");

g.append("rect")
    .attr("x", x(myData[payOff]["month"]))
    .attr("y", 0.)
    .attr("width", width-x(myData[payOff]["month"]))
    .attr("height", height)
    .style("opacity", 0.1)
    .style("fill", "steelblue");

// Dividing line if between the plot

if ((payOff > 5) && (payOff < count - 5)){

    console.log('Printing payoff time');

    g.append("line")
        .attr("x1", x(myData[payOff]["month"]))
        .attr("y1", 0)
        .attr("x2", x(myData[payOff]["month"]))
        .attr("y2", height)
        .style("stroke-width", 2)
        .style("stroke", "gray")
        .style("opacity", 0.9);

    g.append("rect")
        .attr("x", x(myData[payOff]["month"])-130.0)
        .attr("y", 5.0)
        .attr("width", 120.0)
        .attr("height", 20.0)
        .style("opacity", 0.9)
        .style("fill", "gray");

    g.append("line")
        .attr("x1", x(myData[payOff]["month"])-10.0)
        .attr("y1", 15.0)
        .attr("x2", x(myData[payOff]["month"]))
        .attr("y2", 15.0)
        .style("stroke-width", 2)
        .style("stroke", "gray")
        .style("opacity", 0.9);

    g.append("text")
        .attr("x", x(myData[payOff]["month"])-20.0)
        .attr("y", 15.0)
        .attr("dy", ".35em")
        .text("Renting is cheaper")
        .attr("text-anchor", "end")
        .attr("fill", "white");

    g.append("rect")
        .attr("x", x(myData[payOff]["month"])+10.0)
        .attr("y", 15.0)
        .attr("width", 120.0)
        .attr("height", 20.0)
        .style("opacity", 0.9)
        .style("fill", "gray");

    g.append("line")
        .attr("x1", x(myData[payOff]["month"]))
        .attr("y1", 25.0)
        .attr("x2", x(myData[payOff]["month"])+10.0)
        .attr("y2", 25.0)
        .style("stroke-width", 2)
        .style("stroke", "gray")
        .style("opacity", 0.9);

    g.append("text")
        .attr("x", x(myData[payOff]["month"])+20.0)
        .attr("y", 25.0)
        .attr("dy", ".35em")
        .text("Buying is cheaper")
        .attr("fill", "white");
}

// Define the div for the tooltip
var div = d3.select("body").append("div")	
    .attr("class", "tooltip")				
    .style("opacity", 0);

// Label the end of the plots
g.append("text")
    .attr("transform", "translate(" + (width+3) + "," + y(myData[count-1].rent) + ")")
    .attr("dy", ".35em")
    .attr("text-anchor", "start")
    .style("fill", "firebrick")
    .text("Rent");

g.append("text")
    .attr("transform", "translate(" + (width+3) + "," + y(myData[count-1].buy) + ")")
    .attr("dy", ".35em")
    .attr("text-anchor", "start")
    .style("fill", "steelblue")
    .text("Buy");

// Generate line paths
g.append("path")
    .attr("id", "buyLine")
    .attr("d", buyLine(myData));

g.append("g")
    .selectAll()
    .data(myData)
    .enter().append("path")
    .attr("class", "dot")
    .attr("transform", function(d) { return "translate("+x(d.month)+","+y(d.buy)+")"; })
    .attr('d', d3.symbol().type( d3.symbolSquare ).size( 3.0 ) )
    .attr("id", "buyScatter")
    .on("mouseover", function(d) {		
        div.transition()		
            .duration(200)		
            .style("opacity", .9);		
        div	.html("Month: " + d.month + "<br/>" + "Buy: " + Math.round(d.buy) + "<br/>" + "Rent: " + Math.round(d.rent) )	
            .style("left", x(d.month) + "px")		
            .style("top", y(d.buy)+ "px");	
        })					
    .on("mouseout", function(d) {		
        div.transition()		
            .duration(500)		
            .style("opacity", 0);	
    });

g.append("path")
    .attr("id", "rentLine")
    .attr("d", rentLine(myData));

g.append("g")
    .selectAll()
    .data(myData)
    .enter().append("path")
    .attr("class", "dot")
    .attr("transform", function(d) { return "translate("+x(d.month)+","+y(d.rent)+")"; })
    .attr('d', d3.symbol().type( d3.symbolSquare ).size( 3.0 ) )
    .attr("id", "rentScatter")
    .on("mouseover", function(d) {		
        div.transition()		
            .duration(200)		
            .style("opacity", .9);		
        div	.html("Month: " + d.month + "<br/>" + "Buy: " + Math.round(d.buy) + "<br/>" + "Rent: " + Math.round(d.rent) )	
            .style("left", x(d.month) + "px")		
            .style("top", y(d.rent)+ "px");	
        })					
    .on("mouseout", function(d) {		
        div.transition()		
            .duration(500)		
            .style("opacity", 0);	
    });

// Simple
var down_payment_data = [0.0, 25000.0, 50000.0, 75000.0, 100000.0];
var downPaymentSlider = d3
    .sliderBottom()
    .min(d3.min(down_payment_data))
    .max(d3.max(down_payment_data))
    .width(300)
    .tickFormat(d3.format('($d'))
    .ticks(5)
    .default(50000.0)
    .on('onchange', val => {
        d3.select('p#value-down-payment').text(d3.format('($d')(val));
    });

var gSimple = d3
    .select('div#slider-down-payment')
    .append('svg')
    .attr('width', 500)
    .attr('height', 100)
    .append('g')
    .attr('transform', 'translate(30,30)');

gSimple.call(downPaymentSlider);
d3.select('p#value-down-payment').text(d3.format('($d')(downPaymentSlider.value()));

var mortgage_interest_data = [0.01, 0.03, 0.05, 0.07, 0.09];
var mortgageRateSlider = d3
    .sliderBottom()
    .min(d3.min(mortgage_interest_data))
    .max(d3.max(mortgage_interest_data))
    .width(300)
    .tickFormat(d3.format('.2%'))
    .ticks(5)
    .default(0.037)
    .on('onchange', val => {
        d3.select('p#value-mortgage-interest').text(d3.format('.2%')(val));
    });

var gSimple = d3
    .select('div#slider-mortgage-interest')
    .append('svg')
    .attr('width', 500)
    .attr('height', 100)
    .append('g')
    .attr('transform', 'translate(30,30)');

gSimple.call(mortgageRateSlider);
d3.select('p#value-mortgage-interest').text(d3.format('.2%')(mortgageRateSlider.value()));

var annual_maintenance_data = [0.0, 1000.0, 2000.0, 3000.0, 4000.0, 5000.0];
var maintenanceSlider = d3
    .sliderBottom()
    .min(d3.min(annual_maintenance_data))
    .max(d3.max(annual_maintenance_data))
    .width(300)
    .tickFormat(d3.format('($d'))
    .ticks(5)
    .default(1000.0)
    .on('onchange', val => {
        d3.select('p#value-annual-maintenance').text(d3.format('($d')(val));
    });

var gSimple = d3
    .select('div#slider-annual-maintenance')
    .append('svg')
    .attr('width', 500)
    .attr('height', 100)
    .append('g')
    .attr('transform', 'translate(30,30)');

gSimple.call(maintenanceSlider);
d3.select('p#value-annual-maintenance').text(d3.format('($d')(maintenanceSlider.value()));

var annual_home_insurance_data = [0.0, 500.0, 1000.0, 1500.0, 2000.0];
var homeInsuranceSlider = d3
    .sliderBottom()
    .min(d3.min(annual_home_insurance_data))
    .max(d3.max(annual_home_insurance_data))
    .width(300)
    .tickFormat(d3.format('($d'))
    .ticks(5)
    .default(1000.0)
    .on('onchange', val => {
        d3.select('p#value-annual-home-insurance').text(d3.format('($d')(val));
    });

var gSimple = d3
    .select('div#slider-annual-home-insurance')
    .append('svg')
    .attr('width', 500)
    .attr('height', 100)
    .append('g')
    .attr('transform', 'translate(30,30)');

gSimple.call(homeInsuranceSlider);
d3.select('p#value-annual-home-insurance').text(d3.format('($d')(homeInsuranceSlider.value()));