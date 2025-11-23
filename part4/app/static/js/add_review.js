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
  const token = getCookie('token');
  if (!token) {
    window.location.href = 'index.html';
  }
  return token;
}

// place-id
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

// DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('review-form');
  const token = checkAuthentication();
  const placeId = getPlaceIdFromURL();

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const reviewText = document.getElementById('review-text').value;

    const response = await submitReview(token, placeId, reviewText);
    handleResponse(response, form);
  });
});

// POST request
async function submitReview(token, placeId, reviewText) {
    return fetch('http://localhost:5001/api/v1/places/' + placeId + '/reviews', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
            text: reviewText,
            place_id: placeId
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
