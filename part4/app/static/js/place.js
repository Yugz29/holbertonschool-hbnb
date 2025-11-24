document.addEventListener('DOMContentLoaded', () => {
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        console.error('Place ID not found in URL');
        return;
    }

    const loginLink = document.querySelector('.login-button');
    const logoutBtn = document.getElementById('logout-btn'); // use existing button in HTML
    if (logoutBtn) logoutBtn.style.display = 'none';

    const token = getCookie('token');

    const addReviewBtn = document.getElementById('add-review-button');

    // Show/hide Add Review button, login link and logout button
    if (token) {
        if (addReviewBtn) addReviewBtn.style.display = 'inline-block';
        if (loginLink) loginLink.style.display = 'none';
        if (logoutBtn) logoutBtn.style.display = 'inline-flex';
    } else {
        if (addReviewBtn) addReviewBtn.style.display = 'none';
        if (loginLink) loginLink.style.display = 'inline-block';
        if (logoutBtn) logoutBtn.style.display = 'none';
    }

    logoutBtn?.addEventListener('click', () => {
        document.cookie = 'token=; path=/; max-age=0; SameSite=Lax';
        window.location.href = '/login';
    });

    // Redirect to add_review.html with place_id query parameter
    if (addReviewBtn) {
        addReviewBtn.addEventListener('click', () => {
            window.location.href = `/add_review?place_id=${encodeURIComponent(placeId)}`;
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

            const userName = review.user_name || 'Anonymous';
            reviewDiv.appendChild(createText('h3', `By: ${userName}`));
            reviewDiv.appendChild(createText('p', review.text || 'No review.'));
            const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
            reviewDiv.appendChild(createText('p', `Rating: ${stars}`));
            reviewsSection.appendChild(reviewDiv);
        }
    }

    container.appendChild(reviewsSection);
}