document.addEventListener("DOMContentLoaded", function () {
  // --- Smooth Scroll for internal links (optional) ---
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // --- On-Load Animations ---
  const elementsToAnimateOnLoad = document.querySelectorAll(".animate-on-load");
  elementsToAnimateOnLoad.forEach((el, index) => {
    const delay = parseInt(el.dataset.delay) || 0;
    const animationType = el.dataset.animation || "fadeInUp"; // Default to fadeInUp
    
    setTimeout(() => {
      el.style.opacity = "0"; // Ensure opacity is 0 before animation starts
      if (animationType === "fadeInUp") {
        el.style.transform = "translateY(30px)";
      }
      // Add other initial states for different animations if needed
      
      el.classList.add(animationType); // Add animation class
      el.style.animationDelay = `${index * 100}ms`; // Stagger slightly

    }, delay);
  });


  // --- Scroll Reveal for result blocks and other elements ---
  const scrollElements = document.querySelectorAll(".animate-scroll");
  if (scrollElements.length > 0) {
    const scrollObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 } // Trigger when 15% of the element is visible
    );
    scrollElements.forEach((el) => scrollObserver.observe(el));
  }


  // --- Ripple Effect for Buttons ---
  // This is now primarily handled by CSS :active::before for simplicity and performance.
  // The JS version can be more complex if needed. We'll rely on CSS for now.

  // --- Copy to Clipboard Functionality ---
  const copyButtons = document.querySelectorAll(".btn-copy");
  copyButtons.forEach(button => {
    button.addEventListener("click", () => {
      const preElement = button.closest(".result-block").querySelector("pre[data-copyable]");
      if (preElement) {
        const textToCopy = preElement.innerText;
        navigator.clipboard.writeText(textToCopy).then(() => {
          const originalIcon = button.innerHTML;
          button.innerHTML = '<i class="fas fa-check"></i> Copied!';
          button.classList.add("copied");
          
          setTimeout(() => {
            button.innerHTML = originalIcon;
            button.classList.remove("copied");
          }, 2000);
        }).catch(err => {
          console.error("Failed to copy: ", err);
          // Optionally, provide user feedback for error
          const originalIcon = button.innerHTML;
          button.innerHTML = '<i class="fas fa-times"></i> Failed';
           setTimeout(() => {
            button.innerHTML = originalIcon;
          }, 2000);
        });
      }
    });
  });

});