<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local Car Mechanic</title>
    <style>
        /* Embedded CSS from style.css */
        /* Pop-up modal styles */
.modal {
  display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
}

/* Modal Content */
.modal-content {
  background-color: #fefefe;
  margin: 15% auto; /* 15% from the top and centered */
  padding: 20px;
  border: 1px solid #888;
  width: 80%; /* Could be more or less, depending on screen size */
}

/* The Close Button */
.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.google-map iframe {
  width: 100%;
  height: 300px; /* or any other height */
  border: none;
}

footer a img {
  width: 1em; /* sets the icon size to the same as the current font size */
  height: auto; /* maintains aspect ratio */
  vertical-align: middle; /* aligns the icon with the middle of the text */
}

footer a img {
  width: 1em; /* or however large you want the icons to be relative to your text */
  height: auto; /* to maintain aspect ratio */
  vertical-align: middle; /* to align with the text */
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 10px;
  background-color: #333; /* Dark background for the header */
  color: white; /* Light text */
}

nav ul {
  list-style-type: none;
  display: flex;
  gap: 10px;
  margin: 0;
  padding: 0;
}

nav li {
  padding: 5px 10px; /* Add some padding around the list items */
}

nav button {
  background-color: #555; /* Slightly lighter than the header for contrast */
  color: white; /* White text for readability */
  border: none; /* Remove the default border */
  padding: 10px 20px; /* Add some padding for a larger click area */
  margin: 0; /* Remove default margin */
  cursor: pointer; /* Change mouse cursor to indicate it's clickable */
  transition: background-color 0.3s; /* Smooth transition for hover effect */
}

nav button:hover {
  background-color: #777; /* Lighten button background on hover */
}

/* Responsive design for smaller screens */
@media (max-width: 768px) {
  header {
      flex-direction: column;
  }

  nav ul {
      width: 100%;
      justify-content: space-around;
  }

  nav button {
      width: 100%; /* Full width buttons on smaller screens */
      padding: 15px; /* Larger padding for easier touch */
  }
}

/* Add padding and margin as needed for alignment */
body {
  margin: 0;
  padding: 0 20px; /* This adds 20 pixels of padding on the left and right */
  font-family: Arial, sans-serif;
  min-height: 100vh; /* This makes sure the content takes minimum full viewport height */
  display: flex;
  flex-direction: column; /* Aligns the content in a column */
}

main {
  flex: 1; /* This allows the main content to grow and push the footer down */
}

footer {
  background-color: #333; /* Example background color */
  color: white; /* Example text color */
  text-align: center;
  padding: 10px 0; /* Example padding */
  margin-top: auto; /* This pushes the footer to the bottom */
}

.maps-link {
  font-weight: bold;
  text-decoration: underline;
}

/* Style for mobile devices */
@media (max-width: 768px) {
  /* Stack the header title and navigation on top of each other */
  header {
      flex-direction: column;
      align-items: flex-start; /* Align items to the start (left) */
  }

  nav ul {
      flex-direction: column;
      align-items: flex-start;
      width: 100%; /* Full width */
  }

  nav li {
      width: 100%; /* Full width list items */
  }

  /* Adjust button sizes for easier interaction on touch devices */
  nav button {
      width: 100%; /* Full width buttons */
      padding: 15px; /* Larger padding for easier touch */
  }

  /* Adjust modal styles for smaller screens */
  .modal-content {
      width: 90%; /* Make modal content slightly smaller than the screen width */
      margin: 10% auto; /* Increase top margin */
  }

  /* Other styles as needed for smaller screens */
}

/* You can also add styles for larger tablets and smaller desktops, if necessary */
@media (min-width: 769px) and (max-width: 1024px) {
  /* Adjust styles for larger tablets and smaller desktops */
}

.phone-link {
    display: inline-block;
    background-color: #007bff; /* Bootstrap primary button color for example */
    color: white;
    padding: 10px 15px;
    margin: 10px 0;
    border: none;
    border-radius: 5px;
    text-decoration: none;
    text-align: center;
}

.phone-link:hover, .phone-link:active {
    background-color: #0056b3;
}

.contact-options {
    display: flex;
    justify-content: space-around; /* Distributes space evenly around the items */
    padding: 10px 0; /* Add some vertical padding */
}

.contact-person {
    display: block;
    background-color: #007bff; /* Example background color */
    color: white; /* Text color */
    text-align: center;
    padding: 10px;
    margin: 0 5px; /* Add horizontal margin for spacing between boxes */
    text-decoration: none; /* Remove underline from links */
    border-radius: 5px; /* Optional: rounds the corners of the boxes */
    width: 30%; /* Example width to ensure they fit in one row */
}

/* Adjustments for smaller screens */
@media (max-width: 768px) {
    .contact-person {
        width: auto; /* Let the boxes take up the needed width */
        flex-grow: 1; /* Allow boxes to grow as needed */
    }
}

/* Thumbnail images */
.thumbnails img {
  width: 100px;
  cursor: pointer;
  transition: transform 0.2s;
}

.thumbnails img:hover {
  transform: scale(1.1);
}

