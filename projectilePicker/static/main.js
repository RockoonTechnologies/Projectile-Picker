var totalList = [];

var allManufacturers = ["ALL"];
var allDiams = ["ALL"];
var allLevels = ["ALL","LPR", "MPR", "HPR"];
var allMotors = ["ALL"];
var allMaterials = ["ALL"];

window.onload = function() {

    fetch('https://rocketpicker.herokuapp.com/api/main')
        .then(response => response.json())
        .then(json => {
            totalList = json.data;


            for(var x = 0; x < totalList.length; x++) {
                var item = totalList[x];

                var manu = item.manufacturer;
                var diam = item.diameter;
                var motor = item.motor;
                var mat = item.material;
                if(allManufacturers.includes(manu) == false) {
                    allManufacturers.push(manu)
                }
                if(allDiams.includes(diam) == false) {
                    allDiams.push(diam.toString() + `mm | ${(diam / 25.4).toFixed(2)} in`);
                }
                if(allMotors.includes(motor) == false) {
                    allMotors.push(motor);
                }
                if(allMaterials.includes(mat) == false) {
                    allMaterials.push(mat)
                }



            }

            buildHtmlTable('#data', makeTablePretty(totalList));

            addOptions("manu", allManufacturers);
            addOptions("motor", allMotors);
            addOptions("diam", allDiams);
            addOptions("level", allLevels);
            addOptions("material", allMaterials);

    });
}

function makeTablePretty(baseArray) {

    let dup = JSON.parse(JSON.stringify(baseArray));

    for(var x = 0; x < baseArray.length; x++) {
        var item = dup[x];


        item.name = `<a onclick="modalOn('${item.name}');">${item.name}</a>`;
        delete item.url;

        item.img = `<img src=${item.img} width="100" height="auto">`;
        item.material = "N/A";
    }
    return dup;
}


function addOptions(select, array) {
    var s = document.getElementById(select);
    for(var x = 0; x < array.length; x++) {
        var option = document.createElement("option");
        option.text = array[x];
        s.add(option);
    }

}

function buildHtmlTable(selector, array) {
  document.getElementById("amount").innerText = "Found " + array.length.toString() + " results";
  var columns = addAllColumnHeaders(array, selector);

  for (var i = 0; i < array.length; i++) {
    var row$ = $('<tr/>');
    for (var colIndex = 0; colIndex < columns.length; colIndex++) {
      var cellValue = array[i][columns[colIndex]];

      if (cellValue == null) cellValue = "";

      row$.append($('<td/>').html(cellValue));

    }
    $(selector).append(row$);
  }
}

function addAllColumnHeaders(totalList, selector) {
  var columnSet = [];
  var headerTr$ = $('<tr/>');

  for (var i = 0; i < totalList.length; i++) {
    var rowHash = totalList[i];
    for (var key in rowHash) {
      if ($.inArray(key, columnSet) == -1) {
        columnSet.push(key);

        headerTr$.append($('<th/>').html(key));
      }
    }
  }
  $(selector).append(headerTr$);

  return columnSet;
}

function resolveSelect(selector) {


    var e = document.getElementById(selector);
    var value = e.options[e.selectedIndex].value;

    var text = e.options[e.selectedIndex].text;
    if(text.includes("mm")) {
        text = text.split(" ")[0].replace("mm", "");

    }
    return text;
}

var attributes = []
function update() {
    var Smotor = resolveSelect("motor");
    var Sdiameter = resolveSelect("diam");
    var Smanu = resolveSelect("manu");
    var Slevel = resolveSelect("level");
    var Smaterial = resolveSelect("material");

    var tdH = document.getElementById("tdH").value;
    var tdL = document.getElementById("tdL").value;

    var mdH = document.getElementById("mdH").value;
    var mdL = document.getElementById("mdL").value;

    var searchQuery = document.getElementById("search").value;

    newList = [];

     for(var x = 0; x < totalList.length; x++) {
           var item = totalList[x];

           var manu = item.manufacturer;
           var diam = item.diameter.toString();
           var motor = item.motor.toString();
           var level = item.level;
           var mat = item.material;
           var name = item.name;

           var canAdd = true;

           if(manu !== Smanu && Smanu !== "ALL") {

              canAdd = false;
           }
           if(diam !== Sdiameter && Sdiameter !== "ALL")
           {
              canAdd = false;
           }
           if(material !== Smaterial && Smaterial !== "ALL")
           {
              canAdd = false;
           }
           if(motor !== Smotor && Smotor !== "ALL")
           {
              canAdd = false;
           }
           if(level !== Slevel && Slevel !== "ALL")
           {
              canAdd = false;
           }

           diam = parseFloat(diam);
           motor = parseFloat(motor);

           if(tdH && tdL) {
                if(diam >= tdH || diam <= tdL) {
                    canAdd = false;
                }
           }
           if(mdH && mdL) {
                if(motor >= mdH || motor <= mdL) {
                    canAdd = false;
                }
           }

           if(searchQuery) {
                if(stringSimilarity.compareTwoStrings(searchQuery, name) < 0.5) {
                    canAdd = false;
                }
           }

           if(canAdd) {
                newList.push(item);
           }


     }
     var Table = document.getElementById("data");
     Table.innerHTML = "";
     buildHtmlTable('#data', makeTablePretty(newList));
}

function rocketFromName(name) {
     for(var x = 0; x < totalList.length; x++) {
        console.log(totalList[x].name);
        if(totalList[x].name === name) {
            return totalList[x];
        }
     }
}

//---------------------- MODEL STUFF


var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];


function modalOn(name) {
  modal.style.display = "block";
  data = rocketFromName(name);
  document.getElementById("modelTitle").innerHTML = data.name;
  document.getElementById("modalPrice").innerHTML = "$" + data.price;
  document.getElementById("details").innerHTML = `Manufacturer: ${data.manufacturer} <br> Uses a ${data.diameter}mm (${(data.diameter / 25.4).toFixed(2)} in) airframe, made of ${data.material} <br> Motor Type: ${data.motor} mm <br> Level: ${data.level}`;
  document.getElementById("zoom").src = data.img;
  document.getElementById("more").href = data.url;
  document.getElementById("sim").href = `/sim?name=${data.name}&diam=${data.motor}`;
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
