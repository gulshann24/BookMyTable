/* =========================================================
   script.js — L'Gran Restaurant Platform
   ========================================================= */

// ==================== API Base ====================

const API_BASE = "http://127.0.0.1:8000/api";


// ==================== Toast Notification ====================

function showToast(message, type = "success") {
    const toast = document.getElementById("toast");
    if (!toast) return;

    toast.textContent = message;
    toast.className   = `toast ${type} show`;

    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => {
        toast.classList.remove("show");
    }, 3500);
}


// ==================== Mobile Navbar Toggle ====================

const menuToggle  = document.querySelector(".menu-toggle");
const leftLinks   = document.querySelector(".left-links");
const rightLinks  = document.querySelector(".right-links");

if (menuToggle) {
    menuToggle.addEventListener("click", () => {
        leftLinks.classList.toggle("active");
        rightLinks.classList.toggle("active");
    });
}

document.querySelectorAll(".link").forEach(link => {
    link.addEventListener("click", () => {
        leftLinks?.classList.remove("active");
        rightLinks?.classList.remove("active");
    });
});


// ==================== Scroll Reveal ====================

const allSections = document.querySelectorAll("section");

function revealSections() {
    allSections.forEach(section => {
        if (section.getBoundingClientRect().top < window.innerHeight - 100) {
            section.classList.add("show");
        }
    });
}

revealSections();
window.addEventListener("scroll", revealSections);


// ==================== Active Navbar Link ====================

const sections = document.querySelectorAll("section[id]");
const navLinks  = document.querySelectorAll(".link");

window.addEventListener("scroll", () => {
    let current = "";

    sections.forEach(section => {
        if (window.scrollY >= section.offsetTop - section.clientHeight / 3) {
            current = section.getAttribute("id");
        }
    });

    navLinks.forEach(link => {
        link.classList.remove("active");
        if (link.getAttribute("href")?.includes(current)) {
            link.classList.add("active");
        }
    });
});


// ==================== Auth Controls ====================

function renderAuthControls() {
    const container = document.getElementById("auth-controls");
    if (!container) return;

    const username = localStorage.getItem("username");
    const token    = localStorage.getItem("token");

    if (username && token) {
        container.innerHTML = `
            <div class="auth-user">
                <i class='bx bxs-user-circle'></i>
                <span class="auth-name">${username}</span>
                <button class="auth-logout" onclick="logout()">
                    <i class='bx bx-log-out'></i> Logout
                </button>
            </div>
        `;
    } else {
        container.innerHTML = `
            <a href="login.html" class="auth-login-btn">
                <i class='bx bx-log-in'></i> Sign In
            </a>
        `;
    }
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    renderAuthControls();
    showToast("You've been signed out.", "success");
}

renderAuthControls();


// ==================== Favourites ====================

function getFavourites() {
    try {
        return JSON.parse(localStorage.getItem("lgran_favourites") || "[]");
    } catch {
        return [];
    }
}

function toggleFavourite(id) {
    let favs = getFavourites();
    const idx = favs.indexOf(id);

    if (idx === -1) {
        favs.push(id);
        showToast("Added to favourites ❤️");
    } else {
        favs.splice(idx, 1);
        showToast("Removed from favourites");
    }

    localStorage.setItem("lgran_favourites", JSON.stringify(favs));

    // Update button state on card
    const btn = document.querySelector(`.rc-fav[data-id="${id}"]`);
    if (btn) {
        btn.classList.toggle("active", favs.includes(id));
    }
}


// ==================== Rating Stars ====================

function buildStars(rating) {
    const full  = Math.floor(rating);
    const half  = rating % 1 >= 0.5 ? 1 : 0;
    const empty = 5 - full - half;

    return (
        '<i class="bx bxs-star"></i>'.repeat(full) +
        (half ? '<i class="bx bxs-star-half"></i>' : '') +
        '<i class="bx bx-star"></i>'.repeat(empty)
    );
}


// ==================== Restaurant Card ====================

