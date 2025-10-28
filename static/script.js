document.addEventListener("DOMContentLoaded", () => {
    const passwordInput = document.getElementById("password");
    const showPassword = document.getElementById("show-password");
    const show = document.getElementById("show");
    const hide = document.getElementById("hide");

    showPassword.addEventListener("click", () => {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            show.style.display = "inline";
            hide.style.display = "none";
        } else {
            passwordInput.type = "password";
            show.style.display = "none";
            hide.style.display = "inline";
        }
    });
});

function toggleDropdown() {
    const dropdown = document.getElementById("dropdown");
    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
}

function toggleFavoriteImage(event) {
    event.preventDefault();
    const button = event.target;
    const form = button.closest("form");
    const image = button.querySelector("img");
    const currentSrc = image.src;
    const favoriteSrc = image.dataset.favoriteImage;
    const unfavoriteSrc = image.dataset.unfavoriteImage;

    if (currentSrc === favoriteSrc) {
        image.src = unfavoriteSrc;
    } else {
        image.src = favoriteSrc;
    }

    form.submit();
}
