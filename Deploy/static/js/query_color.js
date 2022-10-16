var canvasSize = 200,
    lineWidth=2,
    rows = 4,
    cols = 4;

var boxSize = parseInt(Math.floor(canvasSize/rows));

var cells = new Array(rows * cols).fill(-1);
var selected_color = "";

function hex2rgb(hex) {
  return ['0x' + hex[1] + hex[2] | 0, '0x' + hex[3] + hex[4] | 0, '0x' + hex[5] + hex[6] | 0];
}

function drawBox(reset) {
    var canvas = document.getElementById("canvas"),
        c = canvas.getContext("2d");
    if (reset != true) {
        canvas.addEventListener('click', (e) => handleClick(e, c));
    }

    c.beginPath();
    c.fillStyle = "white";
    c.lineWidth = lineWidth;
    c.strokeStyle = 'black';
    for (var row = 0; row < rows; row++) {
        for (var column = 0; column < cols; column++) {
          var x = column * boxSize;
          var y = row * boxSize;
          c.rect(x, y, boxSize, boxSize);
          c.fill();
          c.stroke();
        }
    }
    c.closePath();
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
    fetch(`${window.origin}/color`, {
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

colorPicker.on(["color:init", "color:change"], function(color){

  //console.log(color.rgbString);
  selected_color = color.rgbString;
  
});

