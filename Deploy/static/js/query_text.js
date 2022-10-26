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
        loadImages(data);
    })
} 

function clearText() {
    let textinput = document.getElementById("textinput");

    textinput.value = ''
}

function copy2Clipboard() {
    let textarea = document.getElementById('textarea');
    navigator.clipboard.writeText(textarea.value);
}

function extractCSV() {
    //TODO: IMPLEMENT THIS
    console.log('EXTRACT CSV');
    let textarea = document.getElementById('textarea');
    var fileContents = JSON.stringify(textarea.value, null, 2);
    var fileName = "query.csv";

    var pp = document.createElement('a');
    pp.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(fileContents));
    pp.setAttribute('download', fileName);
    pp.click();
}
