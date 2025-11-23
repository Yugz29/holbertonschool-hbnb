document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const errorMessage = document.getElementById('error-message');

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
        document.cookie = `token=${data.access_token}; max-age=86400; path=/; SameSite=Lax`;
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
