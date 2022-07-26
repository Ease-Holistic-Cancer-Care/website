function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

$("#specialty_id").on('change', function () {
    var id = $(this).find('option:selected').attr('id');
    var url = document.URL;
    var domain = url.split('/')[0] + "//" + url.split('/')[2] + "/";
    data = httpGet(domain + "getSpecialty/" + String(id) + "/");
    data = data.split('", "');
    temp_data = data[0].split(', \"')
    data[0] = temp_data[1]
    data = [temp_data[0]].concat(data)
    data[data.length - 1] = data[data.length - 1].replaceAll('\"]', "")
    document.getElementById("specialty_name").value = data[1];
    document.getElementById("specialty_description").innerText = data[2];
    document.getElementById("specialty_image").src = data[3]
});