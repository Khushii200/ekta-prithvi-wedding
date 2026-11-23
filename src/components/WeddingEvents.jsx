import { MapPin } from 'lucide-react'
import { EVENTS, eventsSummary, formatDate } from '../data/events.js'
import { artSet } from '../lib/assets.js'
import Reveal from './Reveal.jsx'
import { scrollToId } from './Navigation.jsx'

const TBA = 'Details to be announced'

// Each single-event day gets its own treatment, so the programme never repeats one template.
const TREATMENT = { mehendi: 'arch', vrat: 'quiet', cocktail: 'night' }

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

function Directions({ venue }) {
  return (
    <a className="text-link" href={venue.mapsUrl} target="_blank" rel="noopener noreferrer">
      <MapPin size={14} strokeWidth={1.3} aria-hidden="true" /> Directions
    </a>
  )
}

function Leaf({ event }) {
  const d = formatDate(event.date)
  return (
    <Reveal as="article" id={`day-${event.date}`} className={`leaf leaf--${TREATMENT[event.id] ?? 'arch'}`}>
      <div className="leaf__art">
        <img {...artSet(event.art, 360, 680)} sizes="(min-width: 900px) 420px, 68vw" alt={event.artAlt} width="680" height="680" loading="lazy" decoding="async" />
      </div>
      <div className="leaf__text">
        <p className="leaf__date">
          <span className="numeral">{d.day}</span>
          <span>
            {d.month} {d.year}
            <br />
            {d.weekday}
          </span>
        </p>
        <h3 className="leaf__name">{event.name}</h3>
        <p className="leaf__label">{event.label}</p>
        <dl className="facts">
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
        </dl>
      </div>
    </Reveal>
  )
}

function WeddingDay({ events }) {
  const d = formatDate(events[0].date)
  const titleId = `chapter-${events[0].date}`
  const shared = events.every((e) => e.venue === events[0].venue) ? events[0].venue : null
  return (
    <section id={`day-${events[0].date}`} className="wedding-day" aria-labelledby={titleId}>
      <Reveal className="wedding-day__head">
        <p className="eyebrow">{d.weekday}</p>
        <h3 className="wedding-day__title" id={titleId}>
          <span className="numeral">{d.day}</span>
          <span className="wedding-day__month">{d.month}</span>
        </h3>
        <p className="wedding-day__name">The Wedding Day</p>
      </Reveal>
      <ol className="rites">
        {events.map((e, i) => (
          <Reveal as="li" key={e.id} className={`rite ${i === 1 ? 'rite--heart' : ''}`} delay={i * 0.08}>
            <div className="rite__art">
              <img {...artSet(e.art, 360, 680)} sizes="(min-width: 900px) 320px, 150px" alt={e.artAlt} width="680" height="680" loading="lazy" decoding="async" />
            </div>
            <div className="rite__text">
              <p className={`rite__time ${e.time ? '' : 'is-tba'}`}>{e.time ?? TBA}</p>
              <h4 className="rite__name">{e.name}</h4>
              <p className="rite__label">{e.label}</p>
              {!shared && <p className="rite__venue">{e.venue ? venueText(e.venue) : TBA}</p>}
            </div>
          </Reveal>
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

      <nav className="day-nav" aria-label="Jump to a day">
        {days.map((day) => {
          const d = formatDate(day[0].date)
          const id = `day-${day[0].date}`
          return (
            <a
              key={id}
              href={`#${id}`}
              onClick={(e) => {
                e.preventDefault()
                scrollToId(id)
              }}
            >
              <span className="numeral">{d.day}</span>
              <small>{day.length > 1 ? 'Wedding Day' : day[0].name}</small>
            </a>
          )
        })}
      </nav>

      <div className="programme">
        {days.map((day) => (day.length > 1 ? <WeddingDay key={day[0].date} events={day} /> : <Leaf key={day[0].id} event={day[0]} />))}
      </div>
    </section>
  )
}
