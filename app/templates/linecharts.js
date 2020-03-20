// Select canvases
var svg1 = d3.select("#canvas1");

var	margin = {top: 30, right: 40, bottom: 30, left: 50},
	width = 600 - margin.left - margin.right,
	height = 270 - margin.top - margin.bottom;


var	x = d3.scaleLinear().range([0, width]);
var	y = d3.scaleLinear().range([height, 0]);

var xAxis = d3.axisBottom().scale(x);
var yAxis = d3.axisLeft().scale(y);

// To be replaced by JSON from Python
var myData = [
    {"month": 0, "buy": 68.13, "rent": 34.12},
    {"month": 1, "buy": 63.98, "rent": 45.56},
    {"month": 2, "buy": 67.00, "rent": 67.89},
    {"month": 3, "buy": 89.70, "rent": 78.54},
    {"month": 4, "buy": 99.00, "rent": 89.23},
    {"month": 5, "buy": 130.28, "rent": 99.23},
    {"month": 6, "buy": 166.70, "rent": 101.34},
    {"month": 7, "buy": 234.98, "rent": 122.34},
    {"month": 8, "buy": 345.44, "rent": 134.56},
    {"month": 9, "buy": 443.34, "rent": 160.45},
    {"month": 10, "buy": 543.70, "rent": 180.34},
    {"month": 11, "buy": 580.13, "rent": 210.23},
    {"month": 12, "buy": 605.23, "rent": 223.45},
    {"month": 13, "buy": 622.77, "rent": 201.56},
    {"month": 14, "buy": 626.20, "rent": 212.67},
    {"month": 15, "buy": 628.44, "rent": 310.45},
    {"month": 16, "buy": 636.23, "rent": 350.45},
    {"month": 17, "buy": 633.68, "rent": 410.23},
    {"month": 18, "buy": 624.31, "rent": 430.56},
    {"month": 19, "buy": 629.32, "rent": 460.34},
    {"month": 20, "buy": 618.63, "rent": 510.34},
    {"month": 21, "buy": 599.55, "rent": 534.23},
    {"month": 22, "buy": 609.86, "rent": 578.23},
    {"month": 23, "buy": 617.62, "rent": 590.12},
    {"month": 24, "buy": 614.48, "rent": 560.34},
    {"month": 25, "buy": 606.98, "rent": 580.12}
];

var payOff = 10;

var count = Object.keys(myData).length;
var maxEquity = d3.max(myData, function(d) { return Math.max(d.buy, d.rent); });

x.domain([0, count-1]);
y.domain([0, maxEquity]);

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

// Label the end of the plots
g.append("text")
    .attr("transform", "translate(" + (width+3) + "," + y(myData[count-1].rent) + ")")
    .attr("dy", ".35em")
    .attr("text-anchor", "start")
    .style("fill", "red")
    .text("Rent");

g.append("text")
    .attr("transform", "translate(" + (width+3) + "," + y(myData[count-1].buy) + ")")
    .attr("dy", ".35em")
    .attr("text-anchor", "start")
    .style("fill", "steelblue")
    .text("Buy");

// Generate line paths
g.append("path")
    .attr("class", "line")
    .attr("d", buyLine(myData));

g.append("path")
    .attr("class", "line")
    .style("stroke", "red")
    .attr("d", rentLine(myData));	