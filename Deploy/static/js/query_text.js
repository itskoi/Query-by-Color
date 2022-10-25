function queryText() {
    let textinput = document.getElementById("textinput").value;

    fetch(`${window.origin}/query_text`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(textinput),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json"
      })
    }).then(response=>response.json()).then(data=>{
        console.log(data);
        //loadImages(data);
    })
} 
