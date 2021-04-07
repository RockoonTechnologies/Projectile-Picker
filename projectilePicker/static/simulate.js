
const selectElement = document.getElementById("motor");
selectElement.addEventListener('change', display);

const model =  document.getElementById("name");
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
model.value = urlParams.get('name')

const diam = parseFloat(urlParams.get('diam'))


function search() {
    var input = document.getElementById("motorSearch").value;
    fetch(`https://rocketpicker.herokuapp.com/searchMotor?query=${input}`)
        .then(response => response.json())
        .then(json => {
            results = json;



            selectElement.innerHTML = "";
            for(var x = 0; x < results.length; x++) {
                var item = results[x];
                var option = document.createElement("option");
                option.text = `${item.manufacturerAbbrev}- ${item.commonName}`;
                option.value = JSON.stringify(item);
                selectElement.add(option);
            }

    });
}

function display() {
    var x = document.getElementById("toggle");
    x.style.display = "block";

    var details = document.getElementById("motorInfo");
    var info = JSON.parse(selectElement.value);
    console.log(info);
    details.innerHTML = `Manufacturer: ${info.manufacturer} <br> Name: ${info.commonName} <br> Diameter: ${info.diameter}mm <br> Delays: ${info.delays}`;
    var warn = document.getElementById("warning");
    if(info.diameter !== parseFloat(diam)) {
        warn.innerHTML = "Rocket's motor mount will not support this motor by default";
    }
    else {
     warn.innerHTML = "";
    }
}

var count = 1

function run() {
    var loading = document.getElementById("loading")
    loading.src = "http://cdn.lowgif.com/medium/d35d94c490e598e3-loading-gif-transparent-loading-gif.gif";

    var rName = model.value;
    var values = JSON.parse(selectElement.value)
    var motorName = values.designation;
    var motorManu = values.manufacturerAbbrev;
    fetch(`https://rocketpicker.herokuapp.com/api/simulate?rocketName=${rName}&motorName=${motorName}&motorManu=${motorManu}`)
        .then(response => response.json())
        .then(json => {
            var results = json;
            if(results.Error) {
                alert(results.Error);
                loading.src = "";
                return;
            }
            console.log(results);
            loading.src = "";

            document.getElementById("results").innerHTML = `<h3>Simulation #${count}<h3> <br> Apogee: ${(results.apogee).toFixed(3)}m <br> Total Time (till Apogee): ${(results.totalTime).toFixed(3)}s <br> Burnout Altitude: ${(results.burnoutAltitude).toFixed(3)}m <br> Burnout Velocity: ${(results.burnoutVelocity).toFixed(3)} m/s <br> Coast Altitude: ${(results.coastAltitude).toFixed(3)}m`;
            count++;
    });

}

