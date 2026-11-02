import { art } from '../lib/assets.js'
import { WELCOME_PHOTO } from '../data/photos.js'
import PhotoSlot from './PhotoSlot.jsx'
import Reveal from './Reveal.jsx'

export default function Welcome() {
  return (
    <section id="welcome" className="welcome">
      <img className="welcome__vine" src={art('vine')} alt="" loading="lazy" />
      <Reveal className="welcome__photo">
        <div className="welcome__frame">
          <PhotoSlot item={WELCOME_PHOTO} />
        </div>
        <img className="welcome__sprig" src={art('sprig-a')} alt="" loading="lazy" />
      </Reveal>
      <Reveal className="welcome__text" delay={0.15}>
        <h2 className="h2">A Celebration of Love</h2>
        <p className="prose">
          With the blessings of our families, we invite you to join us as we celebrate the beginning of a beautiful new
          chapter. Your presence will make these moments even more special.
        </p>
      </Reveal>
    </section>
  )
}
