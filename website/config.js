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
 * extraOfferItems  Extra lines for the "What you get" list, as plain strings.
 *               Leave empty until Dash approves them as public terms. The
 *               candidate wording is in docs/Claims_Ledger.md, flag 4.
 */
window.CRAFTARC_CONFIG = {
  leadEndpoint: "",
  leadEmail: "",
  extraOfferItems: [],
  personalEmailDomains: [
    "gmail.com", "googlemail.com", "yahoo.com", "yahoo.co.uk", "hotmail.com", "hotmail.co.uk",
    "outlook.com", "live.com", "icloud.com", "me.com", "aol.com", "proton.me", "protonmail.com", "gmx.com"
  ]
};
