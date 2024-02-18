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
