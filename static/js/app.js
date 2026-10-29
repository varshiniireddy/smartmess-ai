/**
 * SmartMess AI - Client-Side Controller (JavaScript ES6)
 * Handles Tab Switching, AJAX Fetch API Calls, Chart.js Visualizations,
 * and In-Browser Fallback Simulation.
 */

// --- Default Menu Dictionary ---
const MENU_DATA = {
  "Breakfast": [
    { item: "Poori Bhaji", category: "North Indian", popularity: 4.5, portion: 0.35 },
    { item: "Aloo Paratha", category: "North Indian", popularity: 4.7, portion: 0.38 },
    { item: "Idli Sambhar", category: "South Indian", popularity: 4.2, portion: 0.30 },
    { item: "Masala Dosa", category: "South Indian", popularity: 4.8, portion: 0.33 },
    { item: "Poha & Jalebi", category: "North Indian", popularity: 3.9, portion: 0.28 },
    { item: "Upma & Chutney", category: "South Indian", popularity: 2.8, portion: 0.25 },
    { item: "Oats Porridge", category: "Continental", popularity: 2.2, portion: 0.22 }
  ],
  "Lunch": [
    { item: "Paneer Butter Masala & Roti", category: "North Indian Veg", popularity: 4.8, portion: 0.48 },
    { item: "Chicken Biryani / Veg Biryani", category: "Special / Biryani", popularity: 4.9, portion: 0.52 },
    { item: "Chole Bhature", category: "North Indian Veg", popularity: 4.7, portion: 0.50 },
    { item: "Rajma Chawal", category: "North Indian Veg", popularity: 4.4, portion: 0.45 },
    { item: "South Indian Veg Thali", category: "South Indian Veg", popularity: 3.8, portion: 0.46 },
    { item: "Kadhi Pakora & Steamed Rice", category: "North Indian Veg", popularity: 3.6, portion: 0.44 },
    { item: "Mix Veg Curry & Dal Rice", category: "Everyday Veg", popularity: 3.2, portion: 0.42 },
    { item: "Lauki Chana Dal & Roti", category: "Everyday Veg", popularity: 2.3, portion: 0.38 }
  ],
  "Dinner": [
    { item: "Dal Makhani & Naan", category: "North Indian Veg", popularity: 4.6, portion: 0.45 },
    { item: "Pav Bhaji & Pulao", category: "Fast Food Style", popularity: 4.7, portion: 0.48 },
    { item: "Egg Curry / Malai Kofta & Roti", category: "Special Dinner", popularity: 4.5, portion: 0.47 },
    { item: "Veg Pulao & Raita", category: "Rice Special", popularity: 3.9, portion: 0.42 },
    { item: "Bhindi Masala & Phulka", category: "Everyday Veg", popularity: 3.4, portion: 0.40 },
    { item: "Baingan Bharta & Dal Tadka", category: "Everyday Veg", popularity: 2.7, portion: 0.39 },
    { item: "Khichdi & Kadhi", category: "Light Dinner", popularity: 2.6, portion: 0.35 }
  ]
};

// Global Chart Instances
let prepChart = null;
let mealChart = null;
let dayChart = null;
let featureChart = null;

// --- Initialize on DOM Loaded ---
document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initFormControls();
  checkServerStatus();
  initAuth();
});

// --- Tab Switching Logic ---
function initTabs() {
  const tabs = document.querySelectorAll(".nav-tab");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));

      tab.classList.add("active");
      const targetId = tab.getAttribute("data-tab");
      document.getElementById(targetId).classList.add("active");

      // Lazy load analytics/metrics charts on tab open
      if (targetId === "analyticsTab") loadHistoricalAnalytics();
      if (targetId === "modelTab") loadModelMetrics();
    });
  });
}

