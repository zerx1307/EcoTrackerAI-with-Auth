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
        data
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: true } },
      scales: { y: { beginAtZero: true } }
    }
  });
}

function equivalentsHTML(kg) {
  const phone = Math.floor(kg * 50);
  const bulb = Math.floor(kg * 10);
  const trees = (kg / 21.0).toFixed(3);
  return `📱 ${phone} phone charges · 💡 ${bulb} lightbulb hours · 🌳 ${trees} trees/year`;
}

document.addEventListener('DOMContentLoaded', () => {
  if (typeof SERIES !== 'undefined') {
    drawChart(SERIES);
  }
  if (typeof TOTAL !== 'undefined') {
    const eq = document.getElementById('equivalentsBox');
    if (eq) eq.innerHTML = equivalentsHTML(TOTAL);
  }

  const modal = document.getElementById('logModal');
  const openBtn = document.getElementById('openLog');
  const closeBtn = document.getElementById('closeLog');
  if (openBtn && modal) openBtn.onclick = () => { modal.classList.remove('hidden'); modal.classList.add('flex'); };
  if (closeBtn && modal) closeBtn.onclick = () => { modal.classList.add('hidden'); modal.classList.remove('flex'); };

  const form = document.getElementById('logForm');
  const result = document.getElementById('logResult');
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const entry = document.getElementById('entry').value;
      const resp = await postJSON('/api/log', { entry });
      if (resp.ok) {
        result.textContent = `Saved ${resp.co2_saved_kg} kg CO₂ (${resp.meta.category}) 🎉`;
        setTimeout(() => location.reload(), 600);
      } else {
        result.textContent = resp.error || 'Could not log entry';
      }
    });
  }
});
