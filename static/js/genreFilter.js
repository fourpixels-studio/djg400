document.addEventListener("DOMContentLoaded", () => {
    const container = document.querySelector(".genres-container");
    const leftBtn = document.querySelector(".left-btn");
    const rightBtn = document.querySelector(".right-btn");

    leftBtn.addEventListener("click", () => {
        container.scrollBy({ left: -200, behavior: "smooth" });
    });

    rightBtn.addEventListener("click", () => {
        container.scrollBy({ left: 200, behavior: "smooth" });
    });
});
