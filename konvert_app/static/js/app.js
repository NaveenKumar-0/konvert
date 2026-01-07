// static/js/app.js

const API_BASE = "/auth";

// ---------- HELPERS ----------
function showMessage(msg, isError = false) {
  alert(msg);
}

function saveToken(token) {
  localStorage.setItem("access_token", token);
}

function getToken() {
  return localStorage.getItem("access_token");
}

// ---------- SIGN UP ----------
async function signup() {
  const email = document.getElementById("signup-email").value;
  const password = document.getElementById("signup-password").value;

  const res = await fetch(`${API_BASE}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await res.json();

  if (!res.ok) {
    showMessage(data.detail || "Signup failed", true);
    return;
  }

  showMessage("Verification email sent. Please check your email.");
}

// ---------- LOGIN ----------
async function login() {
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  const res = await fetch(`${API_BASE}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await res.json();

  if (!res.ok) {
    if (data.detail?.error === "EMAIL_NOT_VERIFIED") {
      showMessage("Email not verified. Click resend verification.");
    } else {
      showMessage("Invalid credentials", true);
    }
    return;
  }

  saveToken(data.access_token);
  window.location.href = "/dashboard";
}

// ---------- RESEND VERIFICATION ----------
async function resendVerification() {
  const email = document.getElementById("login-email").value;

  const res = await fetch(`${API_BASE}/resend-verification`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email }),
  });

  const data = await res.json();
  showMessage(data.message || "Verification email sent");
}

async function loadHistory() {
  const token = localStorage.getItem("access_token");
  if (!token) return;

  const res = await fetch("/convert/my-files", {
    headers: {
      "Authorization": "Bearer " + token
    }
  });

  const tableBody = document.querySelector("#historyTable tbody");

  if (!res.ok) {
    tableBody.innerHTML = `<tr><td colspan="4">Failed to load history</td></tr>`;
    return;
  }

  const data = await res.json();

  if (data.length === 0) {
    tableBody.innerHTML = `<tr><td colspan="4">No conversions yet</td></tr>`;
    return;
  }

  tableBody.innerHTML = "";

  data.forEach(item => {
    const row = `
      <tr>
        <td>${item.file_type}</td>
        <td>${new Date(item.created_at).toLocaleString()}</td>
        <td><a href="${item.original_file}" target="_blank">Download</a></td>
        <td><a href="${item.converted_file}" target="_blank">Download</a></td>
      </tr>
    `;
    tableBody.innerHTML += row;
  });
}

// Auto load when dashboard opens
if (window.location.pathname === "/dashboard") {
  loadHistory();
}

const imageForm = document.getElementById("imageForm");

if (imageForm) {
  imageForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const file = document.getElementById("imageFile").files[0];
    const format = document.getElementById("format").value;

    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("format", format);

    const token = localStorage.getItem("access_token");

    const res = await fetch("/convert/image", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`
      },
      body: formData
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail || "Conversion failed");
      return;
    }

    document.getElementById("result").innerHTML = `
      <div class="success-box">
        <h3>✅ Image Converted Successfully</h3>
        <p>Your image has been converted to <b>${format.toUpperCase()}</b>.</p>

        <div class="download-links">
          <a class="download-btn" href="${data.original_file}" target="_blank">
            ⬇ Original File
          </a>
          <a class="download-btn primary" href="${data.converted_file}" target="_blank">
            ⬇ Download Converted
          </a>
        </div>
      </div>
    `;
  });
}

loadHistory();

const videoForm = document.getElementById("videoForm");

if (videoForm) {
  videoForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const file = document.getElementById("videoFile").files[0];
    if (!file) {
      alert("Please select a video file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const token = localStorage.getItem("access_token");

    const res = await fetch("/convert/video-to-mp3", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`
      },
      body: formData
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail || "Video conversion failed");
      return;
    }

    document.getElementById("videoResult").innerHTML = `
      <div class="success-box">
        <h3>🎵 Video Converted to MP3</h3>
        <p>Your video was successfully converted.</p>

        <div class="download-links">
          <a class="download-btn" href="${data.original_file}" target="_blank">
            ⬇ Original Video
          </a>

          <a class="download-btn primary" href="${data.converted_file}" target="_blank">
            ⬇ Download MP3
          </a>
        </div>
      </div>
    `;
  });
}

loadHistory();

async function convertVideo() {
  const file = document.getElementById("videoFile").files[0];
  if (!file) {
    alert("Please select a video");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  const token = localStorage.getItem("access_token");

  const res = await fetch("/convert/video-to-mp3", {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + token
    },
    body: formData
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.detail || "Conversion failed");
    return;
  }

  document.getElementById("result").innerHTML = `
    ✅ Conversion successful <br>
    <a href="${data.converted_file}" target="_blank">⬇ Download MP3</a>
  `;
}

