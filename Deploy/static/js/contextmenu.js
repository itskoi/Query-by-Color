//var contextMenu = CtxMenu('.image');

//contextMenu.addItem("Open youtube video", function(){
    //console.log(this);
//}, icon="./static/icons/youtube.svg");

function oncontextmenu() {
    console.log("HELLO WORLD!");
}

let menu = null;
document.addEventListener('DOMContentLoaded', function(){
    //make sure the right click menu is hidden
    menu = document.querySelector('.menu');
    menu.classList.add('off');
    
    //add the right click listener to the box
    //let box = document.getElementById('contextmenu');
    //box.addEventListener('contextmenu', showmenu);
    
    //add a listener for leaving the menu and hiding it
    menu.addEventListener('mouseleave', hidemenu);
    
    //add the listeners for the menu items
    //addMenuListeners();
});

function addMenuListeners(img){
    let youtube_option = document.getElementById('youtube');
    let metadata_option = document.getElementById('metadata');
    // Add the new one
    //youtube_option.addEventListener('click', function(ev) { setLink(ev, img); });
    youtube_option.onclick = function(ev) { setLink(ev, img); };
    metadata_option.onclick = function(ev) { setMetadata(ev, img); };
}

function setMetadata(ev, img) {
    console.log(img);
    hidemenu();
}

function setLink(ev, img){
    console.log(img);
    hidemenu();
}

function showmenu(ev, img){
    addMenuListeners(img);
    //stop the real right click menu
    ev.preventDefault(); 
    //show the custom menu
    menu.style.top = `${ev.clientY - 20}px`;
    menu.style.left = `${ev.clientX - 20}px`;
    menu.classList.remove('off');
}

function hidemenu(ev){
    menu.classList.add('off');
    menu.style.top = '-200%';
    menu.style.left = '-200%';
}


