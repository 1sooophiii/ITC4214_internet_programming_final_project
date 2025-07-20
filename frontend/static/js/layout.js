$(document).ready(function () {
    const $menuBtn = $("#mobileMenuBtn");
    const $mobileMenu = $("#mobileMenu");

    //show or hide hamburger icon depending on window width
    const toggleBurger = () => {
        const triggerCondition = $(window).width() < 1024;

        if (triggerCondition) {
            $menuBtn.removeClass("hidden");
        } else {
            $menuBtn.addClass("hidden");
        }
    };

    toggleBurger();

    //when window is resized call toggleBurger
    $(window).on("resize", function () {
        toggleBurger();
    });

    //when hamburger menu button is clicked show or hide the mobile menu
    $menuBtn.on("click", function () {
        $mobileMenu.toggleClass("hidden");
    });
});
