function goBack() {
    window.history.back();
}

function copyToClipboard() {
    var copyText = document.getElementById("shareLink");
    var copyBtn = document.getElementById("copy-btn");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    document.execCommand("copy");
    copyBtn.innerHTML = "Link Copied";
}
