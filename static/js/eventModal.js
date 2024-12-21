document.addEventListener("DOMContentLoaded", () => {
    const thumbnails = document.querySelectorAll(".image-thumbnail");
    const modal = new bootstrap.Modal(document.getElementById("imageModal"));
    const modalImage = document.getElementById("modalImage");
    const prevButton = document.getElementById("prevButton");
    const nextButton = document.getElementById("nextButton");

    let currentIndex = 0;
    const images = Array.from(thumbnails).map(img => img.src);

    // Open Modal
    thumbnails.forEach((thumbnail, index) => {
        thumbnail.addEventListener("click", () => {
            currentIndex = index;
            updateModalImage();
            modal.show();
        });
    });

    // Navigate Images
    prevButton.addEventListener("click", () => {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        updateModalImage();
    });

    nextButton.addEventListener("click", () => {
        currentIndex = (currentIndex + 1) % images.length;
        updateModalImage();
    });

    // Update Modal Image
    function updateModalImage() {
        modalImage.src = images[currentIndex];
    }
});