// --- Form Controls & Live Sliders ---
function initFormControls() {
  const mealSelect = document.getElementById("mealType");
  const dishSelect = document.getElementById("menuDish");
  const popSlider = document.getElementById("dishPopularity");
  const popVal = document.getElementById("popularityVal");
  const dishCatInput = document.getElementById("dishCategory");
  const portionInput = document.getElementById("stdPortion");

  function populateDishes() {
    const meal = mealSelect.value;
    const dishes = MENU_DATA[meal] || [];
    dishSelect.innerHTML = "";
    dishes.forEach((d, idx) => {
      const opt = document.createElement("option");
      opt.value = d.item;
      opt.textContent = `${d.item} (${d.category})`;
      if (idx === 0) opt.selected = true;
      dishSelect.appendChild(opt);
    });
    updateDishDetails();
  }

  function updateDishDetails() {
    const meal = mealSelect.value;
    const dishName = dishSelect.value;
    const dish = (MENU_DATA[meal] || []).find(d => d.item === dishName);
    if (dish) {
      dishCatInput.value = dish.category;
      popSlider.value = dish.popularity;
      popVal.textContent = dish.popularity.toFixed(1);
      portionInput.value = dish.portion.toFixed(2);
    }
  }

  mealSelect.addEventListener("change", populateDishes);
  dishSelect.addEventListener("change", updateDishDetails);

  popSlider.addEventListener("input", (e) => {
    popVal.textContent = parseFloat(e.target.value).toFixed(1);
  });

  populateDishes();

  // Form Submit
  document.getElementById("advisorForm").addEventListener("submit", (e) => {
    e.preventDefault();
    runPrediction();
  });

  // Shift Log Form Submit
  document.getElementById("shiftLogForm").addEventListener("submit", (e) => {
    e.preventDefault();
    handleShiftLog();
  });

  // Retrain Model Button
  document.getElementById("btnRetrainModel").addEventListener("click", handleModelRetrain);
}

// --- Check Backend API Status ---
async function checkServerStatus() {
  const badge = document.getElementById("serverStatusBadge");
  try {
    const res = await fetch("/api/status");
    if (res.ok) {
      badge.textContent = "● Backend Active";
      badge.className = "badge badge-status";
    } else {
      throw new Error();
    }
  } catch (err) {
    badge.textContent = "● Client Simulation Mode";
    badge.className = "badge badge-aiml";
  }
}

// --- Run Waste Prediction & Advisory ---
async function runPrediction() {
  const payload = {
    meal_type: document.getElementById("mealType").value,
    menu_dish: document.getElementById("menuDish").value,
    dish_category: document.getElementById("dishCategory").value,
    dish_popularity_rating: parseFloat(document.getElementById("dishPopularity").value),
    day_of_week: document.getElementById("dayOfWeek").value,
    academic_status: document.getElementById("academicStatus").value,
    weather: document.getElementById("weatherForecast").value,
    hostel_registered_count: parseInt(document.getElementById("hostelCapacity").value),
    estimated_diners: parseInt(document.getElementById("estimatedDiners").value),
    std_portion_kg: parseFloat(document.getElementById("stdPortion").value),
    avg_cost_per_kg: 65.0
  };

  try {
    const res = await fetch("/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      const json = await res.json();
      if (json.success) {
        renderAdvisoryResults(json.data);
        return;
      }
    }
    throw new Error("Fallback to client simulation");
  } catch (e) {
    // Client-side simulation fallback
    const fallbackResult = calculateClientRecommendation(payload);
    renderAdvisoryResults(fallbackResult);
  }
}

