var express = require('express');
var fs 		= require('fs');
var request = require('request');
var cheerio = require('cheerio');
var app     = express();


var courses = ["COMP2270", "ELEC4700", "SENG2130", "ENGG3500"];

console.log("RUNNING--------");
app.get('/', function(req, res){
	for (var i = 0; i < courses.length; i++) {
		getCourseInfo(courses[i]);
	}
});

function getCourseInfo(course) {
	url = "https://spprd.newcastle.edu.au/Scientia/sws2017prd/reports/list.aspx?objects="+course+"/S1_CA&weeks=1-29&days=1-7;1;2;3;4;5;6;7&periods=1-30;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23;24;25;26;27;28;29;30&template=module_list";

	request(url, function(error, response, html){
	    // if(!error){
	        var $ = cheerio.load(html);

		    $('table > tbody').filter(function(){
		        $(this).children("tr").filter(function() {
		        	// console.log("\tTR:" + $(this).children("td").text());
		        	
		        	var type	= $(this).children("td:nth-child(2)").text();
		        	var day   	= $(this).children("td:nth-child(3)").text();
		        	var sTime 	= $(this).children("td:nth-child(4)").text();
		        	var fTime	= $(this).children("td:nth-child(5)").text();

					var compJSON = { "course":course, "type":type , "day":day, "sTime":sTime, "fTime":fTime};
					// Component = namedtuple("Component", "course type day startTime endTime multiplicity")
		        	console.log(JSON.stringify(compJSON));
		        })
		    })
		// }
	}) ;
}

app.listen('8081');
console.log('Listening to 8081...');
exports = module.exports = app;