function deleteAppointment(appointmentId) {
    // Delete the appointment from the database after confirmation
    if (confirm("Are you sure you want to delete this appointment?")) {
        alert("Appointment deleted! You will be redirected to the appointment page.")
        window.location.href = "/deleteAppointment/" + appointmentId;
    }
}
function completeAppointment(appointmentId) {
    // Complete the appointment from the database after confirmation
    if (confirm("Are you sure you want to complete this appointment?")) {
        alert("Appointment completed! You will be redirected to the appointment page.")
        window.location.href = "/completeAppointment/" + appointmentId;
    }
}
function deleteDocument(documentId) {
    // Delete the document from the database after confirmation
    if (confirm("Are you sure you want to delete this document?")) {
        alert("Document deleted! You will be redirected to the appointment page.")
        window.location.href = "/deleteDocument/" + documentId;
    }
}

var uploadField = document.getElementById("document");
uploadField.onchange = function () {
    if (this.files[0].size > 5242880) {
        alert("File is too big! Please upload a file smaller than 5MB.");
        this.value = "";
    };
};