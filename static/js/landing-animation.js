/**
 * DineFlow Landing Page Spice & Steam Ambient Canvas Animation
 * Subtle, lightweight, high-performance particle system for Indian Restaurant ERP
 * Full support for prefers-reduced-motion accessibility
 */

(function() {
  'use strict';

  const canvas = document.getElementById('df-spice-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let animationFrameId;
  let width, height;
  let particles = [];

  // Check reduced motion preference
  const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  let isReducedMotion = mediaQuery.matches;

  mediaQuery.addEventListener('change', (e) => {
    isReducedMotion = e.matches;
    if (isReducedMotion) {
      cancelAnimationFrame(animationFrameId);
      drawStaticBackground();
    } else {
      init();
    }
  });

  const SPICE_COLORS = [
    'rgba(240, 106, 51, 0.45)', // Terracotta / Paprika
    'rgba(255, 162, 56, 0.40)', // Saffron / Turmeric
    'rgba(196, 43, 59, 0.35)',  // Chili Maroon
    'rgba(217, 179, 43, 0.30)', // Cardamom Gold
    'rgba(52, 189, 85, 0.25)',  // Coriander Green
    'rgba(255, 255, 255, 0.15)' // Steam / White
  ];

  class Particle {
    constructor() {
      this.reset(true);
    }

    reset(initial = false) {
      this.x = Math.random() * width;
      this.y = initial ? Math.random() * height : height + 20;
      this.size = Math.random() * 4.5 + 1.5;
      this.speedY = Math.random() * 0.45 + 0.15;
      this.speedX = (Math.random() - 0.5) * 0.3;
      this.color = SPICE_COLORS[Math.floor(Math.random() * SPICE_COLORS.length)];
      this.opacity = Math.random() * 0.6 + 0.2;
      this.wobble = Math.random() * Math.PI * 2;
      this.wobbleSpeed = Math.random() * 0.02 + 0.005;
    }

    update() {
      this.y -= this.speedY;
      this.wobble += this.wobbleSpeed;
      this.x += this.speedX + Math.sin(this.wobble) * 0.25;

      if (this.y < -30 || this.x < -30 || this.x > width + 30) {
        this.reset(false);
      }
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.fill();
    }
  }

  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  }

  function init() {
    resize();
    particles = [];
    const count = Math.min(Math.floor((width * height) / 18000), 75);
    for (let i = 0; i < count; i++) {
      particles.push(new Particle());
    }
    if (!isReducedMotion) {
      animate();
    } else {
      drawStaticBackground();
    }
  }

  function drawStaticBackground() {
    ctx.clearRect(0, 0, width, height);
    // Draw subtle warm glowing ambient gradient
    const grad = ctx.createRadialGradient(width / 2, height / 3, 50, width / 2, height / 2, width);
    grad.addColorStop(0, 'rgba(122, 26, 36, 0.15)');
    grad.addColorStop(0.5, 'rgba(224, 83, 26, 0.06)');
    grad.addColorStop(1, 'rgba(21, 21, 26, 0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, width, height);
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);

    // Draw ambient warmth glow
    const grad = ctx.createRadialGradient(width / 2, height * 0.4, 80, width / 2, height * 0.5, width * 0.7);
    grad.addColorStop(0, 'rgba(122, 26, 36, 0.18)');
    grad.addColorStop(0.4, 'rgba(224, 83, 26, 0.08)');
    grad.addColorStop(1, 'rgba(21, 21, 26, 0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, width, height);

    // Update and draw particles
    for (let i = 0; i < particles.length; i++) {
      particles[i].update();
      particles[i].draw();
    }

    animationFrameId = requestAnimationFrame(animate);
  }

  window.addEventListener('resize', () => {
    resize();
  });

  window.addEventListener('DOMContentLoaded', init);
})();
