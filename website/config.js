/*
 * Site settings. Edit these before going live.
 *
 * leadEndpoint  Where the demo form sends leads, as a JSON POST.
 *               Works with Formspree (https://formspree.io/f/<id>), Zapier or
 *               Make webhooks, HubSpot via a webhook, or your own API.
 *               Leave empty to fall back to leadEmail.
 * leadEmail     Fallback: if there is no endpoint, the form opens the
 *               visitor's email app with the request filled in.
 * personalEmailDomains  Accepted, but tagged as personal and scored lower.
 * showPendingOffer  Offer lines marked data-pending in index.html (implementation
 *               consultant in three to four meetings, flat fee fixed for four years,
 *               no build-out fee, limited onboarding). Keep false until Dash approves
 *               them as public terms. See docs/Claims_Ledger.md, flag 4.
 */
window.CRAFTARC_CONFIG = {
  leadEndpoint: "",
  leadEmail: "",
  showPendingOffer: false,
  personalEmailDomains: [
    "gmail.com", "googlemail.com", "yahoo.com", "yahoo.co.uk", "hotmail.com", "hotmail.co.uk",
    "outlook.com", "live.com", "icloud.com", "me.com", "aol.com", "proton.me", "protonmail.com", "gmx.com"
  ]
};