function buildRestaurantCard(r) {
    const favs    = getFavourites();
    const isFav   = favs.includes(r.id);
    const isOpen  = r.is_open;
    const tables  = r.available_tables;
    const mapsUrl = r.google_maps_link || `https://maps.google.com/?q=${encodeURIComponent(r.name + ' ' + r.city)}`;

    return `
    <div class="restaurant-card${!isOpen ? ' closed' : ''}" data-id="${r.id}">
        <div class="rc-image">
            <img
                src="${r.image_url}"
                alt="${r.name}"
                loading="lazy"
                onerror="this.src='https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800'"
            >
            <span class="rc-status ${isOpen ? 'open' : 'closed'}">
                ${isOpen ? '● Open Now' : '● Closed'}
            </span>
            <button
                class="rc-fav ${isFav ? 'active' : ''}"
                data-id="${r.id}"
                onclick="toggleFavourite(${r.id})"
                title="${isFav ? 'Remove from favourites' : 'Add to favourites'}"
            >
                <i class='bx ${isFav ? "bxs-heart" : "bx-heart"}'></i>
            </button>
        </div>

        <div class="rc-body">
            <div class="rc-top">
                <h3 class="rc-name">${r.name}</h3>
                <div class="rc-rating">
                    <i class='bx bxs-star'></i>
                    <span>${r.rating.toFixed(1)}</span>
                </div>
            </div>

            <div class="rc-meta">
                <span class="rc-tag cuisine">
                    <i class='bx bx-bowl-hot'></i>
                    ${r.cuisine}
                </span>
                <span class="rc-tag">
                    <i class='bx bx-map'></i>
                    ${r.city}
                </span>
                <span class="rc-tag">
                    ${r.price_range}
                </span>
                ${isOpen
                    ? `<span class="rc-tag" style="color:var(--green)">
                            <i class='bx bx-chair'></i>
                            ${tables} table${tables !== 1 ? 's' : ''} free
                       </span>`
                    : `<span class="rc-tag">
                            <i class='bx bx-time'></i>
                            Opens ${r.opening_time}
                       </span>`
                }
            </div>

            <p class="rc-address">
                <i class='bx bx-location-plus'></i>
                ${r.address}
            </p>

            <div class="rc-actions">
                <button
                    class="rc-btn-book"
                    onclick="selectRestaurant(${r.id}, '${r.name.replace(/'/g, "\\'")}')"
                    ${!isOpen ? 'disabled title="This restaurant is currently closed"' : ''}
                >
                    <i class='bx bx-calendar-check'></i>
                    ${isOpen ? 'Book Now' : 'Closed'}
                </button>
                <a class="rc-btn-map" href="${mapsUrl}" target="_blank" rel="noopener noreferrer">
                    <i class='bx bx-map-alt'></i> Maps
                </a>
            </div>
        </div>
    </div>
    `;
}


// ==================== Restaurant State ====================

let allRestaurants    = [];
let filteredRestaurants = [];


// ==================== Fetch Restaurants ====================

async function fetchRestaurants() {
    const grid    = document.getElementById("restaurant-grid");
    const loading = document.getElementById("restaurants-loading");
    const empty   = document.getElementById("restaurants-empty");

    if (!grid) return;

    loading.style.display = "block";
    empty.style.display   = "none";
    grid.innerHTML        = "";

    try {
        const res  = await fetch(`${API_BASE}/restaurants`);
        const data = await res.json();

        allRestaurants = Array.isArray(data) ? data : [];

        // Also fetch cities & cuisines for filter dropdowns
        await populateFilterDropdowns();

        applyFilters();

    } catch (err) {
        console.error("Restaurants fetch failed:", err);
        loading.style.display = "none";
        empty.style.display   = "block";
        empty.querySelector("p").textContent = "Could not connect to server. Is the backend running?";
    }
}

