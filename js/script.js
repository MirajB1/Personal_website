// js/script.js
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('mobile-menu');
    const navList = document.querySelector('#main-header nav .nav-list');
    const header = document.getElementById('main-header');

    // Mobile Menu Toggle
    if (menuToggle && navList) {
        menuToggle.addEventListener('click', () => {
            navList.classList.toggle('active');
            const isExpanded = navList.classList.contains('active');
            menuToggle.setAttribute('aria-expanded', isExpanded);
            menuToggle.classList.toggle('is-active');
        });
    }

    // Smooth scroll for anchor links & Active link highlighting
    const navLinks = document.querySelectorAll('#main-header nav .nav-list a');
    const headerHeight = header ? header.offsetHeight : 70; // Default if header not found quickly

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.hash !== "") {
                const hash = this.hash;
                const targetElement = document.querySelector(hash);
                if (targetElement) {
                    if (navList.classList.contains('active')) {
                        navList.classList.remove('active');
                        menuToggle.classList.remove('is-active');
                        menuToggle.setAttribute('aria-expanded', 'false');
                    }
                    // If not using CSS scroll-behavior, uncomment and adjust this:
                    // e.preventDefault();
                    // const elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
                    // const offsetPosition = elementPosition - headerHeight;
                    // window.scrollTo({ top: offsetPosition, behavior: "smooth"});
                }
            }
        });
    });

    // Active link highlighting on scroll
    const sections = document.querySelectorAll('main section[id]');
    function setActiveLink() {
        let current = 'hero'; // Default to hero
        const effectiveHeaderHeight = header ? header.offsetHeight : 70; // Recalculate or use stored
        const scrollPosition = window.pageYOffset + effectiveHeaderHeight + 40; // Offset for better accuracy

        sections.forEach(section => {
            // Check if section is in viewport or just passed
            if (section.offsetTop <= scrollPosition && (section.offsetTop + section.offsetHeight) > scrollPosition) {
                current = section.getAttribute('id');
            }
        });

        // If scrolled to bottom, highlight the last section (contact)
        if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight - 50) { // Near bottom
            current = sections[sections.length -1].getAttribute('id');
        }


        navLinks.forEach(link => {
            link.classList.remove('active-link');
            const linkHref = link.getAttribute('href');
            if (linkHref && linkHref.substring(1) === current) {
                link.classList.add('active-link');
            }
        });
         // Fallback for top of page if no other section is active
        if (current === 'hero' && pageYOffset < (sections[0].offsetTop - effectiveHeaderHeight - 20) ) {
             navLinks.forEach(l => l.classList.remove('active-link'));
             const homeLink = document.querySelector('#main-header nav .nav-list a[href="#hero"]');
             if(homeLink) homeLink.classList.add('active-link');
        } else if (current === '' && pageYOffset < 200) { // Ensure hero is active if scrolled near top
            navLinks.forEach(l => l.classList.remove('active-link'));
            const homeLink = document.querySelector('#main-header nav .nav-list a[href="#hero"]');
            if(homeLink) homeLink.classList.add('active-link');
        }
    }
    window.addEventListener('scroll', setActiveLink);
    setActiveLink(); // Set active link on page load

    // Add/remove 'scrolled' class to header
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 30) { // Smaller threshold for scrolled effect
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }

     // Collapsible Sections (Accordion-like for mobile)
    const collapsibleTriggers = document.querySelectorAll('.collapsible-trigger');

    collapsibleTriggers.forEach(trigger => {
        // Set initial state for desktop: content open, icon might be '+'
        // If you want the icon to be '-' on desktop by default when content is open:
        // if (window.innerWidth > 768) {
        //     trigger.classList.add('active'); // Makes icon '-' or 'X'
        // }

        trigger.addEventListener('click', function() {
            const content = this.nextElementSibling;

            // Toggle active class for the icon regardless of view
            this.classList.toggle('active');

            // Only toggle content visibility (collapse/expand) on mobile
            const isMobileView = window.innerWidth <= 768;
            if (isMobileView) {
                if (content && content.classList.contains('collapsible-content')) {
                    content.classList.toggle('open');
                }
            }
            // On desktop, the content remains open due to CSS (max-height not 0)
            // but the icon will still toggle.
        });

        // Ensure correct initial state of icon and content based on viewport on load
        const contentElement = trigger.nextElementSibling;
        if (contentElement && contentElement.classList.contains('collapsible-content')) {
            if (window.innerWidth <= 768) {
                // Mobile: Content closed, icon '+' (no 'active' class on trigger)
                trigger.classList.remove('active');
                contentElement.classList.remove('open'); // CSS handles initial max-height: 0
            } else {
                // Desktop: Content open, icon should be '-' or 'X' if you want it to reflect "open" state
                // Or keep it as '+' if you only want it to react on mobile clicks.
                // For consistency that it CAN be toggled (on mobile), let's keep it as '+'
                trigger.classList.remove('active'); // Start with '+' icon on desktop
                contentElement.classList.add('open'); // Ensure CSS for 'open' makes it visible if it wasn't
            }
        }
    });

    // Update footer year
    const currentYearSpan = document.getElementById('currentYear');
    if (currentYearSpan) {
        currentYearSpan.textContent = new Date().getFullYear();
    }
});