import { useEffect, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { WEDDING } from '../data/events.js'

const TARGET = new Date(WEDDING.countdownTarget).getTime()

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
        <AnimatePresence mode="popLayout" initial={false}>
          <motion.span
            key={text}
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            transition={{ duration: 0.4, ease: 'easeOut' }}
          >
            {text}
          </motion.span>
        </AnimatePresence>
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
          <div className="count__row" role="timer" aria-label={`${left.Days} days, ${left.Hours} hours and ${left.Minutes} minutes until the celebrations`}>
            {Object.entries(left).map(([k, v]) => (
              <Unit key={k} label={k} value={v} />
            ))}
          </div>
          <p className="count__note">until 26 December 2026, India time</p>
        </>
      ) : (
        <p className="count__done">THE CELEBRATIONS HAVE BEGUN!</p>
      )}
    </section>
  )
}
