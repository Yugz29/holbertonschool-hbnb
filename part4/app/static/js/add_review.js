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

// Get place-id from URL
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('place_id') || params.get('id');
}

// DOMContentLoaded
document.addEventListener('DOMContentLoaded', async () => {
  const form = document.getElementById('review-form');
  const message = document.getElementById('login-message');
  const placeId = getPlaceIdFromURL();

  // Vérifier que le placeId existe
  if (!placeId) {
      alert('No place ID provided');
      window.location.href = '/index';
      return;
  }

  // Gérer l'affichage des boutons login/logout
  const token = getCookie('token');
  const loginBtn = document.querySelector('.login-button');
  const logoutBtn = document.getElementById('logout-btn');
  
  if (token) {
      // Utilisateur connecté
      if (loginBtn) loginBtn.style.display = 'none';
      if (logoutBtn) {
          logoutBtn.style.display = 'inline-block';
          logoutBtn.addEventListener('click', () => {
              document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
              window.location.href = '/index';
          });
      }
      if (form) form.style.display = 'block';
      if (message) message.style.display = 'none';
  } else {
      // Pas connecté
      if (loginBtn) loginBtn.style.display = 'inline-block';
      if (logoutBtn) logoutBtn.style.display = 'none';
      if (form) form.style.display = 'none';
      if (message) {
          message.style.display = 'block';
          message.textContent = 'Connectez-vous pour laisser un commentaire.';
      }
  }

  // Fetch place name dynamically
  try {
      const placeResponse = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`);
      if (placeResponse.ok) {
          const place = await placeResponse.json();
          document.getElementById('place-name').textContent = place.title || place.name || 'Unknown Place';
      } else {
          document.getElementById('place-name').textContent = 'Unknown Place';
      }
  } catch (error) {
      console.error('Error fetching place:', error);
      document.getElementById('place-name').textContent = 'Unknown Place';
  }

  // Charger les reviews existantes
  fetchPlaceReviews(placeId);

  // Handle form submission
  if (form) {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const reviewText = document.getElementById('review-text').value.trim();
        const rating = document.getElementById('rating').value;

        // Vérifier que l'utilisateur est connecté avant de soumettre
        const token = getCookie('token');
        if (!token) {
            alert('You must be logged in to submit a review');
            window.location.href = '/login';
            return false;
        }

        if (!reviewText) {
            alert('Review text cannot be empty.');
            return false;
        }
        if (isNaN(rating) || rating < 1 || rating > 5) {
            alert('Rating must be a number between 1 and 5.');
            return false;
        }

        try {
            const response = await submitReview(token, placeId, reviewText, rating);
            if (response.ok) {
                alert('Review submitted successfully!');
                form.reset();
                // Rafraîchir la liste des reviews
                fetchPlaceReviews(placeId);
            } else {
                const errorData = await response.json();
                alert(errorData.error || 'Failed to submit review');
            }
        } catch (err) {
            console.error('Error submitting review:', err);
            alert('An error occurred while submitting the review.');
        }
        return false;
    });
  }

  // POST request to submit review
  async function submitReview(token, placeId, reviewText, rating) {
    return fetch(`http://127.0.0.1:5000/api/v1/reviews/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            text: reviewText,
            rating: Number.parseInt(rating, 10),
            place_id: String(placeId)
        })
    });
  }
});

// Fetch and update reviews for a place
async function fetchPlaceReviews(placeId) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/places/${placeId}/reviews`);
        if (!response.ok) throw new Error('Failed to fetch reviews');
        const reviews = await response.json();
        const reviewsSection = document.getElementById('reviews-list');
        if (!reviewsSection) return;

        reviewsSection.innerHTML = '<h3>Reviews</h3>';

        if (!reviews || reviews.length === 0) {
            reviewsSection.innerHTML += '<p>No reviews yet.</p>';
            return;
        }

        // Parcourir chaque review et récupérer le nom de l'utilisateur
        for (const review of reviews) {
            const div = document.createElement('div');
            div.classList.add('review-card');
            const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
            
            // Récupérer le nom d'utilisateur
            let userName = 'Anonymous';
            if (review.user_id) {
                try {
                    const userResponse = await fetch(`http://127.0.0.1:5000/api/v1/users/${review.user_id}`);
                    if (userResponse.ok) {
                        const user = await userResponse.json();
                        // Construire le nom complet ou utiliser l'email
                        userName = `${user.first_name || ''} ${user.last_name || ''}`.trim() || user.email || 'Anonymous';
                    }
                } catch (err) {
                    console.error('Error fetching user:', err);
                }
            }
            
            div.innerHTML = `<strong>${userName}</strong><br>${review.text}<br>Rating: ${stars}`;
            reviewsSection.appendChild(div);
        }
    } catch (err) {
        console.error(err);
        const reviewsSection = document.getElementById('reviews-list');
        if (reviewsSection) reviewsSection.innerHTML = '<p>Failed to load reviews.</p>';
    }
}
