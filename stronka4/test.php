<?php
// Start PHP session for potential future use
session_start();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local Car Mechanic</title>
    <style>
        /* Pop-up modal styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgb(0,0,0);
            background-color: rgba(0,0,0,0.4);
        }

        /* Modal Content */
        .modal-content {
            background-color: #fefefe;
            margin: 15% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 80%;
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
            height: 300px;
            border: none;
        }

        footer a img {
            width: 1em;
            height: auto;
            vertical-align: middle;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 10px;
            background-color: #333;
            color: white;
        }

        nav ul {
            list-style-type: none;
            display: flex;
            gap: 10px;
            margin: 0;
            padding: 0;
        }

        nav li {
            padding: 5px 10px;
        }

        nav button {
            background-color: #555;
            color: white;
            border: none;
            padding: 10px 20px;
            margin: 0;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        nav button:hover {
            background-color: #777;
        }

        @media (max-width: 768px) {
            header {
                flex-direction: column;
            }

            nav ul {
                width: 100%;
                justify-content: space-around;
            }

            nav button {
                width: 100%;
                padding: 15px;
            }
        }

        body {
            margin: 0;
            padding: 0 20px;
            font-family: Arial, sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        main {
            flex: 1;
        }

        footer {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 10px 0;
            margin-top: auto;
        }

        .maps-link {
            font-weight: bold;
            text-decoration: underline;
        }

        @media (max-width: 768px) {
            header {
                flex-direction: column;
                align-items: flex-start;
            }

            nav ul {
                flex-direction: column;
                align-items: flex-start;
                width: 100%;
            }

            nav li {
                width: 100%;
            }

            nav button {
                width: 100%;
                padding: 15px;
            }

            .modal-content {
                width: 90%;
                margin: 10% auto;
            }
        }

        .phone-link {
            display: inline-block;
            background-color: #007bff;
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
            justify-content: space-around;
            padding: 10px 0;
        }

        .contact-person {
            display: block;
            background-color: #007bff;
            color: white;
            text-align: center;
            padding: 10px;
            margin: 0 5px;
            text-decoration: none;
            border-radius: 5px;
            width: 30%;
        }

        @media (max-width: 768px) {
            .contact-person {
                width: auto;
                flex-grow: 1;
            }
        }

        .thumbnails img {
            width: 100px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .thumbnails img:hover {
            transform: scale(1.1);
        }

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

        .lightbox-close {
            position: absolute;
            top: 10px;
            right: 10px;
            background-color: red;
            color: white;
            border: none;
            cursor: pointer;
            font-size: 20px;
            padding: 5px 10px;
            border-radius: 50%;
            z-index: 3;
        }

        .close-lightbox {
            position: absolute;
            top: 15px;
            right: 15px;
            color: white;
            font-size: 30px;
            cursor: pointer;
        }

        :root {
            --background-color: #ffffff;
            --text-color: #000000;
            --link-color: #0000ff;
            --modal-background-color: #fefefe;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --background-color: #121212;
                --text-color: #ffffff;
                --link-color: #bb86fc;
                --modal-background-color: #333333;
            }
        }

        .light-theme {
            --background-color: #ffffff;
            --text-color: #000000;
            --link-color: #0000ff;
            --modal-background-color: #fefefe;
        }

        .dark-theme {
            --background-color: #121212;
            --text-color: #ffffff;
            --link-color: #bb86fc;
            --modal-background-color: #333333;
        }

        body {
            background-color: var(--background-color);
            color: var(--text-color);
        }

        a {
            color: var(--link-color);
        }

        .modal-content {
            background-color: var(--modal-background-color);
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
                <button id="theme-toggle">Toggle Theme</button>
            </ul>
        </nav>
    </header>
    <main>
        <div class="welcome-text">
            <p>Your trusted partner for all automotive repairs.</p>
        </div>
        <div id="aboutModal" class="modal">
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>About Us</h2>
                <p>We are a family-owned workshop with over 25 years of experience...</p>
            </div>
        </div>
        <div id="servicesModal" class="modal">
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>Services</h2>
                <p>We offer a wide range of services, including...</p>
            </div>
        </div>
        <div id="galleryModal" class="modal">
            <div class="modal-content">
                <span class="close">&times;</span>
                <div class="thumbnails">
                    <img src="static/images/1.jpg" alt="Thumbnail 1" class="thumbnail">
                    <img src="static/images/2.jpg" alt="Thumbnail 2" class="thumbnail">
                </div>
                <div class="lightbox" style="display:none;">
                    <div class="lightbox-content">
                        <span class="arrow left">&#10094;</span>
                        <img class="fullsize-photo">
                        <span class="arrow right">&#10095;</span>
                        <span class="close-lightbox">&times;</span>
                    </div>
                </div>
            </div>
        </div>
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
                <div class="google-map">
                    <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2549.0841379255903!2d18.73525917722413!3d50.29035727156201!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x6bb30835716a3609%3A0x6a5c64b627f42465!2sMotospec%20Serwis%20Samochodowy!5e0!3m2!1sen!2spl!4v1708367202157!5m2!1sen!2spl" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                </div>
            </div>
        </div>
    </main>
    <footer>
        <p>&copy; 2024 Local Car Mechanic Shop. All rights reserved.</p>
        <p>Follow us on:
            <a href="https://www.facebook.com/profile.php?id=61552495111520" target="_blank"><img src="static/images/facebook-icon.png" alt="Facebook"></a>
            <a href="https://www.instagram.com/motospec.serwis/" target="_blank"><img src="static/images/instagram-icon.png" alt="Instagram"></a>
        </p>
        <p>Find us <a href="https://www.google.com/maps/dir/?api=1&destination=Motospec+Serwis+Samochodowy,+Genera%C5%82a+W%C5%82adys%C5%82awa+Sikorskiego+94,+44-103+Gliwice" target="_blank" class="maps-link">here</a>:
            <a href="https://www.google.com/maps/dir/?api=1&destination=Motospec+Serwis+Samochodowy,+Genera%C5%82a+W%C5%82adys%C5%82awa+Sikorskiego+94,+44-103+Gliwice" target="_blank"><img src="static/images/google-maps-icon.png" alt="Google Maps"></a>
        </p>
    </footer>
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            let modalBtns = document.querySelectorAll('[id$="Btn"]');
            
            modalBtns.forEach(function(btn) {
                btn.onclick = function() {
                    let modal = document.getElementById(btn.id.replace('Btn', 'Modal'));
                    if(modal) {
                        modal.style.display = "block";
                    }
                }
            });

            let closeButtons = document.querySelectorAll('.close');
            
            closeButtons.forEach(function(btn) {
                btn.onclick = function() {
                    let modal = btn.closest('.modal');
                    if(modal) {
                        modal.style.display = "none";
                    }
                }
            });

            window.onclick = function(event) {
                if (event.target.classList.contains('modal')) {
                    event.target.style.display = "none";
                }
            }
        });

        document.addEventListener('DOMContentLoaded', () => {
            function closeModals() {
                let modals = document.querySelectorAll('.modal');
                modals.forEach(function(modal) {
                    modal.style.display = 'none';
                });
            }

            let modalBtns = document.querySelectorAll('[id$="Btn"]');
            
            modalBtns.forEach(function(btn) {
                btn.onclick = function() {
                    let modal = document.getElementById(btn.id.replace('Btn', 'Modal'));
                    if(modal) {
                        modal.style.display = "block";
                    }
                }
            });

            let closeButtons = document.querySelectorAll('.close');
            
            closeButtons.forEach(function(btn) {
                btn.onclick = function() {
                    closeModals();
                }
            });

            window.onclick = function(event) {
                if (event.target.classList.contains('modal')) {
                    closeModals();
                }
            }

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
                    fullsizePhoto.src = thumbnail.src;
                    currentIndex = index;
                    updateArrows();
                });
            });

            closeLightboxButton.addEventListener('click', function() {
                lightbox.style.display = 'none';
            });

            document.querySelector('.arrow.left').addEventListener('click', function() {
                navigatePhotos(-1);
            });

            document.querySelector('.arrow.right').addEventListener('click', function() {
                navigatePhotos(1);
            });

            document.addEventListener('keydown', function(event) {
                if (event.key === "Escape") {
                    if (lightbox.style.display === 'flex') {
                        lightbox.style.display = 'none';
                        event.preventDefault();
                    }
                } else if (event.key === 'ArrowLeft') {
                    navigatePhotos(-1);
                } else if (event.key === 'ArrowRight') {
                    navigatePhotos(1);
                }
            });

            function navigatePhotos(direction) {
                if (lightbox.style.display === 'flex') {
                    currentIndex += direction;
                    currentIndex = (currentIndex + thumbnails.length) % thumbnails.length;
                    fullsizePhoto.src = thumbnails[currentIndex].src;
                    updateArrows();
                }
            }

            function updateArrows() {
                document.querySelector('.arrow.left').style.visibility = currentIndex > 0 ? 'visible' : 'hidden';
                document.querySelector('.arrow.right').style.visibility = currentIndex < thumbnails.length - 1 ? 'visible' : 'hidden';
            }
        });

        document.addEventListener('DOMContentLoaded', () => {
            const themeToggle = document.getElementById('theme-toggle');

            themeToggle.addEventListener('click', () => {
                if (document.body.classList.contains('dark-theme')) {
                    document.body.classList.remove('dark-theme');
                    document.body.classList.add('light-theme');
                    localStorage.setItem('theme', 'light');
                } else {
                    document.body.classList.remove('light-theme');
                    document.body.classList.add('dark-theme');
                    localStorage.setItem('theme', 'dark');
                }
            });

            const savedTheme = localStorage.getItem('theme') || 'light';
            document.body.classList.add(savedTheme + '-theme');
        });
    </script>
</body>
</html>
