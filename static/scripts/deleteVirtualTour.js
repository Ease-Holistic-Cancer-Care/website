function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

$("#virtual_tour_id").on('change', function () {
    var id = $(this).find('option:selected').attr('id');
    var url = document.URL;
    var domain = url.split('/')[0] + "//" + url.split('/')[2] + "/";
    data = httpGet(domain + "getVirtualTour/" + String(id) + "/");
    data = data.split('", "');
    console.log(data);
    data[data.length - 1] = data[data.length - 1].replaceAll('\"]', "")
    data[0] = data[0].replaceAll('[\"', "")

    document.getElementById("virtual_tour_title").value = data[0];
    document.getElementById("virtual_tour_description").innerText = data[1];
    document.getElementById("virtual_tour_image").src = data[2]
});