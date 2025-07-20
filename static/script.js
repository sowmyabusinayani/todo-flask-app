// Enable Add buttons only when text is present
function toggleButton(inputId, buttonId) {
    const input = document.getElementById(inputId);
    const button = document.getElementById(buttonId);
    button.disabled = input.value.trim() === "";
}

function showCategoryInput(userId) {
  const box = document.getElementById('category-box-' + userId);
  const input = document.getElementById('cat-input-' + userId + '-new');
  const btn = document.getElementById('cat-submit-' + userId + '-new');
}

// Make input field editable on edit button click
function enableEditing(inputId) {
    const input = document.getElementById(inputId);
    input.removeAttribute("readonly");
    input.focus();
}

// Prevent form submission if blank (or add duplicate check with AJAX later)
function validateForm(inputId, buttonId) {
    const input = document.getElementById(inputId);
    const button = document.getElementById(buttonId);
    if (input.value.trim() === "") {
        button.disabled = true;
    } else {
        button.disabled = false;
    }
}
