import { MapPin } from 'lucide-react'
import { EVENTS, VENUES } from '../data/events.js'
import Reveal from './Reveal.jsx'

export default function Venue() {
  const club = VENUES.theClub
  const atClub = EVENTS.filter((e) => e.venue === club)
  const pending = EVENTS.filter((e) => !e.venue)
  return (
    <section id="venue" className="venue">
      <Reveal className="venue__main">
        <p className="eyebrow eyebrow--gold">The Venue</p>
        <h2 className="venue__name">{club.name}</h2>
        <p className="venue__loc">{club.location}</p>
        <a className="btn" href={club.mapsUrl} target="_blank" rel="noopener noreferrer">
          <MapPin size={15} strokeWidth={1.3} aria-hidden="true" /> Get directions
        </a>
      </Reveal>
      <Reveal className="venue__list" delay={0.1}>
        <ul>
          {atClub.map((e) => (
            <li key={e.id}>
              <strong>{e.name}</strong>
              <span>{e.time}</span>
            </li>
          ))}
          {pending.map((e) => (
            <li key={e.id}>
              <strong>{e.name}</strong>
              <span className="is-tba">Venue details coming soon</span>
            </li>
          ))}
        </ul>
      </Reveal>
    </section>
  )
}
