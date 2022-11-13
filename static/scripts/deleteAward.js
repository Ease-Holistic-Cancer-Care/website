function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

$("#award_id").on('change', function () {
    var id = $(this).find('option:selected').attr('id');
    var url = document.URL;
    var domain = url.split('/')[0] + "//" + url.split('/')[2] + "/";
    data = httpGet(domain + "getAward/" + String(id) + "/");
    data = data.split('", "');
    data[data.length - 1] = data[data.length - 1].replaceAll('\"]', "")
    data[0] = data[0].replaceAll('[\"', "")

    document.getElementById("award_title").value = data[0];
    document.getElementById("award_type").value = data[1];
    document.getElementById("award_description").innerText = data[2];
    document.getElementById("award_image").src = data[3]
});