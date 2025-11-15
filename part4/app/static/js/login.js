document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  async function loginUser(email, password) {
    const response = await fetch("http://localhost:5000/api/v1/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    return response;
  }

  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
      const response = await loginUser(email, password);

      if (response.ok) {
        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = "index.html";
      } else {
        const errorData = await response.json();
        alert("Login Failed: " + (errorData.message || response.statusText));
      }
    } catch (err) {
      console.log(err);
      alert("An unexpected error occurred. Please try again.");
    }
  });
});