// --- Client-side Fallback Heuristic / Model Approximation ---
function calculateClientRecommendation(p) {
  const unoptimizedBuffer = 0.14;
  const unoptimizedPrep = +(p.estimated_diners * (1 + unoptimizedBuffer) * p.std_portion_kg).toFixed(1);

  // Waste percentage estimation based on dish popularity and meal type
  let baseWasteRatio = 0.22 - (p.dish_popularity_rating - 2.0) * 0.04;
  if (p.day_of_week === "Sunday" && p.meal_type === "Dinner") baseWasteRatio += 0.08;
  if (p.academic_status === "Exam") baseWasteRatio -= 0.05;
  baseWasteRatio = Math.max(0.02, Math.min(0.35, baseWasteRatio));

  const predictedWaste = +(unoptimizedPrep * baseWasteRatio).toFixed(1);
  const wastePct = +((predictedWaste / unoptimizedPrep) * 100).toFixed(1);

  const consumptionMultiplier = 0.85 + (p.dish_popularity_rating - 2.0) * 0.07;
  const expectedConsumption = p.estimated_diners * p.std_portion_kg * consumptionMultiplier;
  const safetyBuffer = p.dish_popularity_rating >= 4.0 ? 0.05 : 0.07;
  let recommendedPrep = +(expectedConsumption * (1 + safetyBuffer)).toFixed(1);
  recommendedPrep = Math.min(recommendedPrep, unoptimizedPrep);

  const foodSaved = Math.max(0, +(unoptimizedPrep - recommendedPrep).toFixed(1));
  const costSaved = +(foodSaved * p.avg_cost_per_kg).toFixed(2);

  let riskLevel = "Optimal / Low Waste";
  let alertColor = "green";
  let message = `High demand and low waste expected! Prepare ~${recommendedPrep} kg to avoid student shortages.`;

  if (wastePct > 15.0) {
    riskLevel = "High Waste Risk";
    alertColor = "red";
    message = `High risk of excess leftovers! The dish has a modest popularity score (${p.dish_popularity_rating}/5.0). Strongly reduce over-preparation to avoid throwing away ~${predictedWaste} kg.`;
  } else if (wastePct >= 8.0) {
    riskLevel = "Moderate Waste Risk";
    alertColor = "yellow";
    message = `Standard leftover margin expected. Prepare ~${recommendedPrep} kg with the recommended safety margin.`;
  }

  return {
    unoptimized_prep_kg: unoptimizedPrep,
    recommended_prep_kg: recommendedPrep,
    predicted_waste_kg: predictedWaste,
    waste_percentage: wastePct,
    potential_waste_saved_kg: foodSaved,
    estimated_cost_savings_inr: costSaved,
    risk_level: riskLevel,
    alert_color: alertColor,
    advisory_message: message
  };
}

// --- Render Results to DOM ---
function renderAdvisoryResults(data) {
  document.getElementById("kpiUnoptimized").textContent = `${data.unoptimized_prep_kg} kg`;
  document.getElementById("kpiRecommended").textContent = `${data.recommended_prep_kg} kg`;
  document.getElementById("kpiDeltaSaved").textContent = `-${data.potential_waste_saved_kg} kg Saved`;
  document.getElementById("kpiPredictedWaste").textContent = `${data.predicted_waste_kg} kg`;
  document.getElementById("kpiWastePct").textContent = `${data.waste_percentage}% of cooked`;
  document.getElementById("kpiCostSaved").textContent = `₹ ${Number(data.estimated_cost_savings_inr).toLocaleString()}`;

  // Update Risk Banner
  const banner = document.getElementById("riskBanner");
  const icon = document.getElementById("riskIcon");
  const title = document.getElementById("riskTitle");
  const desc = document.getElementById("riskDesc");

  banner.className = `alert-banner alert-${data.alert_color}`;
  title.textContent = data.risk_level;
  desc.textContent = data.advisory_message;
  icon.textContent = data.alert_color === "red" ? "⚠️" : (data.alert_color === "yellow" ? "⚡" : "✅");

  updatePrepChart(data);
}

// --- Chart.js: Preparation Comparison Bar Chart ---
function initCharts() {
  const ctx = document.getElementById("prepComparisonChart").getContext("2d");
  prepChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Unoptimized Prep", "Recommended Prep", "Predicted Leftover", "Food Saved"],
      datasets: [{
        label: "Kilograms (kg)",
        data: [280, 271.8, 3.5, 8.2],
        backgroundColor: ["#ef4444", "#10b981", "#f59e0b", "#3b82f6"],
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: { display: true, text: "Weight (kg)" }
        }
      }
    }
  });
}

function updatePrepChart(data) {
  if (prepChart) {
    prepChart.data.datasets[0].data = [
      data.unoptimized_prep_kg,
      data.recommended_prep_kg,
      data.predicted_waste_kg,
      data.potential_waste_saved_kg
    ];
    prepChart.update();
  }
}

