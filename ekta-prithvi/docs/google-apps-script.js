// Paste into Extensions > Apps Script in your Google Sheet. See docs/CONNECT-RSVP.md.
const HEADERS = ['Received', 'Guest name', 'Phone', 'Guests', 'Events', 'Dietary preferences', 'Message']

function doPost(e) {
  try {
    const d = JSON.parse(e.postData.contents)
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0]
    if (sheet.getLastRow() === 0) sheet.appendRow(HEADERS)
    sheet.appendRow([new Date(), d.name, d.phone, d.guests, (d.events || []).join(', '), d.dietary, d.message])
    return json({ ok: true })
  } catch (err) {
    return json({ ok: false, error: String(err) })
  }
}

function json(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON)
}
