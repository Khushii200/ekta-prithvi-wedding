import { MapPin } from 'lucide-react'
import { EVENTS, VENUES } from '../data/events.js'
import Reveal from './Reveal.jsx'
import { Item, Letters, Stagger } from './Motion.jsx'

export default function Venue() {
  const club = VENUES.theClub
  const atClub = EVENTS.filter((e) => e.venue === club)
  const pending = EVENTS.filter((e) => !e.venue)
  return (
    <section id="venue" className="venue">
      <div className="venue__main">
        <Reveal as="p" className="eyebrow eyebrow--gold">The Venue</Reveal>
        <h2 className="venue__name" aria-label={club.name}>
          <Letters text={club.name} inView step={0.05} />
        </h2>
        <Reveal as="p" className="venue__loc" delay={0.35}>{club.location}</Reveal>
        <Reveal delay={0.5}>
          <a className="btn" href={club.mapsUrl} target="_blank" rel="noopener noreferrer">
            <MapPin size={15} strokeWidth={1.3} aria-hidden="true" /> Get directions
          </a>
        </Reveal>
      </div>
      <Stagger as="ul" className="venue__list">
        {atClub.map((e) => (
          <Item as="li" key={e.id}>
            <strong>{e.name}</strong>
            <span>{e.time}</span>
          </Item>
        ))}
        {pending.map((e) => (
          <Item as="li" key={e.id}>
            <strong>{e.name}</strong>
            <span className="is-tba">Venue details coming soon</span>
          </Item>
        ))}
      </Stagger>
    </section>
  )
}
