function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

$("#disease_id").on('change', function () {
    var id = $(this).find('option:selected').attr('id');
    var url = document.URL;
    var domain = url.split('/')[0] + "//" + url.split('/')[2] + "/";
    data = httpGet(domain + "getDisease/content/" + String(id) + "/");
    data = JSON.parse(data);
    document.getElementById("disease_title").value = data[0][1];
    document.getElementById("specialty_name").value = data[0][2];
    document.getElementById("disease_description").value = data[0][3];
    document.getElementById("disease_illustration_preview").src = data[0][4];
    var select = document.getElementById('doctors');
    data[0][5] = data[0][5].split(",")
    for (var i = 0; i < select.options.length; i++) {
        if (data[0][5].includes(select.options[i].value)) {
            select.options[i].selected = true;
        }
    }
    document.getElementById("main_image_preview").src = data[0][6];
    for (var i = 0; i < data[1].length; i++) {
        document.getElementById("disease_profile_title" + String(i + 1)).value = data[1][i][1]
        document.getElementById("disease_profile_content" + String(i + 1)).value = data[1][i][2]
    }
    for (var i = 0; i < data[2].length; i++) {
        document.getElementById("disease_type_title" + String(i + 1)).value = data[2][i][1]
        document.getElementById("disease_type_description" + String(i + 1)).value = data[2][i][2]
        document.getElementById("disease_type_image_preview" + String(i + 1)).src = data[2][i][3]
    }
    var causes = "";
    for (var i = 0; i < data[3].length; i++) {
        if (i != data[3].length - 1)
            causes += data[3][i][1] + ";";
        else
            causes += data[3][i][1];
    }
    document.getElementById("disease_causes").value = causes;
    symptoms = "";
    for (var i = 0; i < data[4].length; i++) {
        if (i != data[4].length - 1)
            symptoms += data[4][i][1] + ";";
        else
            symptoms += data[4][i][1];
    }
    document.getElementById("disease_symptoms").value = symptoms;

    for (var i = 0; i < data[5].length; i++) {
        document.getElementById("disease_diagnosis_type" + String(i + 1)).value = data[5][i][1]
        document.getElementById("disease_diagnosis_description" + String(i + 1)).value = data[5][i][2]
    }

    for (var i = 0; i < data[6].length; i++) {
        document.getElementById("disease_severity_type" + String(i + 1)).value = data[6][i][1]
        document.getElementById("disease_severity_description" + String(i + 1)).value = data[6][i][2]
    }

    for (var i = 0; i < data[7].length; i++) {
        document.getElementById("disease_treatment_type" + String(i + 1)).value = data[7][i][1]
        document.getElementById("disease_treatment_description" + String(i + 1)).value = data[7][i][2]
    }
});