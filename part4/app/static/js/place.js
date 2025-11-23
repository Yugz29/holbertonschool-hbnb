document.addEventListener('DOMContentLoaded', () => {
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        console.error('Place ID not found in URL');
        return;
    }

    const token = getCookie('token');

    const addReviewBtn = document.getElementById('add-review-button');
    const loginBtn = document.querySelector('.login-button');
    const reviewForm = document.getElementById('review-form-container');
    const form = document.getElementById('review-form');

    // Show/hide Add Review button and login link
    if (token) {
        if (addReviewBtn) addReviewBtn.style.display = 'inline-block';
        if (loginBtn) loginBtn.style.display = 'none';
    } else {
        if (addReviewBtn) addReviewBtn.style.display = 'none';
        if (loginBtn) loginBtn.style.display = 'inline-block';
    }

    // Toggle review form
    if (addReviewBtn && reviewForm) {
        addReviewBtn.addEventListener('click', () => {
            reviewForm.style.display = reviewForm.style.display === 'none' ? 'block' : 'none';
        });
    }

    // Handle review form submission
    if (form && token) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const reviewText = document.getElementById('review-text').value.trim();
            const rating = Number.parseInt(document.getElementById('review-rating').value);

            if (!reviewText) {
                alert('Review text cannot be empty.');
                return;
            }
            if (Number.isNaN(rating) || rating < 0 || rating > 5) {
                alert('Rating must be between 0 and 5.');
                return;
            }

            // Log values and check for missing placeId/token
            console.log('Submitting review for placeId:', placeId, 'with token:', token);
            if (!placeId) {
                alert('Place ID is missing. Cannot submit review.');
                return;
            }
            if (!token) {
                alert('You are not logged in. Cannot submit review.');
                return;
            }

            try {
                const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    credentials: 'include',
                    body: JSON.stringify({
                        text: reviewText,
                        rating: Number.parseInt(rating, 10),
                        place_id: String(placeId)
                    })
                });

                if (!response.ok) throw new Error('Failed to submit review');

                form.reset();
                fetchPlaceDetails(placeId); // refresh details and reviews
            } catch (err) {
                console.error('Error submitting review:', err);
                alert(err.message);
            }
        });
    }

    // Load place details with token for authentication
    fetchPlaceDetails(placeId, token);
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

async function fetchPlaceDetails(placeId, token) {
    if (!placeId) {
        console.error('Place ID is required');
        return;
    }

    try {
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${encodeURIComponent(placeId)}`, {
            method: 'GET',
            headers,
            credentials: 'include'
        });

        if (!response.ok) throw new Error(`Unable to fetch place details (HTTP ${response.status})`);

        const data = await response.json();
        const place = data.place ?? data;
        displayPlaceDetails(place);
    } catch (err) {
        console.error('Error fetching place details:', err);
        const container = document.getElementById('place-details');
        if (container) {
            container.innerHTML = '<p>Error loading place details. Please try again later.</p>';
        }
    }
}

function createText(tag, text, className) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    element.textContent = text;
    return element;
}

function displayPlaceDetails(place) {
    const container = document.getElementById('place-details');
    if (!container) {
        console.error('Place details container not found');
        return;
    }
    container.innerHTML = '';

    const header = document.createElement('div');
    header.className = 'place-header';
    header.appendChild(createText('h1', place.title || 'Unnamed Place'));
    header.appendChild(createText('p', `Price: ${place.price ?? '—'}€ / night`, 'price'));
    container.appendChild(header);

    if (place.description) {
        container.appendChild(createText('p', place.description, 'description'));
    }

    if (Array.isArray(place.amenities) && place.amenities.length > 0) {
        const amenitiesSection = document.createElement('div');
        amenitiesSection.className = 'amenities';
        amenitiesSection.appendChild(createText('h2', 'Amenities'));
        const ul = document.createElement('ul');
        for (const amenity of place.amenities) {
            ul.appendChild(createText('li', amenity.name || amenity));
        }
        amenitiesSection.appendChild(ul);
        container.appendChild(amenitiesSection);
    }

    const reviewsSection = document.createElement('div');
    reviewsSection.className = 'reviews';
    reviewsSection.appendChild(createText('h2', 'Reviews'));

    const reviews = place.reviews ?? [];
    if (reviews.length === 0) {
        reviewsSection.appendChild(createText('p', 'No reviews yet.'));
    } else {
        for (const review of reviews) {
            const reviewDiv = document.createElement('div');
            reviewDiv.className = 'review';
            reviewDiv.appendChild(createText('h3', `By: ${review.user_name || 'Anonymous'}`));
            reviewDiv.appendChild(createText('p', review.text || 'No review.'));
            const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
            reviewDiv.appendChild(createText('p', `Rating: ${stars}`));
            reviewsSection.appendChild(reviewDiv);
        }
    }

    container.appendChild(reviewsSection);
}