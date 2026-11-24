/*
 * Site settings. Edit these before going live.
 *
 * leadEndpoint  Where the demo form sends leads, as a JSON POST.
 *               Works with Formspree (https://formspree.io/f/<id>), Zapier or
 *               Make webhooks, HubSpot via a webhook, or your own API.
 *               Leave empty to fall back to leadEmail.
 * leadEmail     Fallback: if there is no endpoint, the form opens the
 *               visitor's email app with the request filled in. To receive
 *               leads without the visitor's email app, set leadEndpoint, for
 *               example a Formspree form that forwards to this address.
 * personalEmailDomains  Accepted, but tagged as personal and scored lower.
 */
window.CRAFTARC_CONFIG = {
  leadEndpoint: "",
  leadEmail: "dash@craftarc.ai",
  personalEmailDomains: [
    "gmail.com", "googlemail.com", "yahoo.com", "yahoo.co.uk", "hotmail.com", "hotmail.co.uk",
    "outlook.com", "live.com", "icloud.com", "me.com", "aol.com", "proton.me", "protonmail.com", "gmx.com"
  ]
};
