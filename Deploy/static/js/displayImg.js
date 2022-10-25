var imagePath="./static/images/";
var numberOfImage=100;

let selectedImgs = []


function onclickImg(img) {
    let textarea = document.getElementById('textarea');
    if (!img.classList.contains("clickedImg")) {
        img.classList.add('clickedImg');

        textarea.value += img.title+'\n';
    } else {
        img.classList.remove('clickedImg');

        textarea.value = textarea.value.replace(img.title+'\n', '')
    }

}

function resetSelect() {
    var selectedImgs = document.querySelectorAll(".clickedImg");
    for (var i = 0; i < selectedImgs.length; i++) {
        selectedImgs[i].click();
    }
}

function selectAll() {
    let images = document.getElementsByTagName("img");
    for (var i = 0; i < images.length; i++) {
        images[i].click();
    }
}

function loadImages(image_paths) {
        var parentDIV = document.getElementById("image-grid");
    if (image_paths == -1) {
        // Do nothing
    } else {
        removeAllChildNodes(parentDIV);
        for(var i=0;i< Math.min(numberOfImage, image_paths.length);i++){
            var img= document.createElement('img');
            img.src = imagePath+image_paths[i];
            img.title=image_paths[i];
            img.addEventListener("click", function() {onclickImg(this);});
            parentDIV.appendChild(img);
        }
    }
}

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

