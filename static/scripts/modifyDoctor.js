function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

$("#doctor_id").on('change', function () {
    var id = $(this).find('option:selected').attr('id');
    var url = document.URL;
    var domain = url.split('/')[0] + "//" + url.split('/')[2] + "/";
    data = httpGet(domain + "getDoctor/content/" + String(id) + "/");
    data = JSON.parse(data);
    document.getElementById("doctor_name").value = data[0][1];
    document.getElementById("doctor_current_appointment").value = data[0][2];
    document.getElementById("doctor_image_preview").src = data[0][3];
    document.getElementById("doctor_qualification").value = data[1][0][2];
    document.getElementById("doctor_post_qualification").value = data[1][0][3];
    document.getElementById("doctor_overseas_qualification").value = data[1][0][4];
    document.getElementById("doctor_about").innerText = data[1][0][5];
    for (var i = 0; i < data[2].length; i++) {
        document.getElementById("doctor_degree" + String(i + 1)).value = data[2][i][1];
        document.getElementById("doctor_institute" + String(i + 1)).value = data[2][i][2];
        document.getElementById("doctor_year" + String(i + 1)).value = data[2][i][3];
    }
    for (var i = 0; i < data[3].length; i++) {
        document.getElementById("doctor_organization" + String(i + 1)).value = data[3][i][1];
        document.getElementById("doctor_experience_from_year" + String(i + 1)).value = data[3][i][2];
        document.getElementById("doctor_experience_to_year" + String(i + 1)).value = data[3][i][3];
    }
});