document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const errorMessage = document.getElementById('error-message');

  const loginLink = document.getElementById('login-link');
  const logoutBtn = document.getElementById('logout-btn');

  const tokenCookie = document.cookie.split('; ').find(row => row.startsWith('token='));

  if (tokenCookie) {
      if (loginLink) loginLink.style.display = 'none';
      if (logoutBtn) logoutBtn.style.display = 'inline-block';
  } else {
      if (loginLink) loginLink.style.display = 'inline-block';
      if (logoutBtn) logoutBtn.style.display = 'none';
  }

  if (logoutBtn) {
      logoutBtn.addEventListener('click', () => {
          document.cookie = 'token=; path=/; max-age=0;';
          window.location.href = '/login';
      });
  }

  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    errorMessage.textContent = '';

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    if (!email || !password) {
      errorMessage.textContent = 'Please enter both email and password.';
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
        credentials: 'include'
      });

      if (response.ok) {
        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/;`;
        console.log('✅ JWT stored in cookie:', data.access_token);
        window.location.href = "/index";
      } else {
        const errorData = await response.json();
        errorMessage.textContent = errorData.message || 'Login failed. Please try again.';
      }
    } catch (err) {
        errorMessage.textContent = 'An unexpected error occurred. Please try again.';
    }
  });
});
