// Select canvases
var svg1 = d3.select("#canvas1");

var	margin = {top: 30, right: 40, bottom: 30, left: 50},
	width = 900 - margin.left - margin.right,
    height = 330 - margin.top - margin.bottom;

var	x = d3.scaleLinear().range([0, width]);
var	y = d3.scaleLinear().range([height, 0]);

var xAxis = d3.axisBottom().scale(x);
var yAxis = d3.axisLeft().scale(y);

var count = Object.keys(myData).length;
var maxEquity = d3.max(myData, function(d) { return Math.max(d.buy, d.rent)*1.2; });

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
    .style("opacity", 0.15)
    .style("fill", "steelblue");

g.append("rect")
    .attr("x", x(myData[payOff]["month"]))
    .attr("y", 0.)
    .attr("width", width-x(myData[payOff]["month"]))
    .attr("height", height)
    .style("opacity", 0.15)
    .style("fill", "firebrick");

// Dividing line if between the plot

if ((payOff > 5) && (payOff < count - 5)){

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
    .attr('d', d3.symbol().type( d3.symbolCircle ).size( 10.0 ) )
    .attr("id", "buyScatter")
    .on("mouseover", function(d) {		
        div.transition()		
            .duration(200)		
            .style("opacity", .9);		
        div	.html("Month: " + d.month + "<br/>" + "Buy :" + d.buy + "<br/>" + "Rent :" + d.rent )	
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
    .attr('d', d3.symbol().type( d3.symbolCircle ).size( 10.0 ) )
    .attr("id", "rentScatter")
    .on("mouseover", function(d) {		
        div.transition()		
            .duration(200)		
            .style("opacity", .9);		
        div	.html("Month: " + d.month + "<br/>" + "Buy :" + d.buy + "<br/>" + "Rent :" + d.rent )	
            .style("left", x(d.month) + "px")		
            .style("top", y(d.rent)+ "px");	
        })					
    .on("mouseout", function(d) {		
        div.transition()		
            .duration(500)		
            .style("opacity", 0);	
    });  