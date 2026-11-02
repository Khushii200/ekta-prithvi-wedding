import { useRef } from 'react'
import { motion, useReducedMotion, useScroll } from 'framer-motion'
import { EVENTS } from '../data/events.js'
import EventCard from './EventCard.jsx'
import Reveal from './Reveal.jsx'

const PATH = 'M20 0 C 34 90, 6 170, 20 260 S 36 430, 18 520 S 4 690, 22 780 S 34 930, 20 1000'

export default function WeddingEvents() {
  const ref = useRef(null)
  const reduced = useReducedMotion()
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start 72%', 'end 72%'] })

  return (
    <section id="celebrations" className="events">
      <Reveal className="section-head">
        <h2 className="h2">The Wedding Celebrations</h2>
        <p className="prose">Six occasions across five days.</p>
      </Reveal>
      <div className="events__list" ref={ref}>
        {/* A thread that draws itself down the page as the guest scrolls */}
        <svg className="events__thread" viewBox="0 0 40 1000" preserveAspectRatio="none" aria-hidden="true">
          <path d={PATH} className="thread thread--ghost" />
          <motion.path d={PATH} className="thread" style={{ pathLength: reduced ? 1 : scrollYProgress }} />
        </svg>
        {EVENTS.map((e, i) => (
          <EventCard key={e.id} event={e} flip={i % 2 === 1} />
        ))}
      </div>
    </section>
  )
}
