/* =========================================================
   login.js  —  Handles Login + Register for L'Gran
   ========================================================= */

const API_BASE = "http://127.0.0.1:8000/api";


// ── Tab switching ──────────────────────────────────────────

function switchTab(tab) {
    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));

    document.getElementById("tab-" + tab).classList.add("active");
    document.getElementById("panel-" + tab).classList.add("active");

    // Clear messages
    ["login-msg", "reg-msg"].forEach(id => {
        const el = document.getElementById(id);
        if (el) { el.textContent = ""; el.className = "msg"; }
    });
}


// ── Password visibility toggle ─────────────────────────────

function togglePass(inputId, btn) {
    const input = document.getElementById(inputId);
    const icon  = btn.querySelector("i");

    if (input.type === "password") {
        input.type   = "text";
        icon.className = "bx bx-show";
    } else {
        input.type   = "password";
        icon.className = "bx bx-hide";
    }
}


// ── Show message helper ────────────────────────────────────

function showMsg(id, text, type) {   // type: "error" | "success"
    const el = document.getElementById(id);
    el.textContent  = text;
    el.className    = `msg ${type} show`;
}


// ── LOGIN ──────────────────────────────────────────────────

async function handleLogin() {
    const email    = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value;

    if (!email || !password) {
        showMsg("login-msg", "Please fill in all fields.", "error");
        return;
    }

    const btn = document.getElementById("login-btn");
    btn.disabled    = true;
    btn.textContent = "Signing in…";

    try {
        const res  = await fetch(`${API_BASE}/auth/login`, {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (!res.ok) {
            showMsg("login-msg", data.detail || "Login failed.", "error");
            return;
        }

        // Persist auth info
        localStorage.setItem("token",    data.access_token);
        localStorage.setItem("username", data.username);

        showMsg("login-msg", `Welcome back, ${data.username}! Redirecting…`, "success");

        setTimeout(() => { window.location.href = "index.html"; }, 1200);

    } catch (err) {
        console.error(err);
        showMsg("login-msg", "Unable to connect to server. Is the backend running?", "error");
    } finally {
        btn.disabled    = false;
        btn.textContent = "Sign In";
    }
}


// ── REGISTER ───────────────────────────────────────────────

async function handleRegister() {
    const username = document.getElementById("reg-username").value.trim();
    const email    = document.getElementById("reg-email").value.trim();
    const password = document.getElementById("reg-password").value;
    const confirm  = document.getElementById("reg-confirm").value;

    if (!username || !email || !password || !confirm) {
        showMsg("reg-msg", "Please fill in all fields.", "error");
        return;
    }

    if (password.length < 6) {
        showMsg("reg-msg", "Password must be at least 6 characters.", "error");
        return;
    }

    if (password !== confirm) {
        showMsg("reg-msg", "Passwords do not match.", "error");
        return;
    }

    const btn = document.getElementById("reg-btn");
    btn.disabled    = true;
    btn.textContent = "Creating account…";

    try {
        const res  = await fetch(`${API_BASE}/auth/register`, {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify({ username, email, password })
        });

        const data = await res.json();

        if (!res.ok) {
            showMsg("reg-msg", data.detail || "Registration failed.", "error");
            return;
        }

        showMsg("reg-msg", "Account created! Switching to sign-in…", "success");

        // Pre-fill email and switch tab
        setTimeout(() => {
            document.getElementById("login-email").value = email;
            switchTab("login");
        }, 1400);

    } catch (err) {
        console.error(err);
        showMsg("reg-msg", "Unable to connect to server. Is the backend running?", "error");
    } finally {
        btn.disabled    = false;
        btn.textContent = "Create Account";
    }
}


// ── Enter-key support ──────────────────────────────────────

document.addEventListener("keydown", (e) => {
    if (e.key !== "Enter") return;

    const loginActive = document.getElementById("panel-login").classList.contains("active");

    if (loginActive) {
        handleLogin();
    } else {
        handleRegister();
    }
});
