document.addEventListener("DOMContentLoaded", () => {

    /* =========================
       Mobile Menu Toggle
    ========================= */
    const mobileMenuBtn = document.querySelector(".mobile-menu-btn");
    const navLinks = document.querySelector(".nav-links");
    const navActions = document.querySelector(".nav-actions");

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener("click", () => {
            mobileMenuBtn.classList.toggle("active");
            navLinks.classList.toggle("mobile-active");
            navActions.classList.toggle("mobile-active");
        });
    }

    /* =========================
       Smooth Scrolling
    ========================= */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            const targetId = this.getAttribute("href");
            if (targetId === "#") return;

            e.preventDefault();
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: "smooth"
                });
            }

            // Close mobile menu after click
            navLinks?.classList.remove("mobile-active");
            navActions?.classList.remove("mobile-active");
            mobileMenuBtn?.classList.remove("active");
        });
    });

    /* =========================
       Navbar Shadow on Scroll
    ========================= */
    const navbar = document.querySelector(".navbar");

    window.addEventListener("scroll", () => {
        if (window.scrollY > 20) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    });

    /* =========================
       Simple Scroll Reveal Animation
    ========================= */
    const revealElements = document.querySelectorAll(
        ".feature-card, .process-step, .about, .hero-badge"
    );

    const revealOnScroll = () => {
        const windowHeight = window.innerHeight;
        revealElements.forEach(el => {
            const elementTop = el.getBoundingClientRect().top;
            if (elementTop < windowHeight - 100) {
                el.classList.add("reveal");
            }
        });
    };

    window.addEventListener("scroll", revealOnScroll);
    revealOnScroll(); // Initial check

    /* =========================
       Console Log
    ========================= */
    console.log("🚀 OncoScan frontend loaded successfully");
});