/* Lightbox */
.lightbox {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  z-index: 2;
  display: flex;
  justify-content: center;
  align-items: center;
}

.lightbox-content {
  position: relative;
}

.arrow {
  cursor: pointer;
  position: absolute;
  top: 50%;
  font-size: 24px;
  color: white;
  user-select: none;
}

.arrow.left {
  left: 0;
}

.arrow.right {
  right: 0;
}

.fullsize-photo {
  display: block;
  max-width: 90%;
  max-height: 80vh;
}
    </style>
</head>
<body>
    <header>
        <h1>Welcome to Our Car Mechanic Shop</h1>
        <nav>
            <ul>
                <li><button id="aboutBtn">About Us</button></li>
                <li><button id="servicesBtn">Services</button></li>
                <li><button id="galleryBtn">Gallery</button></li>
                <li><button id="contactBtn">Contact Us</button></li>
            </ul>
        </nav>
    </header>
    <main>
        <!-- Main content or welcome text -->
        <div class="welcome-text">
            <p>Your trusted partner for all automotive repairs.</p>
        </div>
        <!-- About Us Modal -->
        <div id="aboutModal" class="modal">
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>About Us</h2>
                <p>We are a family-owned workshop with over 25 years of experience...</p>
            </div>
        </div>
        <!-- Services Modal -->
        <div id="servicesModal" class="modal">
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>Services</h2>
                <p>We offer a wide range of services, including...</p>
            </div>
        </div>
        <!-- Gallery Modal -->
        <div id="galleryModal" class="modal">
            <div class="modal-content">
                <span class="close">&times;</span>
                <div class="thumbnails">
                    <!-- Example thumbnails -->
                    <img src="static/images/1.jpg" alt="Thumbnail 1" class="thumbnail">
                    <img src="static/images/2.jpg" alt="Thumbnail 2" class="thumbnail">
                    <!-- Add more thumbnails as needed -->
                </div>
                <div class="lightbox" style="display:none;">
                    <div class="lightbox-content">
                        <span class="arrow left">&#10094;</span>
                        <img class="fullsize-photo">
                        <span class="arrow right">&#10095;</span>
                    </div>
                </div>
            </div>
        </div>
        <!-- Contact Us Modal -->
        <div id="contactModal" class="modal">
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>Contact Us</h2>
                <p>Need to book an appointment or have a question? Reach out to us:</p>
                <div class="contact-options">
                    <a href="tel:+1234567890" class="contact-person">Call Person 1</a>
                    <a href="tel:+1234567891" class="contact-person">Call Person 2</a>
                    <a href="tel:+1234567892" class="contact-person">Call Person 3</a>
                </div>
                <!-- Google Maps Embed -->
                <div class="google-map">
                    <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2549.0841379255903!2d18.73525917722413!3d50.29035727156201!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x6bb30835716a3609%3A0x6a5c64b627f42465!2sMotospec%20Serwis%20Samochodowy!5e0!3m2!1sen!2spl!4v1708367202157!5m2!1sen!2spl" 
                    width="600" 
                    height="450" 
                    style="border:0;" 
                    allowfullscreen="" 
                    loading="lazy" 
                    referrerpolicy="no-referrer-when-downgrade"></iframe>
                </div>
            </div>
        </div>
    </main>
    <footer>
        <p>&copy; 2024 Local Car Mechanic Shop. All rights reserved.</p>
        <p>Follow us on:
            <a href="https://www.facebook.com/profile.php?id=61552495111520" target="_blank"><img src="{{ url_for('static', filename='images/facebook-icon.png') }}" alt="Facebook"></a>
            <a href="https://www.instagram.com/motospec.serwis/" target="_blank"><img src="{{ url_for('static', filename='images/instagram-icon.png') }}" alt="Instagram"></a>
        </p>
        <p>Find us <a href="https://www.google.com/maps/dir/?api=1&destination=Motospec+Serwis+Samochodowy,+Generała+Władysława+Sikorskiego+94,+44-103+Gliwice" target="_blank" class="maps-link">here</a>:
            <a href="https://www.google.com/maps/dir/?api=1&destination=Motospec+Serwis+Samochodowy,+Generała+Władysława+Sikorskiego+94,+44-103+Gliwice" target="_blank"><img src="{{ url_for('static', filename='images/google-maps-icon.png') }}" alt="Google Maps"></a>
        </p>
    </footer>

    <script>
        // Embedded JavaScript from script.js
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
    const close = document.querySelector('.close');
    let currentIndex;

    thumbnails.forEach((thumbnail, index) => {
        thumbnail.addEventListener('click', function() {
            lightbox.style.display = 'flex';
            fullsizePhoto.src = thumbnail.src; // Assuming full-size images are the same as thumbnails for simplicity
            currentIndex = index;
            updateArrows();
        });
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

    close.addEventListener('click', function() {
        lightbox.style.display = 'none';
    });

    function updateArrows() {
        document.querySelector('.arrow.left').style.display = currentIndex > 0 ? '' : 'none';
        document.querySelector('.arrow.right').style.display = currentIndex < thumbnails.length - 1 ? '' : 'none';
    }
});
    </script>
</body>
</html>