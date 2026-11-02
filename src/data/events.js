// Edit dates, timings and venues here. The cards, the venue section and the
// RSVP form all read from this file.
//
// time: null  shows "Details to be announced"
// venue: null shows "Details to be announced" on the card and
//             "Venue details coming soon" in the venue section

export const VENUES = {
  theClub: {
    name: 'The Club',
    location: 'Andheri West, Mumbai',
    mapsUrl: 'https://www.google.com/maps/search/?api=1&query=The%20Club%2C%20Andheri%20West%2C%20Mumbai',
  },
}

export const EVENTS = [
  {
    id: 'mehendi',
    name: 'Mehendi',
    date: '2026-12-26',
    time: '10:30 AM onwards',
    venue: null,
    label: 'Henna and flowers',
    art: 'mehendi',
    artAlt: 'Watercolour henna mandala with paisleys and small flowers',
  },
  {
    id: 'jaan-swagat',
    name: 'Jaan Swagat',
    date: '2026-12-28',
    time: '4:00 PM',
    venue: VENUES.theClub,
    label: 'Welcoming the groom',
    art: 'jaan-swagat',
    artAlt: 'Watercolour ceremonial parasol beneath strings of marigolds, with petals scattered on the path',
  },
  {
    id: 'hasta-melap',
    name: 'Hasta Melap',
    date: '2026-12-28',
    time: '5:00 PM',
    venue: VENUES.theClub,
    label: 'Hands joined',
    art: 'hasta-melap',
    artAlt: 'Watercolour mandap with a rose canopy and two linked garlands',
  },
  {
    id: 'reception',
    name: 'Wedding Reception',
    date: '2026-12-28',
    time: '7:30 PM onwards',
    venue: VENUES.theClub,
    label: 'An evening together',
    art: 'reception',
    artAlt: 'Watercolour floral stage arch at dusk with candles on either side',
  },
  {
    id: 'vrat',
    name: 'Vrat',
    date: '2026-12-29',
    time: null,
    venue: null,
    label: 'With devotion',
    art: 'vrat',
    artAlt: 'Watercolour kalash crowned with mango leaves',
  },
  {
    id: 'cocktail',
    name: 'Cocktail',
    date: '2026-12-30',
    time: '8:30 PM onwards',
    venue: null,
    label: 'Raise a glass',
    art: 'cocktail',
    artAlt: 'Two watercolour coupe glasses touching, under small stars, framed by roses',
  },
]

export const WEDDING = {
  // Midnight at the start of 26 December in India (IST is UTC+5:30).
  countdownTarget: '2026-12-26T00:00:00+05:30',
  dateRange: '26 – 30 December 2026',
}

const parts = (iso, opts) =>
  new Intl.DateTimeFormat('en-IN', { timeZone: 'Asia/Kolkata', ...opts }).format(new Date(`${iso}T12:00:00+05:30`))

export const formatDate = (iso) => ({
  day: parts(iso, { day: 'numeric' }),
  month: parts(iso, { month: 'long' }),
  year: parts(iso, { year: 'numeric' }),
  weekday: parts(iso, { weekday: 'long' }),
})
