var imagePath="./static/dataset/";
var numberOfImage=20;

var width = 200, height = 200;

function loadImages() {
    var parentDIV = document.getElementById("image-grid");

    for(var i=1;i<=numberOfImage;i++){
        var img= document.createElement('img');
        img.src = imagePath+i+'.jpg';
        img.width = width;
        img.heigth = height;
        parentDIV.appendChild(img);
    }
}

