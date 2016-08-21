var fs = require('fs');
var Service, Characteristic;
var request = require('request');
var parseString = require('xml2js').parseString;

module.exports = function(homebridge) {
  Service = homebridge.hap.Service;
  Characteristic = homebridge.hap.Characteristic;

  homebridge.registerAccessory("homebridge-temperature-ganglia", "TemperatureGanglia", TemperatureGangliaAccessory);
}

function TemperatureGangliaAccessory(log, config) {
  this.log = log;
  this.name = config["name"];
  log("OLI")
  console.log("OLI")
  

  this.service = new Service.TemperatureSensor(this.name);

  this.service
    .getCharacteristic(Characteristic.CurrentTemperature)
    .on('get', this.getState.bind(this));
}

TemperatureGangliaAccessory.prototype.getState = function(callback) {
	request('http://127.0.0.1:8652/Housenet/pi', function (error, response, body) {
	  if (!error && response.statusCode == 200) {
		  parseString(body, function (err, result) {
			  var metrics = result['GANGLIA_XML']['GRID'][0]['CLUSTER'][0]['HOST'][0]['METRIC']
			  for (var item in metrics) {
				  if ( metrics[item]['$']['NAME'] == 'Temperature' ) {
					  console.log("Temperature is: " + metrics[item]['$']['VAL'])
					  callback(null, parseFloat(metrics[item]['$']['VAL']))
				  }
			  }
		  });
	  }
	})
}

TemperatureGangliaAccessory.prototype.getServices = function() {
  return [this.service];
}
