function deleteAdmin(email) {
    // Delete the appointment from the database after confirmation
    if (confirm("Are you sure you want to delete admin " + email + "?")) {
        alert("Admin deleted! You will be redirected to the Manage Admins page.")
        window.location.href = "/deleteAdmin/" + email + "/";
    }
}

function addAdmin() {
    var email = prompt("Enter Email ID for admin:");
    if (email != null) {
        var password = prompt("Enter password for admin:");
        if (password != null) {
            var userType = prompt("What is the user type? (For admin type \"1\" and for reception type \"2\"");
            if (userType != null && (userType != 1 || userType != 2)) {
                window.location.href = "/addAdmin/" + email + "/" + password + "/" + userType + "/";
            }
        }
    }
}