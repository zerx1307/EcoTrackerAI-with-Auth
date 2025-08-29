async function postJSON(url, data) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return res.json();
}

function drawChart(series) {
  const labels = Object.keys(series);
  const data = Object.values(series);
  const ctx = document.getElementById('impactChart');
  if (!ctx) return;
  
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'kg CO₂ saved',
        data,
        backgroundColor: (ctx) => {
          const canvas = ctx.chart.ctx;
          const gradient = canvas.createLinearGradient(0, 0, 0, 400);
          gradient.addColorStop(0, 'rgba(16, 185, 129, 0.8)');
          gradient.addColorStop(1, 'rgba(52, 211, 153, 0.4)');
          return gradient;
        },
        borderColor: 'rgb(16, 185, 129)',
        borderWidth: 2,
        borderRadius: 8,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { 
        legend: { 
          display: true,
          labels: {
            color: '#065f46',
            font: {
              size: 14,
              weight: 'bold'
            }
          }
        }
      },
      scales: { 
        y: { 
          beginAtZero: true,
          grid: {
            color: 'rgba(16, 185, 129, 0.1)'
          },
          ticks: {
            color: '#065f46'
          }
        },
        x: {
          grid: {
            display: false
          },
          ticks: {
            color: '#065f46'
          }
        }
      },
      animation: {
        duration: 2000,
        easing: 'easeInOutQuart'
      }
    }
  });
}

function equivalentsHTML(kg) {
  const phone = Math.floor(kg * 50);
  const bulb = Math.floor(kg * 10);
  const trees = (kg / 21.0).toFixed(3);
  const car = (kg * 2.31).toFixed(1); // miles not driven
  
  return `
    <div class="grid grid-cols-2 gap-4">
      <div class="flex items-center gap-2 p-3 bg-white/80 rounded-xl">
        <span class="text-2xl">📱</span>
        <div>
          <p class="font-bold text-emerald-800">${phone}</p>
          <p class="text-xs text-emerald-600">phone charges</p>
        </div>
      </div>
      <div class="flex items-center gap-2 p-3 bg-white/80 rounded-xl">
        <span class="text-2xl">💡</span>
        <div>
          <p class="font-bold text-emerald-800">${bulb}h</p>
          <p class="text-xs text-emerald-600">lightbulb hours</p>
        </div>
      </div>
      <div class="flex items-center gap-2 p-3 bg-white/80 rounded-xl">
        <span class="text-2xl">🌳</span>
        <div>
          <p class="font-bold text-emerald-800">${trees}</p>
          <p class="text-xs text-emerald-600">trees/year</p>
        </div>
      </div>
      <div class="flex items-center gap-2 p-3 bg-white/80 rounded-xl">
        <span class="text-2xl">🚗</span>
        <div>
          <p class="font-bold text-emerald-800">${car}mi</p>
          <p class="text-xs text-emerald-600">not driven</p>
        </div>
      </div>
    </div>
  `;
}

// Enhanced animations and interactions
document.addEventListener('DOMContentLoaded', () => {
  // Initialize chart
  if (typeof SERIES !== 'undefined') {
    setTimeout(() => drawChart(SERIES), 500); // Slight delay for better UX
  }
  
  // Initialize equivalents
  if (typeof TOTAL !== 'undefined') {
    const eq = document.getElementById('equivalentsBox');
    if (eq) {
      setTimeout(() => {
        eq.innerHTML = equivalentsHTML(TOTAL);
        eq.classList.add('fade-in-up');
      }, 800);
    }
  }

  // Enhanced modal interactions
  const modal = document.getElementById('logModal');
  const openBtn = document.getElementById('openLog');
  const closeBtn = document.getElementById('closeLog');
  
  if (openBtn && modal) {
    openBtn.onclick = () => { 
      modal.classList.remove('hidden'); 
      modal.classList.add('flex');
      // Add pulse effect to button
      openBtn.classList.add('pulse-glow');
      setTimeout(() => openBtn.classList.remove('pulse-glow'), 2000);
    };
  }
  
  if (closeBtn && modal) {
    closeBtn.onclick = () => { 
      modal.classList.add('hidden'); 
      modal.classList.remove('flex'); 
    };
  }

  // Enhanced form submission
  const form = document.getElementById('logForm');
  const result = document.getElementById('logResult');
  
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;
      
      // Show loading state
      submitBtn.innerHTML = `
        <span class="flex items-center justify-center gap-2">
          <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>Saving...</span>
        </span>
      `;
      submitBtn.disabled = true;
      
      try {
        const entry = document.getElementById('entry').value;
        const resp = await postJSON('/api/log', { entry });
        
        if (resp.ok) {
          // Show success state
          if (result) {
            result.innerHTML = `
              <div class="flex items-center justify-center gap-2">
                <span>🎉</span>
                <span>Saved ${resp.co2_saved_kg} kg CO₂ (${resp.meta.category})</span>
              </div>
            `;
            result.classList.remove('hidden');
            result.classList.add('fade-in-up');
          }
          
          // Reset form
          form.reset();
          
          // Reload page after delay
          setTimeout(() => {
            window.location.reload();
          }, 1500);
        } else {
          throw new Error(resp.error || 'Could not log entry');
        }
      } catch (error) {
        // Show error state
        if (result) {
          result.innerHTML = `
            <div class="flex items-center justify-center gap-2 text-red-600">
              <span>⚠️</span>
              <span>${error.message}</span>
            </div>
          `;
          result.classList.remove('hidden');
          result.classList.add('fade-in-up');
        }
      } finally {
        // Reset button
        setTimeout(() => {
          submitBtn.innerHTML = originalText;
          submitBtn.disabled = false;
        }, 1000);
      }
    });
  }

  // Add floating animation to cards on scroll
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in-up');
      }
    });
  }, observerOptions);

  // Observe all cards
  document.querySelectorAll('.bg-white\\/70, .glass-effect').forEach(card => {
    observer.observe(card);
  });

  // Add smooth hover effects to buttons
  document.querySelectorAll('.eco-gradient').forEach(btn => {
    btn.addEventListener('mouseenter', () => {
      btn.style.transform = 'translateY(-2px) scale(1.02)';
    });
    
    btn.addEventListener('mouseleave', () => {
      btn.style.transform = 'translateY(0) scale(1)';
    });
  });
});

// Add some fun particles effect (optional)
function createParticle() {
  const particle = document.createElement('div');
  particle.className = 'fixed w-2 h-2 bg-green-400 rounded-full opacity-50 pointer-events-none z-0';
  particle.style.left = Math.random() * window.innerWidth + 'px';
  particle.style.top = window.innerHeight + 'px';
  
  document.body.appendChild(particle);
  
  // Animate upward
  const animation = particle.animate([
    { transform: 'translateY(0px) rotate(0deg)', opacity: 0.5 },
    { transform: `translateY(-${window.innerHeight + 100}px) rotate(360deg)`, opacity: 0 }
  ], {
    duration: 8000 + Math.random() * 4000,
    easing: 'linear'
  });
  
  animation.addEventListener('finish', () => {
    particle.remove();
  });
}

// Create particles occasionally
setInterval(() => {
  if (Math.random() < 0.1) { // 10% chance every interval
    createParticle();
  }
}, 2000);
