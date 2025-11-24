document.addEventListener('DOMContentLoaded', () => {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  const logoutBtn = document.getElementById('logout-btn');

  if (token) {
      if (loginLink) loginLink.style.display = 'none';
      if (logoutBtn) logoutBtn.style.display = 'inline-block';
  } else {
      if (loginLink) loginLink.style.display = 'block';
      if (logoutBtn) logoutBtn.style.display = 'none';
  }

  if (!token) {
    if (loginLink) loginLink.style.display = 'block';
  } else {
    if (loginLink) loginLink.style.display = 'none';
  }
  fetchPlaces(token);
});

/* --- UTILITAIRE : lire un cookie --- */
function getCookie(name) {
  console.log('🔍 Tous les cookies:', document.cookie);
  const cookies = document.cookie.split(';').map(c => c.trim());
  console.log('🍪 Cookies parsés:', cookies);
  const cookie = cookies.find(c => c.startsWith(name + '='));
  console.log(`🎯 Cookie "${name}" trouvé:`, cookie);
  if (!cookie) return null;
  return cookie.split('=')[1];
}


/* --- FETCH PLACES --- */
async function fetchPlaces(token) {
  const headers = token ? { "Authorization": `Bearer ${token}` } : {};
  const result = await fetch('http://127.0.0.1:5000/api/v1/places/', {
    headers
  });

  if (!result.ok) {
    throw new Error('Unable to get Places');
  }

  const data = await result.json();
  displayPlaces(data.places);
  enableFiltering();
}

/* --- AFFICHE LES PLACES --- */
function displayPlaces(data) {
  const list = document.getElementById('places-list');
  list.innerHTML = '';

  for (const place of data) {  // keep same but ensure the function receives the correct array
    const div = document.createElement('div');
    div.classList.add('place-card');
    div.dataset.price = place.price;

    div.innerHTML = `
      <h2>${place.title}</h2>
      <p>Prix: ${place.price}€ / night</p>
      <a href="/place?id=${place.id}" class="details-button">View details</a>`;
    list.appendChild(div);
  }
}

/* --- FILTERING --- */
function enableFiltering() {
  const filter = document.getElementById('price-filter');

  filter.addEventListener('change', () => {
    const maxPrice = filter.value === "All" ? Infinity : Number.parseInt(filter.value);
    const cards = document.querySelectorAll('.place-card');

    for (const card of cards) {
      const price = Number.parseInt(card.dataset.price);
      card.style.display = price <= maxPrice ? "block" : "none";
    }
  });
}

/* --- LOGOUT --- */
document.getElementById('logout-btn')?.addEventListener('click', async () => {
  document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC";
  await fetch('/api/v1/auth/logout', { method: 'POST' });
  window.location.href = '/login';
});
