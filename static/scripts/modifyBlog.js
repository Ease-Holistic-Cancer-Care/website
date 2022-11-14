function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

$("#blog_id").on('change', function () {
    var id = $(this).find('option:selected').attr('id');
    var url = document.URL;
    var domain = url.split('/')[0] + "//" + url.split('/')[2] + "/";
    data = httpGet(domain + "getBlogContent/" + String(id) + "/");
    data = data.split('", "');
    data[data.length - 1] = data[data.length - 1].replaceAll('\"]', "")
    data[0] = data[0].replaceAll('[\"', "")
    data[2] = data[2].split('\\r\\n\\r\\n')
    if (data[2].length == 1) {
        data[2] = data[2][0].split('\\n\\n')
    }
    console.log(data)
    document.getElementById("blog_title").value = data[0];
    document.getElementById("blog_description").innerText = data[1];
    document.getElementById("blog_content").value = "";
    for (i = 0; i < data[2].length; i++) {
        if (i == data[2].length - 1)
            document.getElementById("blog_content").value += data[2][i];
        else
            document.getElementById("blog_content").value += data[2][i] + "\n\n"
    }
    document.getElementById("blog_image").src = data[3]
});