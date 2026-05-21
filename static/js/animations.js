// Initialize simple UI animations and particles if available
document.addEventListener('DOMContentLoaded', function(){
  // Fade in main content
  document.querySelectorAll('.fade-in').forEach(function(el, idx){
    el.style.animationDelay = (idx * 80) + 'ms'
  })

  // Initialize tsParticles if present
  if (window.tsParticles) {
    tsParticles.load('tsparticles', {
      fpsLimit: 60,
      particles: {
        number: { value: 30 },
        color: { value: '#ffffff' },
        opacity: { value: 0.08 },
        size: { value: { min: 2, max: 6 } },
        move: { enable: true, speed: 0.7 }
      }
    });
  }

  // Password show/hide toggle (elements with class 'password-toggle' and data-target selector)
  document.querySelectorAll('.password-toggle').forEach(function(btn){
    btn.addEventListener('click', function(){
      var target = btn.getAttribute('data-target');
      var input = document.querySelector(target);
      if(!input) return;
      if(input.type === 'password'){
        input.type = 'text';
        btn.textContent = 'Hide';
      } else {
        input.type = 'password';
        btn.textContent = 'Show';
      }
    });
  });
})
