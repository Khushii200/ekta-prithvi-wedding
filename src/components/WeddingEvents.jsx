import { useRef } from 'react'
import { motion, useReducedMotion, useScroll } from 'framer-motion'
import { EVENTS, formatDate } from '../data/events.js'
import { art } from '../lib/assets.js'
import EventCard, { TBA } from './EventCard.jsx'
import Reveal from './Reveal.jsx'

const PATH = 'M20 0 C 34 90, 6 170, 20 260 S 36 430, 18 520 S 4 690, 22 780 S 34 930, 20 1000'

// The light of each occasion, morning gold through to night, and the shape of its card.
const LOOK = {
  mehendi: { mood: 'morning', shape: 'arch' },
  'jaan-swagat': { mood: 'afternoon' },
  'hasta-melap': { mood: 'golden' },
  reception: { mood: 'dusk' },
  vrat: { mood: 'dawn', shape: 'framed' },
  cocktail: { mood: 'night', shape: 'ticket' },
}

// Consecutive events on the same date become one chapter.
function byDay(events) {
  const days = []
  for (const e of events) {
    const last = days[days.length - 1]
    if (last && last[0].date === e.date) last.push(e)
    else days.push([e])
  }
  return days
}

function DayCard({ event, role }) {
  const look = LOOK[event.id] ?? {}
  return (
    <motion.article
      className={`day-card day-card--${role} mood--${look.mood}`}
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '0px 0px -10% 0px' }}
      transition={{ duration: 0.95, ease: [0.22, 0.7, 0.3, 1], delay: role === 'heart' ? 0.12 : 0 }}
    >
      <div className="day-card__art">
        <img src={art(event.art)} alt={event.artAlt} width="680" height="680" loading="lazy" decoding="async" />
      </div>
      <div className="day-card__body">
        <p className={`day-card__time ${event.time ? '' : 'is-tba'}`}>{event.time ?? TBA}</p>
        <h4 className="day-card__name">{event.name}</h4>
        <p className="day-card__label">{event.label}</p>
        <p className={`day-card__venue ${event.venue ? '' : 'is-tba'}`}>
          {event.venue ? `${event.venue.name}, ${event.venue.location.split(',')[0]}` : TBA}
        </p>
      </div>
    </motion.article>
  )
}

function WeddingDay({ events }) {
  const d = formatDate(events[0].date)
  const roles = events.length === 3 ? ['side', 'heart', 'side'] : events.map(() => 'side')
  return (
    <section className="chapter" aria-labelledby="chapter-title">
      <img className="chapter__wash" src={art('wash-rose')} alt="" aria-hidden="true" loading="lazy" />
      <Reveal className="chapter__head">
        <p className="chapter__kicker">{d.weekday}</p>
        <h3 className="chapter__title" id="chapter-title">
          <span className="chapter__day">{d.day}</span>
          <span className="chapter__month">{d.month}</span>
        </h3>
        <p className="chapter__name">The Wedding Day</p>
        <ol className="chapter__times" aria-label="Order of the day">
          {events.map((e) => (
            <li key={e.id}>
              <span>{e.time ?? 'Time to be announced'}</span> {e.name}
            </li>
          ))}
        </ol>
      </Reveal>
      <div className="chapter__grid">
        {events.map((e, i) => (
          <DayCard key={e.id} event={e} role={roles[i]} />
        ))}
      </div>
    </section>
  )
}

export default function WeddingEvents() {
  const ref = useRef(null)
  const reduced = useReducedMotion()
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start 72%', 'end 72%'] })
  let single = 0

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
        {byDay(EVENTS).map((day) =>
          day.length > 1 ? (
            <WeddingDay key={day[0].date} events={day} />
          ) : (
            <EventCard key={day[0].id} event={day[0]} flip={single++ % 2 === 1} {...LOOK[day[0].id]} />
          ),
        )}
      </div>
    </section>
  )
}
