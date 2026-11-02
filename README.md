# Ekta & Prithvi: wedding invitation website

React, Vite, Framer Motion and Lucide. Needs Node 18 or newer.

## Run it
```
npm install
npm run dev        # http://localhost:5173
npm run build      # production files in dist/
npm run preview    # check the production build
```

## What to edit

| To change | Go to |
|---|---|
| Event dates, times, venues, labels | `src/data/events.js` (`null` shows "Details to be announced") |
| Countdown target and venue details | `src/data/events.js` (`WEDDING`, `VENUES`) |
| Couple photographs | Save in `src/assets/photos/` using the names below |
| Illustrations | Save over a file in `src/assets/illustrations/` with the same base name; webp, png, jpg or svg all work |
| Background music | Replace `src/assets/music/background.mp3` (keep one audio file in the folder). The included track is a synthesised stand-in |
| RSVP to Google Sheets | `docs/CONNECT-RSVP.md` |

### Photo file names
`couple-hero` (hero arch, portrait), `welcome` (4:5 portrait), `closing` (square, shown in a circle), `gallery-1` to `gallery-9`. Any of .jpg .png .webp .avif. A missing file shows the painted placeholder. Gallery labels are in `src/data/photos.js`. Resize to about 1600px on the long side before adding.

## Illustrations
All art was painted in code by `tools/paint/` (`npm run paint`; needs Python with numpy, scipy and Pillow). Running it overwrites `src/assets/illustrations/`.

## Deploy on Vercel
1. Push this folder to a GitHub repository.
2. On vercel.com choose **Add New > Project** and import it. Vercel detects Vite: build `npm run build`, output `dist`.
3. Add `VITE_RSVP_ENDPOINT` under Environment Variables if RSVP is connected.
4. Deploy. Or run `npx vercel` from this folder.
