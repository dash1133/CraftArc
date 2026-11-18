/* CraftArc landing page: lead form, attribution and lead scoring. No dependencies. */
(function () {
  "use strict";

  var CFG = window.CRAFTARC_CONFIG || {};
  var ATTR_KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "li_fat_id"];
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  /* ---------- attribution: first touch is kept for the session ---------- */
  function readAttribution() {
    var params = new URLSearchParams(window.location.search);
    var current = {};
    ATTR_KEYS.forEach(function (k) {
      var v = params.get(k);
      if (v) current[k] = v.slice(0, 200);
    });
    var stored = null;
    try {
      stored = JSON.parse(window.sessionStorage.getItem("craftarc_attr") || "null");
    } catch (e) {
      stored = null;
    }
    if (!stored) {
      stored = current;
      stored.referrer = document.referrer || "";
      stored.landing_page = window.location.pathname + window.location.search;
      try {
        window.sessionStorage.setItem("craftarc_attr", JSON.stringify(stored));
      } catch (e) {
        /* storage blocked: attribution still works for this page view */
      }
    }
    return stored;
  }

  /* ---------- lead scoring: fit with the CraftArc buyer ---------- */
  function scoreLead(d) {
    var score = 0;
    var role = { coo: 30, managing_partner: 30, partner_md: 20, talent_hr: 10, other: 0 };
    var aum = { lt1b: 5, "1to2b": 15, "2to5b": 25, "5to10b": 25, gt10b: 15 };
    var timing = { q1_2027: 20, q2_2027: 12, later: 4, unsure: 6 };
    var framework = { yes: 15, draft: 10, no: 4 };
    var team = { lt10: 2, "10to25": 10, "26to50": 10, gt50: 8 };
    score += role[d.role] || 0;
    score += aum[d.aum] || 0;
    score += timing[d.timing] || 0;
    score += framework[d.framework] || 0;
    score += team[d.team] || 0;
    if (d.email_type === "personal") score -= 10;
    score = Math.max(0, Math.min(100, score));
    var priority = score >= 70 ? "hot" : score >= 45 ? "warm" : "nurture";
    return { fit_score: score, priority: priority };
  }

  function emailType(email) {
    var domain = (email.split("@")[1] || "").toLowerCase();
    var list = CFG.personalEmailDomains || [];
    return list.indexOf(domain) >= 0 ? "personal" : "work";
  }

  /* ---------- form ---------- */
  var form = document.getElementById("lead-form");
  if (!form) return;
  var statusEl = document.getElementById("form-status");
  var submitBtn = document.getElementById("submit");
  var thanks = document.getElementById("thanks");
  var sending = false;
  var attribution = readAttribution();

  var RULES = {
    name: function (v) { return v.trim().length >= 2 ? "" : "Please enter your full name."; },
    email: function (v) { return EMAIL_RE.test(v.trim()) ? "" : "Please enter a valid email address."; },
    firm: function (v) { return v.trim().length >= 2 ? "" : "Please enter your firm's name."; },
    role: function (v) { return v ? "" : "Please choose your role."; },
    consent: function (_v, el) { return el.checked ? "" : "Please agree so we can reply to you."; }
  };

  function setError(id, msg) {
    var el = form.elements[id];
    var err = document.getElementById(id + "-err");
    if (!el || !err) return;
    if (msg) {
      err.textContent = msg;
      err.hidden = false;
      el.setAttribute("aria-invalid", "true");
      el.setAttribute("aria-describedby", id + "-err");
    } else {
      err.textContent = "";
      err.hidden = true;
      el.removeAttribute("aria-invalid");
      el.removeAttribute("aria-describedby");
    }
  }

  function validate() {
    var firstBad = null;
    Object.keys(RULES).forEach(function (id) {
      var el = form.elements[id];
      var msg = RULES[id](el.value || "", el);
      setError(id, msg);
      if (msg && !firstBad) firstBad = el;
    });
    return firstBad;
  }

  Object.keys(RULES).forEach(function (id) {
    var el = form.elements[id];
    el.addEventListener("blur", function () {
      if (el.getAttribute("aria-invalid") === "true") setError(id, RULES[id](el.value || "", el));
    });
    el.addEventListener("change", function () {
      if (el.getAttribute("aria-invalid") === "true") setError(id, RULES[id](el.value || "", el));
    });
  });

  function collect() {
    var f = form.elements;
    var data = {
      name: f.name.value.trim(),
      email: f.email.value.trim(),
      firm: f.firm.value.trim(),
      role: f.role.value,
      aum: f.aum.value,
      team: f.team.value,
      timing: f.timing.value,
      framework: f.framework.value,
      message: f.message.value.trim(),
      consent: f.consent.checked
    };
    data.email_type = emailType(data.email);
    var s = scoreLead(data);
    data.fit_score = s.fit_score;
    data.priority = s.priority;
    data.source = "craftarc-website";
    data.page = window.location.href.split("#")[0];
    data.submitted_at = new Date().toISOString();
    Object.keys(attribution).forEach(function (k) { data[k] = attribution[k]; });
    return data;
  }

  function showThanks(data) {
    form.hidden = true;
    thanks.hidden = false;
    thanks.focus();
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: "lead_submitted", lead_priority: data ? data.priority : "unknown" });
  }

  function mailtoHref(data) {
    var lines = [
      "Name: " + data.name, "Email: " + data.email, "Firm: " + data.firm, "Role: " + data.role,
      "AUM: " + (data.aum || "not given"), "Senior deal team: " + (data.team || "not given"),
      "Next cycle: " + (data.timing || "not given"), "Framework: " + (data.framework || "not given"),
      "", data.message
    ];
    return "mailto:" + encodeURIComponent(CFG.leadEmail) +
      "?subject=" + encodeURIComponent("CraftArc demo request: " + data.firm) +
      "&body=" + encodeURIComponent(lines.join("\n"));
  }

  function setStatus(msg, isError) {
    statusEl.textContent = msg;
    statusEl.classList.toggle("is-error", !!isError);
  }

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    if (sending) return;
    setStatus("", false);

    // Honeypot: bots fill hidden fields. Pretend success, send nothing.
    if (form.elements.company_website.value) {
      showThanks(null);
      return;
    }

    var bad = validate();
    if (bad) {
      bad.focus();
      setStatus("Please check the highlighted fields.", true);
      return;
    }

    var data = collect();

    if (!CFG.leadEndpoint) {
      if (CFG.leadEmail) {
        (window.__craftarcNavigate || function (href) { window.location.href = href; })(mailtoHref(data));
        var head = document.querySelector("#thanks h3");
        if (head) head.textContent = "One more step: press send in your email app.";
        var msg = document.getElementById("thanks-msg");
        if (msg) msg.textContent = "Your email app should open with your request filled in. " +
          "If it did not open, email " + CFG.leadEmail + " and we will arrange a time.";
        showThanks(data);
      } else {
        setStatus("Sorry, the form is not connected yet. Please email us instead.", true);
        if (window.console) console.error("CraftArc: set leadEndpoint or leadEmail in config.js");
      }
      return;
    }

    sending = true;
    submitBtn.disabled = true;
    submitBtn.textContent = "Sending...";
    fetch(CFG.leadEndpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(data)
    })
      .then(function (res) {
        if (!res.ok) throw new Error("HTTP " + res.status);
        showThanks(data);
      })
      .catch(function () {
        var fallback = CFG.leadEmail ? " You can also email us at " + CFG.leadEmail + "." : "";
        setStatus("Sorry, something went wrong and your request was not sent. Please try again." + fallback, true);
      })
      .then(function () {
        sending = false;
        submitBtn.disabled = false;
        submitBtn.textContent = "Request my demo";
      });
  });

  /* ---------- offer lines waiting for approval: hidden unless config says so ---------- */
  // Offer lines Dash has approved since launch (config.js: extraOfferItems). Plain text only.
  var stack = document.getElementById("offer-stack");
  (CFG.extraOfferItems || []).forEach(function (text) {
    if (!stack || typeof text !== "string" || !text.trim()) return;
    var li = document.createElement("li");
    li.textContent = text.trim();
    stack.appendChild(li);
  });

  /* ---------- CTA clicks, for analytics ---------- */
  document.querySelectorAll("[data-cta]").forEach(function (a) {
    a.addEventListener("click", function () {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ event: "cta_click", cta: a.getAttribute("data-cta") });
    });
  });

  // Exposed for tests.
  window.__craftarc = { scoreLead: scoreLead, emailType: emailType };
})();

/* ---------- screenshot viewer: open the full screen in a dialog ---------- */
(function () {
  "use strict";
  var dlg = document.getElementById("viewer");
  if (!dlg || typeof dlg.showModal !== "function") return;
  var img = dlg.querySelector("img");
  var cap = dlg.querySelector("p");
  document.querySelectorAll("[data-full]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      img.src = btn.getAttribute("data-full");
      img.alt = btn.getAttribute("data-alt") || "";
      cap.textContent = btn.getAttribute("data-alt") || "";
      dlg.showModal();
    });
  });
  dlg.addEventListener("click", function (e) {
    if (e.target === dlg || e.target.hasAttribute("data-close")) dlg.close();
  });
})();
