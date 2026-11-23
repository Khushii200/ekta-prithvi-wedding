import { useEffect, useRef, useState } from 'react'
import { animate, useInView, useReducedMotion } from 'framer-motion'
import { WEDDING, formatDate } from '../data/events.js'
import { art } from '../lib/assets.js'
import Reveal from './Reveal.jsx'
import { Sparkles } from './Motion.jsx'

const TARGET = new Date(WEDDING.countdownTarget).getTime()
const START = formatDate(WEDDING.countdownTarget.slice(0, 10))
const DRIFT = Array.from({ length: 9 }, (_, i) => ({
  src: `petal-${(i % 3) + 1}`,
  left: `${6 + ((i * 37) % 90)}%`,
  size: 13 + ((i * 7) % 12),
  duration: `${11 + ((i * 5) % 8)}s`,
  delay: `${-((i * 3.1) % 14)}s`,
  drift: `${(i % 2 ? 1 : -1) * (24 + ((i * 13) % 40))}px`,
}))

function remaining(now) {
  const ms = TARGET - now
  if (ms <= 0) return null
  const s = Math.floor(ms / 1000)
  return { Days: Math.floor(s / 86400), Hours: Math.floor(s / 3600) % 24, Minutes: Math.floor(s / 60) % 60, Seconds: s % 60 }
}

function Unit({ label, value, roll }) {
  const shown = roll < 1 ? Math.round(value * roll) : value
  const text = String(shown).padStart(2, '0')
  return (
    <div className="count__unit">
      <div className="count__num" aria-hidden="true">
        <span key={roll < 1 ? 'rolling' : text}>{text}</span>
      </div>
      <span className="count__label">{label}</span>
    </div>
  )
}

export default function Countdown() {
  const [left, setLeft] = useState(() => remaining(Date.now()))
  const reduced = useReducedMotion()
  const [roll, setRoll] = useState(0)
  const rowRef = useRef(null)
  const inView = useInView(rowRef, { once: true, margin: '-12% 0px' })

  useEffect(() => {
    const id = setInterval(() => setLeft(remaining(Date.now())), 1000)
    return () => clearInterval(id)
  }, [])

  // The numbers race up to the real time the first time they are seen.
  useEffect(() => {
    if (!inView) return
    if (reduced) {
      setRoll(1)
      return
    }
    const controls = animate(0, 1, { duration: 1.9, ease: [0.16, 0.8, 0.24, 1], onUpdate: setRoll })
    return () => controls.stop()
  }, [inView, reduced])

  return (
    <section id="countdown" className="count" aria-label="Countdown to the wedding celebrations">
      <Sparkles count={22} seed={7} />
      <span className="drift" aria-hidden="true">
        {DRIFT.map((p, i) => (
          <img key={i} src={art(p.src)} alt="" loading="lazy" style={{ left: p.left, width: p.size, height: p.size, animationDuration: p.duration, animationDelay: p.delay, '--drift': p.drift }} />
        ))}
      </span>
      {left ? (
        <>
          <Reveal as="p" className="eyebrow">Counting down</Reveal>
          <div ref={rowRef} className="count__row" role="timer" aria-label={`${left.Days} days, ${left.Hours} hours and ${left.Minutes} minutes until the celebrations`}>
            {Object.entries(left).map(([k, v]) => (
              <Unit key={k} label={k} value={v} roll={roll} />
            ))}
          </div>
          <Reveal as="p" className="count__note" delay={0.3}>
            until {START.day} {START.month} {START.year}, India time
          </Reveal>
        </>
      ) : (
        <p ref={rowRef} className="count__done">The celebrations have begun!</p>
      )}
    </section>
  )
}
