"use strict";

let app = angular.module("Educacion",[]);

app.controller("MainController",function($scope){
    var self = $scope;
    self.page = 1;

    self.setPage = (i) => {
    	self.page = i;
    };

    createGraph("#hola","data/resultado_alto.csv","#ff8323");
    createGraph("#hola2","data/resultado_bajo.csv","#485");

});

let createGraph = (div,dataset,color) => {
	var margin = {top: 20, right: 20, bottom: 80, left: 60},
    width = 800 - margin.left - margin.right,
    height = 420 - margin.top - margin.bottom;

	var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);

	var y = d3.scale.linear().range([height, 0]);

	var xAxis = d3.svg.axis()
	    .scale(x)
	    .orient("bottom");

	var yAxis = d3.svg.axis()
	    .scale(y)
	    .orient("left")
	    .ticks(10);

	var tooltip = d3.select(div).append("div")
		.attr("class", "tooltip")
		.style("opacity", 0);

	var svg = d3.select(div).append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", 
	          "translate(" + margin.left + "," + margin.top + ")");

    svg.on("mouseout",function(){
    	tooltip.style("opacity",0);
    });

	d3.csv(dataset, function(error, data) {
	  data = data.sort(function(a,b){return b.confidence - a.confidence;});
	  x.domain(data.map(function(d) { return d.lhs+"=>"+d.rhs; }));
	  y.domain([0.40, 0.60]);

	  svg.selectAll("bar")
	      .data(data)
	    .enter().append("rect")
	      .style("fill", color)
	      .attr("x", function(d) { return x(d.lhs+"=>"+d.rhs); })
	      .attr("width", x.rangeBand())
	      .attr("y", function(d) { return y(d.confidence); })
	      .attr("height", function(d) { return height - y(d.confidence);})
	      .on("mouseover",function(d){
	      		tooltip.style("opacity",0.95);
	      		tooltip.html(getContent(d))
	      			.style("left", (d3.event.pageX + 10) + "px")
					.style("top", (d3.event.pageY - 58) + "px");
	      })
	      .on("mouseout",function(d){
	      		tooltip.attr("opacity",0);
	      });

	   svg.append("g")
	      .attr("class", "x axis")
	      .attr("transform", "translate(0," + height + ")")
	      .call(xAxis)
	    .selectAll("text")
	      .style("text-anchor", "end")
	      .attr("dx", "-.8em")
	      .attr("dy", "-.55em")
	      .attr("transform", "rotate(-90)" );

	  svg.append("g")
	      .attr("class", "y axis")
	      .call(yAxis)
	    .append("text")
	      .attr("transform", "rotate(-90)")
	      .attr("y", 6)
	      .attr("dy", ".71em")
	      .style("text-anchor", "end")
	      .text("confidence");

	});

};


let getContent = (d) => {
	return "<strong>Regla:</strong><br>"+d.lhs.replace(/,/g,", ")+"=>"+d.rhs+"<br>" +
		"<strong>Support:</strong> "+d.support+"<br>" +
		"<strong>Confidence:</strong> "+d.confidence+"<br>"+
		"<strong>Lift:</strong><br> "+d.lift; 
}


