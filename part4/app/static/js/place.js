document.addEventListener('DOMContentLoaded', () => {
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        console.error('Place ID not found in URL');
        return;
    }

    const loginLink = document.querySelector('.login-button');
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) logoutBtn.style.display = 'none';

    const token = getCookie('token');
    const addReviewBtn = document.getElementById('add-review-button');

    if (token) {
        if (loginLink) loginLink.style.display = 'none';
        if (logoutBtn) logoutBtn.style.display = 'inline-flex';
    } else {
        if (loginLink) loginLink.style.display = 'inline-block';
        if (logoutBtn) logoutBtn.style.display = 'none';
    }

    logoutBtn?.addEventListener('click', () => {
        document.cookie = 'token=; path=/; max-age=0; SameSite=Lax';
        window.location.href = '/login';
    });

    if (addReviewBtn) {
        addReviewBtn.style.display = 'inline-block'; // Toujours visible
        
        addReviewBtn.addEventListener('click', () => {
            if (!token) {
                alert('You must be logged in to add a review.');
                window.location.href = '/login';
                return;
        }
            
            window.location.href = `/add_review?place_id=${encodeURIComponent(placeId)}`;
        });
    }

    // Charger les détails du lieu
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
    } catch (error) {
        console.error('Error fetching place details:', error);
        const placeInfoContainer = document.querySelector('.place-info');
        if (placeInfoContainer) {
            placeInfoContainer.innerHTML = '<p>Unable to load place details. Please try again later.</p>';
        }
    }
}

function createText(tag, text, className = '') {
    const element = document.createElement(tag);
    element.textContent = text;
    if (className) element.className = className;
    return element;
}

function displayPlaceDetails(place) {
    const placeInfoContainer = document.querySelector('.place-info');
    if (!placeInfoContainer) {
        console.error('Place info container not found');
        return;
    }
    placeInfoContainer.innerHTML = '';

    // Header du lieu
    const header = document.createElement('div');
    header.className = 'place-header';
    header.appendChild(createText('h1', place.title || 'Unnamed Place'));
    header.appendChild(createText('p', `Price: ${place.price ?? '—'}€ / night`, 'price'));
    placeInfoContainer.appendChild(header);

    // Description
    if (place.description) {
        placeInfoContainer.appendChild(createText('p', place.description, 'description'));
    }

    // Host info
    if (place.host_name) {
        placeInfoContainer.appendChild(createText('p', `Host: ${place.host_name}`, 'host'));
    }

    // Location
    if (place.latitude && place.longitude) {
        placeInfoContainer.appendChild(createText('p', `Location: ${place.latitude}, ${place.longitude}`, 'location'));
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
        placeInfoContainer.appendChild(amenitiesSection);
    }

    // Affiche les reviews
    displayReviews(place.reviews ?? []);
}

function displayReviews(reviews) {
    const reviewsList = document.getElementById('reviews-list');
    if (!reviewsList) {
        console.error('Reviews list container not found');
        return;
    }
    reviewsList.innerHTML = '';

    if (reviews.length === 0) {
        reviewsList.appendChild(createText('p', 'No reviews yet.'));
        return;
    }

    for (const review of reviews) {
        const reviewDiv = document.createElement('div');
        reviewDiv.className = 'review';

        const userName = review.user_name || 'Anonymous';
        reviewDiv.appendChild(createText('h3', `By: ${userName}`));
        reviewDiv.appendChild(createText('p', review.text || 'No review.'));

        const stars = '★'.repeat(review.rating || 0) + '☆'.repeat(5 - (review.rating || 0));
        reviewDiv.appendChild(createText('p', `Rating: ${stars}`, 'rating'));

        reviewsList.appendChild(reviewDiv);
    }
}
