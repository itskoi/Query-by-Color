var canvasSize = 200,
    lineWidth=2,
    rows = 4,
    cols = 4;

var boxSize = parseInt(Math.floor(canvasSize/rows));

var cells = new Array(rows * cols).fill(-1);
var global_cell = -1;
var selected_color = "";

function hex2rgb(hex) {
  return ['0x' + hex[1] + hex[2] | 0, '0x' + hex[3] + hex[4] | 0, '0x' + hex[5] + hex[6] | 0];
}

function drawBox(reset) {
    var canvas1 = document.getElementById("canvas1"),
        c1 = canvas1.getContext("2d");
    var canvas2 = document.getElementById("canvas2"),
        c2 = canvas2.getContext("2d");

    if (reset != true) {
        canvas1.addEventListener('click', (e) => handleClick(e, c1));
    } else {
        cells = new Array(rows * cols).fill(-1);
    }

    // Draw local rects
    c1.beginPath();
    c1.fillStyle = "white";
    c1.lineWidth = lineWidth;
    c1.strokeStyle = 'black';

    for (var row = 0; row < rows; row++) {
        for (var column = 0; column < cols; column++) {
          var x = column * boxSize;
          var y = row * boxSize;
          c1.rect(x, y, boxSize, boxSize);
          c1.fill();
          c1.stroke();
        }
    }
    c1.closePath();

    // Draw global rect
    c2.beginPath();
    c2.fillStyle = "white";
    c2.lineWidth = lineWidth;
    c2.strokeStyle = 'black';

    c2.rect(0, 0, boxSize, boxSize);
    c2.fill();
    c2.stroke();

    c2.closePath();
}

function handleClick(e, c) {
    var posx = Math.floor(e.offsetX / boxSize),
        posy = Math.floor(e.offsetY / boxSize);

    console.log(posx, posy)

    if (posx >= 0 && posx < cols) {
        if (posy >= 0 && posy < rows) {
            var id = parseInt(posx+cols*posy); 

            if (cells[id] != -1) {
                cells[id] = -1;
                c.fillStyle = "white";
            } else {
                // Save color
                cells[id] = selected_color;
                c.fillStyle = selected_color;
            }

            // Update color
            c.fillRect(posx * boxSize, posy * boxSize, boxSize, boxSize);
            c.stroke();
        }
    }
}

function queryColor() {
    let global_color = document.getElementById("checkbox").checked;

    if (global_color == true) {
        fetch(`${window.origin}/global_color`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(selected_color),
        cache: "no-cache",
        headers: new Headers({
          "content-type": "application/json"
          })
        }).then(response=>response.json()).then(data=>{
            console.log(data);
            loadImages(data);
        })
    } else {
        fetch(`${window.origin}/local_color`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(cells),
        cache: "no-cache",
        headers: new Headers({
          "content-type": "application/json"
          })
        }).then(response=>response.json()).then(data=>{
            console.log(data);
            loadImages(data);
        })
    }
}

// Create a new color picker instance
// https://iro.js.org/guide.html#getting-started
var colorPicker = new iro.ColorPicker(".colorPicker", {
  // color picker options
  // Option guide: https://iro.js.org/guide.html#color-picker-options
  width: 200,
  color: "rgb(255, 0, 0)",
  borderWidth: 1,
  borderColor: "#fff",
});

colorPicker.on(["color:init"], (color)=>selected_color=color.rgbString);


colorPicker.on(["color:change"], function(color){

    //console.log(color.rgbString);
    selected_color = color.rgbString;

    // Update global color
    var canvas2 = document.getElementById("canvas2"),
        c2 = canvas2.getContext("2d");

    c2.fillStyle = selected_color;
    c2.fillRect(0, 0, boxSize, boxSize);
    c2.stroke();
  
});