async function populateFilterDropdowns() {
    try {
        const [citiesRes, cuisinesRes] = await Promise.all([
            fetch(`${API_BASE}/restaurants/cities`),
            fetch(`${API_BASE}/restaurants/cuisines`)
        ]);

        const citiesData   = await citiesRes.json();
        const cuisinesData = await cuisinesRes.json();

        const citySelect    = document.getElementById("city-filter");
        const cuisineSelect = document.getElementById("cuisine-filter");

        if (citySelect && citiesData.cities) {
            citiesData.cities.forEach(city => {
                const opt = document.createElement("option");
                opt.value       = city;
                opt.textContent = city;
                citySelect.appendChild(opt);
            });
        }

        if (cuisineSelect && cuisinesData.cuisines) {
            cuisinesData.cuisines.forEach(cuisine => {
                const opt = document.createElement("option");
                opt.value       = cuisine;
                opt.textContent = cuisine;
                cuisineSelect.appendChild(opt);
            });
        }

    } catch (err) {
        console.warn("Could not load filter options:", err);
    }
}


// ==================== Apply Filters (client-side) ====================

function applyFilters() {
    const search   = document.getElementById("restaurant-search")?.value.trim().toLowerCase() || "";
    const city     = document.getElementById("city-filter")?.value || "";
    const cuisine  = document.getElementById("cuisine-filter")?.value || "";
    const sortBy   = document.getElementById("sort-filter")?.value || "rating";
    const openOnly = document.getElementById("open-only-filter")?.checked || false;

    filteredRestaurants = allRestaurants.filter(r => {
        if (search && !`${r.name} ${r.cuisine} ${r.address} ${r.city}`.toLowerCase().includes(search)) return false;
        if (city    && r.city.toLowerCase()    !== city.toLowerCase())    return false;
        if (cuisine && r.cuisine.toLowerCase() !== cuisine.toLowerCase()) return false;
        if (openOnly && !r.is_open) return false;
        return true;
    });

    if (sortBy === "rating") {
        filteredRestaurants.sort((a, b) => b.rating - a.rating);
    } else if (sortBy === "name") {
        filteredRestaurants.sort((a, b) => a.name.localeCompare(b.name));
    }

    renderRestaurants();
}

function renderRestaurants() {
    const grid    = document.getElementById("restaurant-grid");
    const loading = document.getElementById("restaurants-loading");
    const empty   = document.getElementById("restaurants-empty");

    loading.style.display = "none";

    if (!filteredRestaurants.length) {
        empty.style.display = "block";
        empty.querySelector("p").textContent = "Try adjusting your filters or search term.";
        grid.innerHTML = "";
        return;
    }

    empty.style.display = "none";
    grid.innerHTML      = filteredRestaurants.map(buildRestaurantCard).join("");
}

function resetFilters() {
    document.getElementById("restaurant-search").value  = "";
    document.getElementById("city-filter").value        = "";
    document.getElementById("cuisine-filter").value     = "";
    document.getElementById("sort-filter").value        = "rating";
    document.getElementById("open-only-filter").checked = false;
    applyFilters();
}

// Debounced search
let searchTimer;
document.getElementById("restaurant-search")?.addEventListener("input", () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(applyFilters, 280);
});

document.getElementById("city-filter")?.addEventListener("change",      applyFilters);
document.getElementById("cuisine-filter")?.addEventListener("change",   applyFilters);
document.getElementById("sort-filter")?.addEventListener("change",      applyFilters);
document.getElementById("open-only-filter")?.addEventListener("change", applyFilters);


// ==================== Restaurant Selection → Booking ====================

