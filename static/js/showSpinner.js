function showSpinner() {
    var submitBtn = document.getElementById('submit-btn');
    var submitText = document.getElementById('submit-text');
    var processingText = document.getElementById('processing-text');
    var spinner = document.getElementById('spinner');
    submitBtn.disabled = true;
    submitText.classList.add('d-none');
    spinner.classList.remove('d-none');
    processingText.classList.remove('d-none');
}
