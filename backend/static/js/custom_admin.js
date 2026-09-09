/* ==============================================================================
   TIIPE & NOVATRIX MASTER JAZZMIN ADMIN JAVASCRIPT
   ============================================================================== */

document.addEventListener('DOMContentLoaded', function () {
    console.log("TIIPE & Novatrix Unified Master Admin Portal initialized.");

    // Highlight brand context badges dynamically
    const currentUrl = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-sidebar .nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentUrl) {
            link.classList.add('active');
        }
    });
});
