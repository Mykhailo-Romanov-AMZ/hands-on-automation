// ============================================================
// HandsOn Automation — Interactions
// Motion budget: 1 hero effect (CSS) + 1 scroll effect
// + 1 microinteraction (CTA form). Total <= 3.
//
// Logging stays separate from logic: handlers call the log()
// helper below instead of printing directly.
// ============================================================

// ---------- Logging helper (isolated, not mixed into logic) ----------

function log(label, data) {
  console.debug(`[HandsOnAutomation] ${label}`, data ?? "");
}

log("page loaded", { path: window.location.pathname });

// ---------- Scroll reveal (scroll effect 2/3) ----------

const revealElements = document.querySelectorAll(".reveal");

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        log("section revealed", entry.target.className);
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.15 }
);

revealElements.forEach((el) => observer.observe(el));

// ---------- CTA form microinteraction (3/3) ----------

const form = document.querySelector("#sprint-form");
const formSuccess = document.querySelector("#form-success");
const formError = document.querySelector("#form-error");
const emailInput = form.querySelector("#email");
const submitButton = form.querySelector("button[type='submit']");

// Inline messages for the three ways a signup can fail.
const MESSAGES = {
  invalid: "That email doesn't look right — double-check it and try again.",
  duplicate: "You're already on the list. Your build plan is on its way.",
  offline: "Couldn't join right now. Please try again in a minute.",
};

function showError(message) {
  formError.textContent = message;
  formError.hidden = false;
  log("cta error", { message });
  emailInput.focus();
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  formError.hidden = true;

  const email = emailInput.value.trim();

  // Light client pre-check only — the server is the source of truth.
  if (!email || !email.includes("@")) {
    showError(MESSAGES.invalid);
    return;
  }

  log("cta submitting", { email });

  // Double-submit guard: one POST at a time (decision E in launch-hardening).
  submitButton.disabled = true;

  try {
    const response = await fetch("/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });

    if (response.status === 201) {
      log("cta saved", { email });
      form.hidden = true;
      formSuccess.hidden = false;
      return;
    }

    if (response.status === 409) {
      showError(MESSAGES.duplicate);
      return;
    }

    if (response.status === 429) {
      showError(MESSAGES.offline);
      return;
    }

    showError(MESSAGES.invalid);
  } catch (networkError) {
    log("cta failed", { error: String(networkError) });
    showError(MESSAGES.offline);
  } finally {
    // Re-enable on every outcome; on success the form is hidden anyway.
    submitButton.disabled = false;
  }
});