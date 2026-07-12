document.addEventListener('DOMContentLoaded', function() {
    const hamburgerBtn = document.getElementById('hamburger-btn');
    const nav = document.querySelector('.header-nav nav');

    hamburgerBtn.addEventListener('click', function() {
        nav.classList.toggle('active'); //  classe 'active' pour afficher/masquer le menu
    });
});