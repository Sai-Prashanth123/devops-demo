const API = "http://127.0.0.1:8000";

async function register() {
  const email = document.getElementById("reg-email").value;
  const password = document.getElementById("reg-pass").value;

  const res = await fetch(`${API}/register`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ email, password })
  });

  alert(await res.text());
}

async function login() {
  const email = document.getElementById("log-email").value;
  const password = document.getElementById("log-pass").value;

  const res = await fetch(`${API}/login`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ email, password })
  });

  alert(await res.text());
}
