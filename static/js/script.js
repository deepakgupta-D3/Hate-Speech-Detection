

// static/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    console.log('JavaScript is loaded and ready!');
});

const messageForm = document.getElementById('messageForm');
const toast = document.getElementById('toast');

// Function to show toast notification
function showToast(message) {
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Ensure form submits only if textarea is filled
messageForm.addEventListener('submit', function (event) {
    const textarea = document.getElementById('message');
    if (textarea.value.trim() === "") {
        event.preventDefault(); // Prevent submission
        showToast("Enter message"); // Show toast
    }
});