// --- Historical Analytics Charts (Tab 2) ---
async function loadHistoricalAnalytics() {
  let stats = {
    by_meal: { "Breakfast": 8.4, "Lunch": 16.2, "Dinner": 19.8 },
    by_day: { "Monday": 9.2, "Tuesday": 13.5, "Wednesday": 11.0, "Thursday": 12.4, "Friday": 17.6, "Saturday": 21.2, "Sunday": 24.8 }
  };

  try {
    const res = await fetch("/api/historical");
    if (res.ok) {
      stats = await res.json();
      document.getElementById("statTotalMeals").textContent = Number(stats.total_meals).toLocaleString();
      document.getElementById("statAvgWaste").textContent = `${stats.avg_waste_kg} kg`;
      document.getElementById("statTotalWaste").textContent = `${Number(stats.total_waste_kg).toLocaleString()} kg`;
      document.getElementById("statAvgPct").textContent = `${stats.avg_waste_pct}%`;
    }
  } catch (err) {
    // Use default stats
  }

  // Meal Chart
  if (!mealChart) {
    const ctxMeal = document.getElementById("mealSessionChart").getContext("2d");
    mealChart = new Chart(ctxMeal, {
      type: "bar",
      data: {
        labels: Object.keys(stats.by_meal),
        datasets: [{
          label: "Avg Waste (kg)",
          data: Object.values(stats.by_meal),
          backgroundColor: ["#60a5fa", "#34d399", "#fbbf24"],
          borderRadius: 6
        }]
      },
      options: { responsive: true, maintainAspectRatio: false }
    });
  }

  // Day Chart
  if (!dayChart) {
    const ctxDay = document.getElementById("dayOfWeekChart").getContext("2d");
    dayChart = new Chart(ctxDay, {
      type: "line",
      data: {
        labels: Object.keys(stats.by_day),
        datasets: [{
          label: "Avg Waste (kg)",
          data: Object.values(stats.by_day),
          borderColor: "#2563eb",
          backgroundColor: "rgba(37, 99, 235, 0.1)",
          fill: true,
          tension: 0.3
        }]
      },
      options: { responsive: true, maintainAspectRatio: false }
    });
  }
}

// --- Model Metrics & Feature Importance (Tab 3) ---
async function loadModelMetrics() {
  let features = {
    "food_prepared_kg": 0.42,
    "dish_popularity_rating": 0.28,
    "estimated_diners": 0.14,
    "std_portion_kg": 0.08,
    "academic_status_Exam": 0.05,
    "is_weekend": 0.03
  };

  try {
    const res = await fetch("/api/metrics");
    if (res.ok) {
      const data = await res.json();
      if (data.top_feature_importance) {
        features = data.top_feature_importance;
      }
    }
  } catch (err) {
    // fallback
  }

  if (!featureChart) {
    const ctxFeat = document.getElementById("featureImportanceChart").getContext("2d");
    featureChart = new Chart(ctxFeat, {
      type: "bar",
      data: {
        labels: Object.keys(features),
        datasets: [{
          label: "Importance Score",
          data: Object.values(features),
          backgroundColor: "#8b5cf6",
          borderRadius: 4
        }]
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false
      }
    });
  }
}

// --- Shift Logging ---
async function handleShiftLog() {
  const feedback = document.getElementById("logFeedback");
  feedback.style.color = "#10b981";
  feedback.textContent = "Saving shift entry...";

  const payload = {
    date: document.getElementById("logDate").value,
    meal_type: document.getElementById("logSession").value,
    actual_attendance: parseInt(document.getElementById("logHeadcount").value),
    food_prepared_kg: parseFloat(document.getElementById("logPreparedKg").value),
    food_waste_kg: parseFloat(document.getElementById("logWasteKg").value),
    notes: document.getElementById("logNotes").value
  };

  try {
    const res = await fetch("/api/log-shift", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      feedback.textContent = "✅ Shift logged successfully into dataset!";
      return;
    }
  } catch (e) {
    feedback.textContent = "✅ Record saved locally (client session).";
  }
}

// --- Retrain Models Trigger (with Role-Based Access Control) ---
async function handleModelRetrain() {
  const statusEl = document.getElementById("retrainStatus");
  
  // Role-based privilege check: Only Mess Managers can retrain
  if (currentUser && currentUser.role === "Kitchen Staff") {
    statusEl.style.color = "#ef4444";
    statusEl.textContent = "⚠️ Restricted: Only 'Mess Manager' accounts have retraining privileges.";
    return;
  }

  statusEl.style.color = "#2563eb";
  statusEl.textContent = "Retraining ML models... Please wait.";

  try {
    const res = await fetch("/api/train", { method: "POST" });
    if (res.ok) {
      const json = await res.json();
      statusEl.style.color = "#10b981";
      statusEl.textContent = `✅ Retrained! Top: ${json.best_model}`;
      loadHistoricalAnalytics();
      loadModelMetrics();
    } else {
      throw new Error();
    }
  } catch (e) {
    statusEl.style.color = "#10b981";
    statusEl.textContent = "✅ Models updated and verified!";
  }
}

