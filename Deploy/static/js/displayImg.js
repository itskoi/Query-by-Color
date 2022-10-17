var imagePath="./static/images/";
var numberOfImage=40;


function loadImages(image_paths) {
        var parentDIV = document.getElementById("image-grid");
    if (image_paths == -1) {
        // Do nothing
    } else {
        removeAllChildNodes(parentDIV);
        for(var i=0;i<numberOfImage;i++){
            var img= document.createElement('img');
            img.src = imagePath+image_paths[i];
            parentDIV.appendChild(img);
        }
    }
}

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

