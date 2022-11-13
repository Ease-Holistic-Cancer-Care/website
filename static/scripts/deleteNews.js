function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

$("#news_id").on('change', function () {
    var id = $(this).find('option:selected').attr('id');
    var url = document.URL;
    var domain = url.split('/')[0] + "//" + url.split('/')[2] + "/";
    data = httpGet(domain + "getNews/" + String(id) + "/");
    data = data.split('", "');
    data[data.length - 1] = data[data.length - 1].replaceAll('\"]', "")
    data[0] = data[0].replaceAll('[\"', "")

    document.getElementById("news_title").value = data[0];
    document.getElementById("news_description").innerText = data[1];
    document.getElementById("news_image").src = data[2]
});