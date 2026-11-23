import { useRef } from 'react'
import { motion, useReducedMotion, useScroll, useTransform } from 'framer-motion'
import { MapPin } from 'lucide-react'
import { EVENTS, eventsSummary, formatDate } from '../data/events.js'
import { artSet } from '../lib/assets.js'
import Reveal from './Reveal.jsx'
import { scrollToId } from './Navigation.jsx'
import { Item, Letters, Sparkles, Stagger } from './Motion.jsx'

const TBA = 'Details to be announced'

// Each single-event day gets its own treatment, so the programme never repeats one template.
const TREATMENT = { mehendi: 'arch', vrat: 'quiet', cocktail: 'night' }
// Each painting keeps a small movement of its own.
const IDLE = { mehendi: 'spin', 'jaan-swagat': 'sway', 'hasta-melap': 'breathe', reception: 'float', vrat: 'float', cocktail: 'clink' }

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

const venueText = (v) => `${v.name}, ${v.location.split(',')[0]}`
const BLOOM = { type: 'spring', stiffness: 60, damping: 13 }

function Directions({ venue }) {
  return (
    <a className="text-link" href={venue.mapsUrl} target="_blank" rel="noopener noreferrer">
      <MapPin size={14} strokeWidth={1.3} aria-hidden="true" /> Directions
    </a>
  )
}

function Leaf({ event }) {
  const d = formatDate(event.date)
  const ref = useRef(null)
  const reduced = useReducedMotion()
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start end', 'end start'] })
  const ghostY = useTransform(scrollYProgress, [0, 1], [70, -70])
  const kind = TREATMENT[event.id] ?? 'arch'
  return (
    <article ref={ref} id={`day-${event.date}`} className={`leaf leaf--${kind}`}>
      <motion.span className="leaf__ghost numeral" aria-hidden="true" style={reduced ? undefined : { y: ghostY }}>
        {d.day}
      </motion.span>
      {kind === 'night' && <Sparkles count={16} seed={5} />}
      <motion.div
        className="leaf__art"
        initial={{ opacity: 0, scale: 0.72, rotate: -10 }}
        whileInView={{ opacity: 1, scale: 1, rotate: 0 }}
        viewport={{ once: true, margin: '-12% 0px' }}
        transition={BLOOM}
      >
        <img className={`idle idle--${IDLE[event.id]}`} {...artSet(event.art, 360, 680)} sizes="(min-width: 900px) 420px, 68vw" alt={event.artAlt} width="680" height="680" loading="lazy" decoding="async" />
      </motion.div>
      <Stagger className="leaf__text">
        <Item as="p" className="leaf__date">
          <span className="numeral">{d.day}</span>
          <span>
            {d.month} {d.year}
            <br />
            {d.weekday}
          </span>
        </Item>
        <Item as="h3" className="leaf__name">{event.name}</Item>
        <Item as="p" className="leaf__label">{event.label}</Item>
        <Item as="dl" className="facts">
          <div>
            <dt>Time</dt>
            <dd className={event.time ? '' : 'is-tba'}>{event.time ?? TBA}</dd>
          </div>
          <div>
            <dt>Venue</dt>
            <dd className={event.venue ? '' : 'is-tba'}>
              {event.venue ? venueText(event.venue) : TBA}
              {event.venue && <Directions venue={event.venue} />}
            </dd>
          </div>
        </Item>
      </Stagger>
    </article>
  )
}

function WeddingDay({ events }) {
  const d = formatDate(events[0].date)
  const titleId = `chapter-${events[0].date}`
  const shared = events.every((e) => e.venue === events[0].venue) ? events[0].venue : null
  const ref = useRef(null)
  const reduced = useReducedMotion()
  // The champagne band opens out to the full width of the page.
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start 100%', 'start 42%'] })
  const bandX = useTransform(scrollYProgress, [0, 1], [0.84, 1])
  return (
    <section ref={ref} id={`day-${events[0].date}`} className="wedding-day" aria-labelledby={titleId}>
      <motion.span className="wedding-day__band" aria-hidden="true" style={reduced ? undefined : { scaleX: bandX }} />
      <Sparkles count={10} seed={3} />
      <Reveal className="wedding-day__head">
        <p className="eyebrow">{d.weekday}</p>
        <h3 className="wedding-day__title" id={titleId} aria-label={`${d.day} ${d.month}`}>
          <span className="numeral"><Letters text={d.day} inView step={0.12} /></span>
          <span className="wedding-day__month"><Letters text={d.month} inView delay={0.25} step={0.035} /></span>
        </h3>
        <p className="wedding-day__name">The Wedding Day</p>
      </Reveal>
      <ol className="rites">
        {events.map((e, i) => (
          <motion.li
            key={e.id}
            className={`rite ${i === 1 ? 'rite--heart' : ''}`}
            initial={{ opacity: 0, x: i % 2 ? 34 : -34 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: '-10% 0px' }}
            transition={{ duration: 0.9, delay: i * 0.1, ease: [0.22, 0.7, 0.3, 1] }}
          >
            <motion.div
              className="rite__art"
              initial={{ scale: 0.6, rotate: i % 2 ? 9 : -9 }}
              whileInView={{ scale: 1, rotate: 0 }}
              viewport={{ once: true, margin: '-10% 0px' }}
              transition={{ ...BLOOM, delay: 0.1 + i * 0.1 }}
            >
              <img className={`idle idle--${IDLE[e.id]}`} {...artSet(e.art, 360, 680)} sizes="(min-width: 900px) 320px, 150px" alt={e.artAlt} width="680" height="680" loading="lazy" decoding="async" />
            </motion.div>
            <div className="rite__text">
              <p className={`rite__time ${e.time ? '' : 'is-tba'}`}>{e.time ?? TBA}</p>
              <h4 className="rite__name">{e.name}</h4>
              <p className="rite__label">{e.label}</p>
              {!shared && <p className="rite__venue">{e.venue ? venueText(e.venue) : TBA}</p>}
            </div>
          </motion.li>
        ))}
      </ol>
      {shared && (
        <Reveal className="wedding-day__venue">
          <span>{venueText(shared)}</span>
          <Directions venue={shared} />
        </Reveal>
      )}
    </section>
  )
}

export default function WeddingEvents() {
  const days = byDay(EVENTS)
  return (
    <section id="celebrations" className="events">
      <Reveal className="section-head">
        <p className="eyebrow eyebrow--gold">The Programme</p>
        <h2 className="h2">The Wedding Celebrations</h2>
        <p className="section-note">{eventsSummary()}</p>
      </Reveal>

      <Stagger as="nav" className="day-nav" aria-label="Jump to a day">
        {days.map((day) => {
          const d = formatDate(day[0].date)
          const id = `day-${day[0].date}`
          return (
            <Item
              as="a"
              key={id}
              href={`#${id}`}
              onClick={(e) => {
                e.preventDefault()
                scrollToId(id)
              }}
            >
              <span className="numeral">{d.day}</span>
              <small>{day.length > 1 ? 'Wedding Day' : day[0].name}</small>
            </Item>
          )
        })}
      </Stagger>

      <div className="programme">
        {days.map((day) => (day.length > 1 ? <WeddingDay key={day[0].date} events={day} /> : <Leaf key={day[0].id} event={day[0]} />))}
      </div>
    </section>
  )
}
