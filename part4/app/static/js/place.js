document.addEventListener('DOMContentLoaded', () => {
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        console.error('Place ID not found in URL');
        return;
    }

    // Vérifier côté serveur si l'utilisateur est connecté
    fetch('/api/v1/auth/check', { method: 'GET', credentials: 'include' })
        .then(res => res.json())
        .then(data => {
            const addReviewBtn = document.getElementById('add-review-button');
            const loginBtn = document.querySelector('.login-button');

            if (data.authenticated) {
                if (addReviewBtn) addReviewBtn.style.display = 'inline-block';
                if (loginBtn) loginBtn.style.display = 'none';
            } else {
                if (addReviewBtn) addReviewBtn.style.display = 'none';
                if (loginBtn) loginBtn.style.display = 'inline-block';
            }

            // Ajouter toggle du formulaire Add Review
            const reviewForm = document.getElementById('review-form-container');
            if (addReviewBtn && reviewForm) {
                addReviewBtn.addEventListener('click', () => {
                    reviewForm.style.display = reviewForm.style.display === 'none' ? 'block' : 'none';
                });
            }

            // Load the place details, the HttpOnly cookie is included automatically
            fetchPlaceDetails(placeId);
        })
        .catch(err => {
            console.error('Auth check failed:', err);
            fetchPlaceDetails(placeId);
        });
});

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

async function fetchPlaceDetails(placeId) {
    if (!placeId) {
        console.error('Place ID is required');
        return;
    }

    const url = `/api/v1/places/${encodeURIComponent(placeId)}`;
    try {
        const response = await fetch(url, { method: 'GET', credentials: 'include' });
        if (!response.ok) {
            throw new Error(`Unable to fetch place details (HTTP ${response.status})`);
        }
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

    // Header: title and price
    const header = document.createElement('div');
    header.className = 'place-header';
    header.appendChild(createText('h1', place.title || 'Unnamed Place'));
    header.appendChild(createText('p', `Price: ${place.price ?? '—'}€ / night`, 'price'));
    container.appendChild(header);

    // Description
    if (place.description) {
        container.appendChild(createText('p', place.description, 'description'));
    }

    // Amenities
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

    // Reviews
    const reviewsSection = document.createElement('div');
    reviewsSection.className = 'reviews';
    reviewsSection.appendChild(createText('h2', 'Reviews'));

    if (Array.isArray(place.reviews) && place.reviews.length > 0) {
        for (const review of place.reviews) {
            const reviewDiv = document.createElement('div');
            reviewDiv.className = 'review';
            reviewDiv.appendChild(createText('h3', `By: ${review.user_name || 'Anonymous'}`));
            reviewDiv.appendChild(createText('p', review.text || 'No review.'));
            reviewsSection.appendChild(reviewDiv);
        }
    } else {
        reviewsSection.appendChild(createText('p', 'No reviews yet.'));
    }

    container.appendChild(reviewsSection);
}