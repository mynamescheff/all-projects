document.addEventListener('DOMContentLoaded', () => {
    // Get all buttons that opens modals
    let modalBtns = document.querySelectorAll('[id$="Btn"]'); // Selects all buttons ending with 'Btn'
    
    modalBtns.forEach(function(btn) {
        btn.onclick = function() {
            let modal = document.getElementById(btn.id.replace('Btn', 'Modal'));
            if(modal) {
                modal.style.display = "block";
            }
        }
    });

    // Get all elements that closes modals
    let closeButtons = document.querySelectorAll('.close');
    
    closeButtons.forEach(function(btn) {
        btn.onclick = function() {
            let modal = btn.closest('.modal');
            if(modal) {
                modal.style.display = "none";
            }
        }
    });

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = "none";
        }
    }
});

document.addEventListener('DOMContentLoaded', () => {
    // Function to close any open modal
    function closeModals() {
        let modals = document.querySelectorAll('.modal');
        modals.forEach(function(modal) {
            modal.style.display = 'none';
        });
    }

    // Attach click event to modal buttons
    let modalBtns = document.querySelectorAll('[id$="Btn"]');
    
    modalBtns.forEach(function(btn) {
        btn.onclick = function() {
            let modal = document.getElementById(btn.id.replace('Btn', 'Modal'));
            if(modal) {
                modal.style.display = "block";
            }
        }
    });

    // Attach click event to close buttons
    let closeButtons = document.querySelectorAll('.close');
    
    closeButtons.forEach(function(btn) {
        btn.onclick = function() {
            closeModals();
        }
    });

    // Close modals when clicking outside of them
    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            closeModals();
        }
    }

    // Close modals when pressing the Esc key
    document.onkeydown = function(event) {
        if (event.key === "Escape") {
            closeModals();
        }
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const thumbnails = document.querySelectorAll('.thumbnail');
    const lightbox = document.querySelector('.lightbox');
    const fullsizePhoto = document.querySelector('.fullsize-photo');
    const closeLightboxButton = document.querySelector('.close-lightbox');
    let currentIndex;

    thumbnails.forEach((thumbnail, index) => {
        thumbnail.addEventListener('click', function() {
            lightbox.style.display = 'flex';
            fullsizePhoto.src = thumbnail.src; // Assuming full-size images are the same as thumbnails for simplicity
            currentIndex = index;
            updateArrows();
        });
    });

    closeLightboxButton.addEventListener('click', function() {
        lightbox.style.display = 'none';
    });

    document.querySelector('.arrow.left').addEventListener('click', function() {
        if (currentIndex > 0) {
            currentIndex--;
            fullsizePhoto.src = thumbnails[currentIndex].src;
            updateArrows();
        }
    });

    document.querySelector('.arrow.right').addEventListener('click', function() {
        if (currentIndex < thumbnails.length - 1) {
            currentIndex++;
            fullsizePhoto.src = thumbnails[currentIndex].src;
            updateArrows();
        }
    });

    document.addEventListener('keydown', function(event) {
        // Updated handling for the Escape key
        if (event.key === "Escape") {
            if (lightbox.style.display === 'flex') {
                lightbox.style.display = 'none';
                // Prevent further actions if lightbox was open
                event.stopPropagation();
            }
            // Removed the else clause that might close the gallery modal
        } else if (event.key === 'ArrowLeft') {
            navigatePhotos(-1);
        } else if (event.key === 'ArrowRight') {
            navigatePhotos(1);
        }
    });

    function navigatePhotos(direction) {
        // Adjust currentIndex based on direction and wrap around if necessary
        currentIndex += direction;
        if (currentIndex < 0) currentIndex = thumbnails.length - 1;
        if (currentIndex >= thumbnails.length) currentIndex = 0;
        fullsizePhoto.src = thumbnails[currentIndex].src;
        updateArrows();
    }

    function updateArrows() {
        document.querySelector('.arrow.left').style.display = currentIndex > 0 ? '' : 'none';
        document.querySelector('.arrow.right').style.display = currentIndex < thumbnails.length - 1 ? '' : 'none';
    }
});

