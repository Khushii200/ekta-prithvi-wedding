import { motion } from 'framer-motion'
import { art } from '../lib/assets.js'
import { formatDate } from '../data/events.js'

export const TBA = 'Details to be announced'

const WASH = { morning: 'wash-gold', afternoon: 'wash-gold', golden: 'wash-rose', dusk: 'wash-dusk', dawn: 'wash-sage', night: 'wash-dusk' }

export default function EventCard({ event, flip, mood = 'morning', shape = 'plain' }) {
  const d = formatDate(event.date)
  return (
    <motion.article
      className={`event ${flip ? 'event--flip' : ''} mood--${mood} shape--${shape}`}
      initial={{ opacity: 0, y: 26 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '0px 0px -10% 0px' }}
      transition={{ duration: 0.95, ease: [0.22, 0.7, 0.3, 1] }}
    >
      <div className="event__art">
        <img className="event__wash" src={art(WASH[mood])} alt="" aria-hidden="true" loading="lazy" />
        <img src={art(event.art)} alt={event.artAlt} width="680" height="680" loading="lazy" decoding="async" />
      </div>
      <span className="event__knot" aria-hidden="true" />
      <div className="event__card">
        <div className="event__date">
          <span className="event__day">{d.day}</span>
          <span className="event__month">
            {d.month} {d.year}
            <br />
            {d.weekday}
          </span>
        </div>
        <p className="event__label">{event.label}</p>
        <h3 className="event__name">{event.name}</h3>
        <dl className="event__meta">
          <div>
            <dt>Time</dt>
            <dd className={event.time ? '' : 'is-tba'}>{event.time ?? TBA}</dd>
          </div>
          <div>
            <dt>Venue</dt>
            <dd className={event.venue ? '' : 'is-tba'}>
              {event.venue ? `${event.venue.name}, ${event.venue.location.split(',')[0]}` : TBA}
            </dd>
          </div>
        </dl>
      </div>
    </motion.article>
  )
}
