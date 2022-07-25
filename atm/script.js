var message = document.getElementById("message");
var bedrag = document.getElementById("bedrag");

fetch("./data.json")
.then(response => {
    return response.json();
})
.then(data => display(data));


function display(data){
    message.innerHTML = data.message
    bedrag.innerHTML = data.bedrag
}