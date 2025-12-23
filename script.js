// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Active navigation state on scroll
let sections = document.querySelectorAll('section[id]');
let navLinks = document.querySelectorAll('.nav-links a');

window.addEventListener('scroll', () => {
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (window.pageYOffset >= (sectionTop - 200)) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.style.color = '';
        if (link.getAttribute('href') === `#${current}`) {
            link.style.color = 'var(--accent-gold)';
        }
    });
});

// Fade in animation on scroll
const observerOptions = {
    threshold: 0.15,
    rootMargin: '0px 0px -50px 0px'
};

const fadeInObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for fade-in animation
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll(
        '.achievement-stat, .timeline-item, .category-card, .spec-item, .guideline-card, .indicator-item, .pipeline-step'
    );
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        fadeInObserver.observe(el);
    });
});

// Scroll progress indicator
const createScrollIndicator = () => {
    const indicator = document.createElement('div');
    indicator.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--accent-gold) 0%, var(--accent-bronze) 100%);
        z-index: 9999;
        transition: width 0.1s;
        box-shadow: 0 2px 4px rgba(212, 175, 55, 0.3);
    `;
    document.body.appendChild(indicator);
    
    window.addEventListener('scroll', () => {
        const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (window.scrollY / windowHeight) * 100;
        indicator.style.width = scrolled + '%';
    });
};

createScrollIndicator();

// Parallax effect for hero section
window.addEventListener('scroll', () => {
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        const scrollPosition = window.pageYOffset;
        heroSection.style.transform = `translateY(${scrollPosition * 0.5}px)`;
        heroSection.style.opacity = 1 - (scrollPosition / 700);
    }
});

// Counter animation for stats
const animateCounter = (element, target, duration = 2000) => {
    let startTimestamp = null;
    const start = 0;
    const end = target;
    
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        
        // Check if the element contains a decimal
        if (target.toString().includes('.')) {
            element.textContent = (progress * (end - start) + start).toFixed(2);
        } else {
            element.textContent = Math.floor(progress * (end - start) + start);
        }
        
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    
    window.requestAnimationFrame(step);
};

// Observe stats for counter animation
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !entry.target.dataset.animated) {
            entry.target.dataset.animated = 'true';
            const valueElement = entry.target.querySelector('.stat-number, .metric-value');
            if (valueElement) {
                const text = valueElement.textContent;
                const value = parseFloat(text.replace(/[^0-9.]/g, ''));
                if (!isNaN(value)) {
                    valueElement.textContent = '0';
                    setTimeout(() => {
                        animateCounter(valueElement, value);
                        // Add back any suffixes
                        if (text.includes('min')) {
                            setTimeout(() => {
                                valueElement.textContent = value + ' min';
                            }, 2000);
                        } else if (text.includes('+')) {
                            setTimeout(() => {
                                valueElement.textContent = value + '+';
                            }, 2000);
                        }
                    }, 200);
                }
            }
        }
    });
}, { threshold: 0.5 });

document.addEventListener('DOMContentLoaded', () => {
    const statElements = document.querySelectorAll('.achievement-stat, .metric-box');
    statElements.forEach(el => statsObserver.observe(el));
});

// Add subtle hover effect to cards
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.category-card, .guideline-card, .spec-item');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });
    });
});

// Console message
console.log('%c Digital Immortality Project ', 'background: #1a1a2e; color: #d4af37; font-size: 24px; padding: 12px; font-weight: bold;');
console.log('%c The Staff Sergeant Jimmy Mitchell Project ', 'font-size: 14px; color: #6c757d; padding: 4px;');
console.log('%c "In memory of those who served" ', 'font-size: 12px; color: #999; font-style: italic; padding: 4px;');

// Add fade-in to hero content
document.addEventListener('DOMContentLoaded', () => {
    const heroContent = document.querySelector('.hero-content');
    if (heroContent) {
        heroContent.style.opacity = '0';
        heroContent.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            heroContent.style.transition = 'opacity 1s ease, transform 1s ease';
            heroContent.style.opacity = '1';
            heroContent.style.transform = 'translateY(0)';
        }, 200);
    }
});

// Memorial section special effect
const memorialObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('memorial-visible');
            const quote = entry.target.querySelector('.memorial-quote');
            if (quote) {
                setTimeout(() => {
                    quote.style.opacity = '1';
                    quote.style.transform = 'translateY(0)';
                }, 500);
            }
        }
    });
}, { threshold: 0.3 });

document.addEventListener('DOMContentLoaded', () => {
    const memorial = document.querySelector('.memorial-section');
    if (memorial) {
        memorialObserver.observe(memorial);
        
        const quote = memorial.querySelector('.memorial-quote');
        if (quote) {
            quote.style.opacity = '0';
            quote.style.transform = 'translateY(20px)';
            quote.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
        }
    }
});

// Mobile menu toggle (if needed)
const createMobileMenu = () => {
    if (window.innerWidth <= 768) {
        const nav = document.querySelector('.nav');
        const navLinks = document.querySelector('.nav-links');
        
        if (!document.querySelector('.mobile-toggle')) {
            const toggle = document.createElement('button');
            toggle.className = 'mobile-toggle';
            toggle.innerHTML = '☰';
            toggle.style.cssText = `
                background: none;
                border: none;
                font-size: 1.8rem;
                color: var(--primary-dark);
                cursor: pointer;
                display: none;
            `;
            
            nav.querySelector('.nav-container').appendChild(toggle);
            
            toggle.addEventListener('click', () => {
                navLinks.classList.toggle('active');
            });
        }
    }
};

window.addEventListener('resize', createMobileMenu);
createMobileMenu();
