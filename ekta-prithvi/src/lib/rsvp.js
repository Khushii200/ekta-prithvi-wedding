// Sends an RSVP to the address in VITE_RSVP_ENDPOINT (see docs/CONNECT-RSVP.md).
// With no address set, nothing is stored and the page tells the guest so.
const ENDPOINT = import.meta.env.VITE_RSVP_ENDPOINT

export const isRsvpConnected = Boolean(ENDPOINT)

export async function submitRsvp(data) {
  if (!ENDPOINT) return { stored: false }

  // text/plain avoids a CORS preflight, which Google Apps Script cannot answer.
  const res = await fetch(ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
    body: JSON.stringify({ ...data, submittedAt: new Date().toISOString() }),
  })
  if (!res.ok) throw new Error(`RSVP endpoint returned ${res.status}`)
  const body = await res.json().catch(() => ({}))
  if (body.ok === false) throw new Error(body.error || 'RSVP endpoint rejected the reply')
  return { stored: true }
}

export function validateRsvp(v) {
  const errors = {}
  if (!v.name.trim()) errors.name = 'Enter your name.'
  const count = Number(v.guests)
  if (!Number.isInteger(count) || count < 1 || count > 20) errors.guests = 'Enter a number of guests from 1 to 20.'
  if (v.phone.trim() && !/^\+?[\d\s()-]{7,20}$/.test(v.phone.trim())) errors.phone = 'Enter a phone number using digits only, or leave this empty.'
  if (v.events.length === 0) errors.events = 'Choose at least one celebration.'
  return errors
}