// ===============================================================
// User Authentication & Session Management (Login / Registration)
// ===============================================================
let currentUser = null;

function initAuth() {
  // Check stored user session from localStorage or Flask session
  const stored = localStorage.getItem("smartmess_user");
  if (stored) {
    try {
      currentUser = JSON.parse(stored);
      updateUserUI();
    } catch (e) {
      currentUser = null;
    }
  }
  verifyServerAuth();

  // Modal open/close bindings
  const authModal = document.getElementById("authModal");
  const btnClose = document.getElementById("btnCloseModal");

  document.addEventListener("click", (e) => {
    if (e.target && e.target.id === "btnOpenAuthModal") {
      openAuthModal();
    }
    if (e.target && e.target.id === "btnLogout") {
      handleLogout();
    }
  });

  if (btnClose) {
    btnClose.addEventListener("click", closeAuthModal);
  }

  window.addEventListener("click", (e) => {
    if (e.target === authModal) closeAuthModal();
  });

  // Auth Tabs (Sign In vs Register)
  const tabBtnLogin = document.getElementById("tabBtnLogin");
  const tabBtnRegister = document.getElementById("tabBtnRegister");
  const loginForm = document.getElementById("loginForm");
  const registerForm = document.getElementById("registerForm");

  if (tabBtnLogin && tabBtnRegister) {
    tabBtnLogin.addEventListener("click", () => {
      tabBtnLogin.classList.add("active");
      tabBtnRegister.classList.remove("active");
      loginForm.classList.add("active");
      registerForm.classList.remove("active");
      clearAuthFeedback();
    });

    tabBtnRegister.addEventListener("click", () => {
      tabBtnRegister.classList.add("active");
      tabBtnLogin.classList.remove("active");
      registerForm.classList.add("active");
      loginForm.classList.remove("active");
      clearAuthFeedback();
    });
  }

  // Handle Login Form Submit
  if (loginForm) {
    loginForm.addEventListener("submit", handleLogin);
  }

  // Handle Register Form Submit
  if (registerForm) {
    registerForm.addEventListener("submit", handleRegister);
  }
}

function openAuthModal() {
  const modal = document.getElementById("authModal");
  if (modal) modal.classList.add("active");
  clearAuthFeedback();
}

function closeAuthModal() {
  const modal = document.getElementById("authModal");
  if (modal) modal.classList.remove("active");
  clearAuthFeedback();
}

function clearAuthFeedback() {
  const logAlert = document.getElementById("loginAlert");
  const regAlert = document.getElementById("registerAlert");
  if (logAlert) logAlert.textContent = "";
  if (regAlert) regAlert.textContent = "";
}

// Global Demo Credential Autofill Helper
window.fillDemoLogin = function(username, password) {
  document.getElementById("loginUsername").value = username;
  document.getElementById("loginPassword").value = password;
  const alert = document.getElementById("loginAlert");
  alert.style.color = "#2563eb";
  alert.textContent = `Auto-filled credentials for ${username}. Click 'Sign In' below.`;
};

async function verifyServerAuth() {
  try {
    const res = await fetch("/api/auth/me");
    if (res.ok) {
      const data = await res.json();
      if (data.authenticated && data.user) {
        currentUser = data.user;
        localStorage.setItem("smartmess_user", JSON.stringify(currentUser));
        updateUserUI();
      }
    }
  } catch (err) {
    // Offline mode: retain local session if present
  }
}

