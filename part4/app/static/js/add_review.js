// Auth
function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (const cookie of cookies) {
    const [key, value] = cookie.trim().split('=');
    if (key === name) {
      return value;
    }
  }
  return null;
}

function checkAuthentication() {
  return getCookie('token') || null;
}

// place-id
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

// DOMContentLoaded
document.addEventListener('DOMContentLoaded', async () => {
  const form = document.getElementById('review-form');
  const message = document.getElementById('login-message');
  const placeId = getPlaceIdFromURL();

  // Function to check authentication with backend
  async function isAuthenticated() {
      const token = getCookie('token');
      if (!token) return false;

      try {
          const res = await fetch('/api/v1/auth/check', {
              method: 'GET',
              credentials: 'include',
              headers: {
                  'Authorization': `Bearer ${token}`
              }
          });
          if (res.ok) {
              const data = await res.json();
              return data.authenticated === true;
          }
      } catch (err) {
          console.error(err);
      }
      return false;
  }

  const loggedIn = await isAuthenticated();

  if (!loggedIn) {
      if (form) form.style.display = 'none';
      if (message) message.style.display = 'block';
      return;
  }

  if (form) form.style.display = 'block';
  if (message) message.style.display = 'none';

  // Fetch place name dynamically
  try {
      const placeResponse = await fetch('http://127.0.0.1:5000/api/v1/places/' + placeId, {
          credentials: 'include'
      });
      if (placeResponse.ok) {
          const place = await placeResponse.json();
          document.getElementById('place-name').textContent = place.name;
      } else {
          document.getElementById('place-name').textContent = 'Unknown Place';
      }
  } catch (error) {
      console.error('Error fetching place:', error);
      document.getElementById('place-name').textContent = 'Unknown Place';
  }

  // Only attach submit fetch if authenticated
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      e.stopPropagation();
      const reviewText = document.getElementById('review-text').value.trim();
      let rating = parseInt(document.getElementById('rating').value);
      if (isNaN(rating) || rating < 0 || rating > 5) {
        alert('Rating must be a number between 0 and 5.');
        return false;
      }

      try {
        const token = getCookie('token');
        const response = await submitReview(token, placeId, reviewText, rating);
        handleResponse(response, form);
      } catch (err) {
        console.error('Error submitting review:', err);
      }
      return false;
    });
  }

  // POST request
  async function submitReview(token, placeId, reviewText, rating) {
    return fetch(`/api/v1/reviews/places/${encodeURIComponent(placeId)}/reviews`, {
        credentials: 'include',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
            text: reviewText,
            rating: rating
        })
    });
  }

  // Success / Error
  function handleResponse(response, form) {
    if (response.ok) {
        alert('Review submitted successfully!');
        form.reset();
    } else {
        alert('Failed to submit review');
    }
  }
});
