import { WELCOME_PHOTO, hasPhoto } from '../data/photos.js'
import PhotoSlot from './PhotoSlot.jsx'
import Reveal from './Reveal.jsx'

export default function Welcome() {
  const withPhoto = hasPhoto(WELCOME_PHOTO)
  return (
    <section id="welcome" className={`welcome ${withPhoto ? 'welcome--photo' : ''}`}>
      {withPhoto && (
        <Reveal className="welcome__photo">
          <PhotoSlot item={WELCOME_PHOTO} />
        </Reveal>
      )}
      <Reveal className="welcome__text">
        <h2 className="eyebrow eyebrow--gold">A Celebration of Love</h2>
        <p className="welcome__letter">
          With the blessings of our families, we invite you to join us as we celebrate the beginning of a beautiful new
          chapter.
        </p>
        <p className="welcome__after">Your presence will make these moments even more special.</p>
      </Reveal>
    </section>
  )
}
