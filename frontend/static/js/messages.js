// This is for DJango messages to dissapear after 3000 ms
// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", function() {
    const messages = document.getElementById('django-messages');
    if (messages) {
        setTimeout(function() {
            messages.style.transition = "opacity 0.7s";
            messages.style.opacity = 0;
            setTimeout(() => messages.remove(), 700);
        }, 3000);
    }
});
