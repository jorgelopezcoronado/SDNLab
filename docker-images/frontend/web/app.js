fetch('http://localhost:8888/')
.then(function (response) {
    return response.json();
})
.then(function (json) {
    document.querySelector("#msg").innerHTML = json.msg;
    document.querySelector("#lang").innerHTML = '<i>-' + json.language + '</i>';
})
.catch(error => {
    console.log("Fetching trees data failed", error);
});

