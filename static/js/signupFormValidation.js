const emailPassword = document.getElementById("email-password");
const usernameNames = document.getElementById("username-names");
const prevBtn = document.getElementById("show-username-names");
const nextBtn = document.getElementById("show-email-password");
const username = document.getElementById("id_username");
const firstName = document.getElementById("id_first_name");

emailPassword.style.display = 'none';
usernameNames.style.display = 'block';

function nextStep() {
    validateField(username);
    validateField(firstName);
    
    if (username.value.trim() !== "" && firstName.value.trim() !== "") {
        usernameNames.style.display = 'none';
        emailPassword.style.display = 'block';
    }
}

function validateField(field) {
    const invalidFeedback = field.nextElementSibling;

    if (field.value.trim() === "") {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
        invalidFeedback.textContent = "This field is required.";
    } else {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
        invalidFeedback.textContent = "Looks good!";
        invalidFeedback.style.color = 'green';
    }
}

function previousStep() {
    emailPassword.style.display = 'none';
    usernameNames.style.display = 'block';
}

nextBtn.addEventListener("click", nextStep);
prevBtn.addEventListener("click", previousStep);