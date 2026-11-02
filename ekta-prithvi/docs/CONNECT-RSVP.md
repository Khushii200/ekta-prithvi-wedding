# Connect the RSVP form to Google Sheets

Until this is done, the form validates and thanks the guest, and tells them plainly that the reply was not saved.

1. Create a Google Sheet for replies.
2. In the sheet, open **Extensions > Apps Script**, delete what is there and paste in `docs/google-apps-script.js`. Save.
3. Click **Deploy > New deployment**, choose type **Web app**, set *Execute as* to **Me** and *Who has access* to **Anyone**. Deploy and allow access.
4. Copy the web app URL (ending in `/exec`).
5. Locally: copy `.env.example` to `.env` and set `VITE_RSVP_ENDPOINT=<that URL>`. On Vercel: add the same variable under **Settings > Environment Variables**, then redeploy.
6. Send a test reply and check that a row appears.

To use another backend, set `VITE_RSVP_ENDPOINT` to any URL that accepts a POST with a JSON body and returns `{ "ok": true }`. The code is in `src/lib/rsvp.js`.