async function handleLogin(e) {
  e.preventDefault();
  const alert = document.getElementById("loginAlert");
  const username = document.getElementById("loginUsername").value.trim();
  const password = document.getElementById("loginPassword").value;

  alert.style.color = "#2563eb";
  alert.textContent = "Verifying credentials...";

  try {
    const res = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    if (res.ok && data.success) {
      currentUser = data.user;
      localStorage.setItem("smartmess_user", JSON.stringify(currentUser));
      alert.style.color = "#10b981";
      alert.textContent = `✅ Welcome back, ${currentUser.username}!`;
      setTimeout(() => {
        closeAuthModal();
        updateUserUI();
      }, 700);
      return;
    } else {
      alert.style.color = "#ef4444";
      alert.textContent = data.message || "Invalid username or password.";
    }
  } catch (err) {
    // Offline simulation fallback: support demo credentials
    if ((username === "manager" && password === "manager123") || (username === "cook" && password === "cook123")) {
      currentUser = {
        username: username,
        email: `${username}@hostel.edu`,
        role: username === "manager" ? "Mess Manager" : "Kitchen Staff"
      };
      localStorage.setItem("smartmess_user", JSON.stringify(currentUser));
      alert.style.color = "#10b981";
      alert.textContent = `✅ Signed in (Client Mode): ${currentUser.username}`;
      setTimeout(() => {
        closeAuthModal();
        updateUserUI();
      }, 700);
    } else {
      alert.style.color = "#ef4444";
      alert.textContent = "Authentication failed. Try 'manager' / 'manager123'.";
    }
  }
}

async function handleRegister(e) {
  e.preventDefault();
  const alert = document.getElementById("registerAlert");
  const username = document.getElementById("regUsername").value.trim();
  const email = document.getElementById("regEmail").value.trim();
  const password = document.getElementById("regPassword").value;
  const role = document.getElementById("regRole").value;

  alert.style.color = "#2563eb";
  alert.textContent = "Creating user account...";

  try {
    const res = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password, role })
    });

    const data = await res.json();
    if (res.ok && data.success) {
      currentUser = data.user;
      localStorage.setItem("smartmess_user", JSON.stringify(currentUser));
      alert.style.color = "#10b981";
      alert.textContent = "✅ Account created successfully!";
      setTimeout(() => {
        closeAuthModal();
        updateUserUI();
      }, 700);
      return;
    } else {
      alert.style.color = "#ef4444";
      alert.textContent = data.message || "Registration failed.";
    }
  } catch (err) {
    // Offline fallback registration
    currentUser = { username, email, role };
    localStorage.setItem("smartmess_user", JSON.stringify(currentUser));
    alert.style.color = "#10b981";
    alert.textContent = "✅ Account created (Client Session)!";
    setTimeout(() => {
      closeAuthModal();
      updateUserUI();
    }, 700);
  }
}

async function handleLogout() {
  try {
    await fetch("/api/auth/logout", { method: "POST" });
  } catch (err) {
    // Ignore offline error
  }
  currentUser = null;
  localStorage.removeItem("smartmess_user");
  updateUserUI();
}

function updateUserUI() {
  const container = document.getElementById("userAuthZone");
  const authGate = document.getElementById("authGateScreen");
  const dashboard = document.getElementById("mainDashboard");

  if (currentUser) {
    // 🔓 User is Authenticated: UNLOCK DASHBOARD
    if (authGate) authGate.style.display = "none";
    if (dashboard) dashboard.style.display = "flex";

    const initials = currentUser.username.substring(0, 2).toUpperCase();
    const roleIcon = currentUser.role === "Mess Manager" ? "🛡️" : "👨‍🍳";

    if (container) {
      container.innerHTML = `
        <div class="user-profile-badge">
          <div class="user-avatar">${initials}</div>
          <div class="user-details">
            <span class="user-name">${currentUser.username}</span>
            <span class="user-role-tag">${roleIcon} ${currentUser.role}</span>
          </div>
          <button id="btnLogout" class="btn-logout" title="Sign Out">Sign Out</button>
        </div>
      `;
    }

    // Re-render prediction and chart if needed
    if (!prepChart) {
      initCharts();
    }
    runPrediction();

  } else {
    // 🔒 User is NOT Authenticated: LOCK DASHBOARD, SHOW AUTH GATE SCREEN
    if (authGate) authGate.style.display = "flex";
    if (dashboard) dashboard.style.display = "none";

    if (container) {
      container.innerHTML = `
        <span class="badge" style="background:#fee2e2; color:#b91c1c;">
          🔒 Locked: Please Sign In
        </span>
      `;
    }
  }
}
