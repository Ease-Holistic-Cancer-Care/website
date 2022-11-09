function deletePatient(id, name) {
    // Delete the appointment from the database after confirmation
    if (confirm("Are you sure you want to delete patient " + name + "?")) {
        alert("Patient deleted! You will be redirected to the Manage Patients page.")
        window.location.href = "/deletePatient/" + id + "/";
    }
}