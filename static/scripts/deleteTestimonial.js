function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

$("#testimonial_id").on('change', function () {
    var id = $(this).find('option:selected').attr('id');
    var url = document.URL;
    var domain = url.split('/')[0] + "//" + url.split('/')[2] + "/";
    data = httpGet(domain + "getTestimonial/" + String(id) + "/");
    data = data.replaceAll('[', '');
    data = data.replaceAll(']', '');
    data = data.replaceAll('"', '');
    data = data.split(", ");
    document.getElementById("testimonial_name").value = data[1];
    document.getElementById("testimonial_designation").value = data[2];
    document.getElementById("testimonial_content").value = data[3];
    document.getElementById("testimonial_image").src = data[4]
});