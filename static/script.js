/**
 * script.js – Shared front-end utilities for AI Fitness Trainer
 */

// ── Smooth page load ──────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  document.body.style.opacity = '0';
  document.body.style.transition = 'opacity 0.3s ease';
  requestAnimationFrame(() => { document.body.style.opacity = '1'; });

  // Highlight active nav link
  const current = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(link => {
    if (link.getAttribute('href') === current) {
      link.style.color = '#ff6b35';
    }
  });
});

// ── BMI colour helper (used on result page) ───────────────
function getBmiColour(bmi) {
  if (bmi < 18.5) return '#00d4ff';
  if (bmi < 25)   return '#00e676';
  if (bmi < 30)   return '#ffd700';
  return '#ff4757';
}

// ── Utility: auto-dismiss alerts after 4 s ────────────────
document.querySelectorAll('.alert').forEach(el => {
  setTimeout(() => {
    el.style.transition = 'opacity 0.5s';
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 500);
  }, 4000);
});
