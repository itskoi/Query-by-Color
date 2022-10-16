var imagePath="./static/images/";
var numberOfImage=20;

var width = 150, height = 150;


function loadImages(image_paths) {
        var parentDIV = document.getElementById("image-grid");
    if (image_paths == -1) {
        // Do nothing
    } else {
        removeAllChildNodes(parentDIV);
        for(var i=0;i<numberOfImage;i++){
            var img= document.createElement('img');
            img.src = imagePath+image_paths[i];
            img.width = width;
            img.heigth = height;
            parentDIV.appendChild(img);
        }
    }
}

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

