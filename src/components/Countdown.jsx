import { useEffect, useState } from 'react'
import { WEDDING, formatDate } from '../data/events.js'

const TARGET = new Date(WEDDING.countdownTarget).getTime()
const START = formatDate(WEDDING.countdownTarget.slice(0, 10))

function remaining(now) {
  const ms = TARGET - now
  if (ms <= 0) return null
  const s = Math.floor(ms / 1000)
  return { Days: Math.floor(s / 86400), Hours: Math.floor(s / 3600) % 24, Minutes: Math.floor(s / 60) % 60, Seconds: s % 60 }
}

function Unit({ label, value }) {
  const text = String(value).padStart(2, '0')
  return (
    <div className="count__unit">
      <div className="count__num" aria-hidden="true">
        <span key={text}>{text}</span>
      </div>
      <span className="count__label">{label}</span>
    </div>
  )
}

export default function Countdown() {
  const [left, setLeft] = useState(() => remaining(Date.now()))

  useEffect(() => {
    const id = setInterval(() => setLeft(remaining(Date.now())), 1000)
    return () => clearInterval(id)
  }, [])

  return (
    <section id="countdown" className="count" aria-label="Countdown to the wedding celebrations">
      {left ? (
        <>
          <p className="eyebrow">Counting down</p>
          <div className="count__row" role="timer" aria-label={`${left.Days} days, ${left.Hours} hours and ${left.Minutes} minutes until the celebrations`}>
            {Object.entries(left).map(([k, v]) => (
              <Unit key={k} label={k} value={v} />
            ))}
          </div>
          <p className="count__note">
            until {START.day} {START.month} {START.year}, India time
          </p>
        </>
      ) : (
        <p className="count__done">The celebrations have begun!</p>
      )}
    </section>
  )
}
