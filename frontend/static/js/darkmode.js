$(document).ready(function () {
    const $toggleBtn = $("#toggle-dark");
    const $toggleMobileBtn = $("#mobile-toggle-dark");
    const $darkIcon = $("#dark-icon");
    const $lightIcon = $("#light-icon");

    function updateIcon(isDark) {
        if (isDark) {
            $darkIcon.hide();
            $lightIcon.show();
        } else {
            $darkIcon.show();
            $lightIcon.hide();
        }
    }

    $toggleBtn.on("click", function () {
        const isDark = $("html").toggleClass("dark").hasClass("dark");
        localStorage.setItem("theme", isDark ? "dark" : "light");
        updateIcon(isDark);
    });

    $toggleMobileBtn.on("click", function () {
        const isDark = $("html").toggleClass("dark").hasClass("dark");
        localStorage.setItem("theme", isDark ? "dark" : "light");
        updateIcon(isDark);
    });

    if (localStorage.getItem("theme") === "dark") {
        $("html").addClass("dark");
    }

    updateIcon($("html").hasClass("dark"));
});