function selectRestaurant(id, name) {
    // Store selection
    document.getElementById("booking-restaurant-id").value   = id;
    document.getElementById("booking-restaurant-name").value = name;

    // Show banner
    const banner = document.getElementById("selected-restaurant-banner");
    const srbName = document.getElementById("srb-name");
    if (banner && srbName) {
        srbName.textContent     = name;
        banner.style.display    = "block";
    }

    // Scroll to booking
    const bookingSection = document.getElementById("booking");
    if (bookingSection) {
        bookingSection.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    showToast(`✓ ${name} selected — complete your booking below`);
}

function clearSelectedRestaurant() {
    document.getElementById("booking-restaurant-id").value   = "";
    document.getElementById("booking-restaurant-name").value = "";

    const banner = document.getElementById("selected-restaurant-banner");
    if (banner) banner.style.display = "none";

    // Scroll back to restaurant list
    document.getElementById("restaurants")?.scrollIntoView({ behavior: "smooth" });
}

// Make these globally accessible
window.selectRestaurant       = selectRestaurant;
window.clearSelectedRestaurant = clearSelectedRestaurant;
window.resetFilters           = resetFilters;
window.toggleFavourite        = toggleFavourite;


// ==================== Booking Form ====================

const bookingForm = document.getElementById("booking-form");

if (bookingForm) {
    bookingForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        const name          = document.getElementById("b-name")?.value.trim();
        const email         = document.getElementById("b-email")?.value.trim();
        const phone         = document.getElementById("b-phone")?.value.trim();
        const guests        = document.getElementById("b-guests")?.value.trim();
        const bookingDate   = document.getElementById("b-date")?.value;
        const bookingTime   = document.getElementById("b-time")?.value;
        const restaurantId  = document.getElementById("booking-restaurant-id")?.value || null;
        const restaurantName= document.getElementById("booking-restaurant-name")?.value || null;

        if (!name || !email || !phone || !guests || !bookingDate || !bookingTime) {
            showToast("Please fill in all booking fields.", "error");
            return;
        }

        const submitBtn = bookingForm.querySelector(".btn");
        submitBtn.disabled     = true;
        submitBtn.innerHTML    = '<i class="bx bx-loader-alt bx-spin"></i> Booking…';

        try {
            const token   = localStorage.getItem("token");
            const headers = { "Content-Type": "application/json" };
            if (token) headers["Authorization"] = `Bearer ${token}`;

            const body = {
                full_name:       name,
                email:           email,
                phone:           phone,
                guests:          parseInt(guests),
                booking_date:    bookingDate,
                booking_time:    bookingTime,
            };

            if (restaurantId)   body.restaurant_id   = parseInt(restaurantId);
            if (restaurantName) body.restaurant_name = restaurantName;

            const response = await fetch(`${API_BASE}/bookings/`, {
                method:  "POST",
                headers,
                body:    JSON.stringify(body)
            });

            const data = await response.json();

            if (!response.ok) throw new Error(data.detail || "Booking failed");

            const where = restaurantName ? ` at ${restaurantName}` : "";
            showToast(`🎉 Table booked${where}! Confirmation sent to ${email}`, "success");

            bookingForm.reset();
            clearSelectedRestaurant();

        } catch (error) {
            console.error(error);
            showToast("Booking failed: " + error.message, "error");
        } finally {
            submitBtn.disabled  = false;
            submitBtn.innerHTML = '<i class="bx bx-calendar-check"></i> Confirm Reservation';
        }
    });
}


// ==================== Contact Form ====================

const contactForm = document.querySelector(".contact-form");

if (contactForm) {
    contactForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        const name    = document.getElementById("name")?.value.trim();
        const email   = document.getElementById("email")?.value.trim();
        const phone   = document.getElementById("phone")?.value.trim();
        const message = document.getElementById("message")?.value.trim();

        if (!name || !email || !message) {
            showToast("Please fill all required fields.", "error");
            return;
        }

        const submitBtn       = contactForm.querySelector(".btn");
        submitBtn.disabled    = true;
        submitBtn.textContent = "Sending…";

        try {
            const response = await fetch(`${API_BASE}/contact/`, {
                method:  "POST",
                headers: { "Content-Type": "application/json" },
                body:    JSON.stringify({
                    full_name: name,
                    email:     email,
                    phone:     phone || null,
                    message:   message
                })
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || "Message failed");

            showToast("✅ Message sent! We'll get back to you soon.", "success");
            contactForm.reset();

        } catch (error) {
            console.error(error);
            showToast("Message failed: " + error.message, "error");
        } finally {
            submitBtn.disabled    = false;
            submitBtn.textContent = "Send Message";
        }
    });
}


// ==================== Init ====================

fetchRestaurants();
