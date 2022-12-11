function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

let questions = [], answers = [];

$("#disease_id").on('change', function () {
    var id = $(this).find('option:selected').attr('id');
    var url = document.URL;
    var domain = url.split('/')[0] + "//" + url.split('/')[2] + "/";
    data = httpGet(domain + "getDiseaseFAQ/" + String(id) + "/");
    data = JSON.parse(data);
    for (i = 0; i < data.length; i++) {
        questions.push(data[i][0]);
        answers.push(data[i][1]);
    }
    var question_select = document.getElementById("faq_question");
    for (i = 0; i < questions.length; i++) {
        var option = document.createElement("option");
        option.text = questions[i];
        option.value = questions[i];
        option.id = "faq_" + id + "_" + i;
        question_select.add(option);
    }
});

$("#faq_question").on('change', function () {
    var id = $(this).find('option:selected').attr('id');
    var index = id.split('_')[2];
    document.getElementById("faq_answer").value = answers[index];
})