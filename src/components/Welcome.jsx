import { useRef } from 'react'
import { motion, useReducedMotion, useScroll, useTransform } from 'framer-motion'
import { WELCOME_PHOTO, hasPhoto } from '../data/photos.js'
import PhotoSlot from './PhotoSlot.jsx'
import Reveal from './Reveal.jsx'

const LETTER = 'With the blessings of our families, we invite you to join us as we celebrate the beginning of a beautiful new chapter.'
const WORDS = LETTER.split(' ')

function Word({ word, index, progress }) {
  const start = index / WORDS.length
  const opacity = useTransform(progress, [start, start + 2.5 / WORDS.length], [0.14, 1])
  return <motion.span style={{ opacity }}>{word} </motion.span>
}

export default function Welcome() {
  const withPhoto = hasPhoto(WELCOME_PHOTO)
  const ref = useRef(null)
  const reduced = useReducedMotion()
  // The sentence inks itself in as the guest scrolls.
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start 82%', 'end 52%'] })
  return (
    <section id="welcome" className={`welcome ${withPhoto ? 'welcome--photo' : ''}`}>
      {withPhoto && (
        <Reveal className="welcome__photo">
          <PhotoSlot item={WELCOME_PHOTO} />
        </Reveal>
      )}
      <div className="welcome__text">
        <Reveal as="h2" className="eyebrow eyebrow--gold">A Celebration of Love</Reveal>
        <p ref={ref} className="welcome__letter" aria-label={LETTER}>
          {reduced ? LETTER : WORDS.map((w, i) => <Word key={i} word={w} index={i} progress={scrollYProgress} />)}
        </p>
        <Reveal as="p" className="welcome__after">Your presence will make these moments even more special.</Reveal>
      </div>
    </section>
  )
}
