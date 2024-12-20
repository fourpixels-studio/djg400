document.addEventListener("DOMContentLoaded", function () {
    const navbar = document.querySelector("nav");
    let lastScrollPosition = 0;

    window.addEventListener("scroll", function () {
        const currentScrollPosition = window.scrollY;

        if (currentScrollPosition > 100) { // Only trigger after scrolling 100px
            if (currentScrollPosition > lastScrollPosition) {
                // User is scrolling down
                navbar.style.transform = "translateY(-100%)"; // Hide navbar
            } else {
                // User is scrolling up
                navbar.style.transform = "translateY(0)"; // Show navbar
            }
        } else {
            // If scroll is less than 100px, always show the navbar
            navbar.style.transform = "translateY(0)";
        }

        // Update the last scroll position
        lastScrollPosition = currentScrollPosition;
    });
});
