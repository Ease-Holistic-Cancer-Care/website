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
    var checkBox = document.getElementById("is_head");
    var heading = document.getElementById("news_heading");
    data = httpGet(domain + "getNews/" + String(id) + "/");
    data = data.split('", "');
    data[data.length - 1] = data[data.length - 1].replaceAll('\"]', "")
    data[0] = data[0].replaceAll('[\"', "")
    if (data.length == 3) {

        document.getElementById("news_title").value = data[0];
        document.getElementById("news_description").innerText = data[1];
        document.getElementById("news_image").src = data[2]
        checkBox.checked = false;
        heading.style.display = "none";
        heading.required = false;
        heading.disabled = true;
        document.getElementById("heading_news").style.display = "none";
        document.getElementById("news_heading").value = "";
    }
    else if (data.length == 4) {

        document.getElementById("news_title").value = data[0];
        document.getElementById("news_description").innerText = data[1];
        document.getElementById("news_heading").value = data[2];
        document.getElementById("news_image").src = data[3]
        checkBox.checked = true;
        heading.style.display = "block";
        heading.required = true;
        heading.disabled = false;
        document.getElementById("heading_news").style.display = "block";
    }
});