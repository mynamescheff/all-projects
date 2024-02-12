function openOverlay(overlayId) {
    var overlay = document.getElementById(overlayId);
    overlay.style.display = 'block';
}

function closeOverlay(overlayId) {
    var overlay = document.getElementById(overlayId);
    overlay.style.display = 'none';
}

// Close the overlay if the user clicks outside of the content area
window.addEventListener('click', function(event) {
    if (event.target.className === 'overlay') {
        closeOverlay(event.target.id);
    }
});
