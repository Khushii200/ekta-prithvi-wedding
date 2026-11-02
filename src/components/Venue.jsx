import { MapPin } from 'lucide-react'
import { art } from '../lib/assets.js'
import { EVENTS, VENUES } from '../data/events.js'
import Reveal from './Reveal.jsx'

export default function Venue() {
  const club = VENUES.theClub
  const atClub = EVENTS.filter((e) => e.venue === club)
  const pending = EVENTS.filter((e) => !e.venue)
  return (
    <section id="venue" className="venue">
      <Reveal className="venue__map">
        <img src={art('map')} alt="Decorative hand-painted map with a rose marking the venue" width="800" height="608" loading="lazy" />
      </Reveal>
      <Reveal className="venue__text" delay={0.12}>
        <h2 className="venue__name">THE CLUB</h2>
        <p className="venue__loc">{club.location}</p>
        <p className="venue__for">{atClub.map((e) => e.name).join(', ').replace(/, ([^,]*)$/, ' and $1')}</p>
        <a className="btn" href={club.mapsUrl} target="_blank" rel="noopener noreferrer">
          <MapPin size={16} strokeWidth={1.4} aria-hidden="true" /> GET DIRECTIONS
        </a>
        <ul className="venue__pending">
          {pending.map((e) => (
            <li key={e.id}>
              <strong>{e.name}</strong>
              <span>Venue details coming soon</span>
            </li>
          ))}
        </ul>
      </Reveal>
    </section>
  )
}
