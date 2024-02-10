document.querySelectorAll('.overlay-section').forEach(item => {
    item.addEventListener('click', function() {
        document.getElementById(this.id + '-overlay').style.display = 'block';
    });
});

document.querySelectorAll('.close-btn').forEach(item => {
    item.addEventListener('click', function() {
        this.parentElement.parentElement.style.display = 'none';
    });
});

// Close overlay when clicking outside of it
window.onclick = function(event) {
    if (event.target.classList.contains('overlay')) {
        event.target.style.display = 'none';
    }
}
