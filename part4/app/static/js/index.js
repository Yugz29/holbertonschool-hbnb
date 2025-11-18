document.addEventListener('DOMContentLoaded', () => {
    checkAuthentification();
  });

function getCookie(name) {
  const pair = document.cookie
  .split('; ')
  .find(row => row.startsWith(name + '='));
if (!pair) return undefined;
return pair.split('=')[1];
}

function checkAuthentification() {
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
}
