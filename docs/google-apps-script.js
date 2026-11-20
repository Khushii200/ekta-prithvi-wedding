// Paste into Extensions > Apps Script in your Google Sheet. See docs/CONNECT-RSVP.md.
const HEADERS = ['Received', 'Guest name', 'Phone', 'Guests', 'Events', 'Dietary preferences', 'Message', 'Reply ID']
const ID_COLUMN = HEADERS.length

function doPost(e) {
  const lock = LockService.getScriptLock()
  lock.waitLock(10000)
  try {
    const d = JSON.parse(e.postData.contents)
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0]
    if (sheet.getLastRow() === 0) sheet.appendRow(HEADERS)
    const row = [new Date(), d.name, d.phone, d.guests, (d.events || []).join(', '), d.dietary, d.message, d.replyId].map(safe)

    // A guest who changes their reply sends the same reply ID again: update their row instead of adding one.
    const existing = d.replyId
      ? sheet.getRange(1, ID_COLUMN, sheet.getLastRow()).createTextFinder(String(d.replyId)).matchEntireCell(true).findNext()
      : null
    if (existing) sheet.getRange(existing.getRow(), 1, 1, row.length).setValues([row])
    else sheet.appendRow(row)
    return json({ ok: true })
  } catch (err) {
    return json({ ok: false, error: String(err) })
  } finally {
    lock.releaseLock()
  }
}

// Text starting with = + - or @ would be run as a spreadsheet formula. A leading ' keeps it as plain text.
function safe(value) {
  if (typeof value !== 'string') return value
  return /^[=+\-@]/.test(value) ? "'" + value : value
}

function json(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON)
}
