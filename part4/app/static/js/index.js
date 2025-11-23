document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
  });

function getCookie(name) {
  const cookies = document.cookie.split(';').map(c => c.trim());
  const cookie = cookies.find(c => c.startsWith(name + '='));
  if (!cookie) return null;
  return cookie.split('=')[1];
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!loginLink) {
    console.warn('login-lin not found in DOM');
  }

  if (!token) {
    if (loginLink) loginLink.style.display = 'block';
    return;
  }

  if (loginLink) loginLink.style.display = 'none';

  fetchPlaces(token);
}

async function fetchPlaces(token) {
  const result = await fetch('http://127.0.0.1:5000/api/v1/places', {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  if (!result.ok) {
    throw new Error('Unable to get Places');
  }

  const data = await result.json();
  displayPlaces(data.places);
  enableFiltering();
}

function displayPlaces(data) {
  const list = document.getElementById('places-list');
  list.innerHTML = '';

  for (const place of data) {
    const div = document.createElement('div');
    div.classList.add('place-card');
    div.dataset.price = place.price;

    div.innerHTML = `
      <h2>${place.title}</h2>
      <p>Prix: ${place.price}€ / night</p>
      <a href="/place?id=${place.id}" class="details-button">View details</a>`;
    list.appendChild(div);
  };
}

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
