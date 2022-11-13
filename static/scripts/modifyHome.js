function deleteCarousel(carouselId) {
    if (confirm("Are you sure you want to delete this carousel?")) {
        alert("Carousel deleted! You will be redirected to the home modification page.")
        window.location.href = "/deleteCarousel/" + carouselId + "/";
    }
}
function deleteStatistic(statisticId) {
    if (confirm("Are you sure you want to delete this statistic?")) {
        alert("Statistic deleted! You will be redirected to the home modification page.")
        window.location.href = "/deleteStatistic/" + statisticId + "/";
    }
}
function deleteFAQ(faqId) {
    if (confirm("Are you sure you want to delete this FAQ?")) {
        alert("FAQ deleted! You will be redirected to the home modification page.")
        window.location.href = "/deleteFAQ/" + faqId + "/";
    }
}