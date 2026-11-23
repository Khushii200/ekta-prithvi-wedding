import { motion } from 'framer-motion'
import { ChevronDown } from 'lucide-react'
import { artSet } from '../lib/assets.js'
import { HERO_PHOTO, hasPhoto } from '../data/photos.js'
import { WEDDING } from '../data/events.js'
import PhotoSlot from './PhotoSlot.jsx'
import { scrollToId } from './Navigation.jsx'

const EASE = [0.22, 0.7, 0.3, 1]

export default function Hero({ ready }) {
  const withPhoto = hasPhoto(HERO_PHOTO)
  const rise = (i) => ({
    initial: { opacity: 0, y: 16 },
    animate: ready ? { opacity: 1, y: 0 } : { opacity: 0, y: 16 },
    transition: { duration: 1.1, delay: 0.1 + i * 0.13, ease: EASE },
  })

  return (
    <section id="home" className={`hero ${withPhoto ? 'hero--photo' : ''}`}>
      <span className="hero__frame" aria-hidden="true" />
      <motion.img className="hero__spray hero__spray--tl" {...artSet('corner-a', 440, 800)} sizes="(min-width: 900px) 27vw, 44vw" alt="" {...rise(5)} />
      <motion.img className="hero__spray hero__spray--br" {...artSet('corner-b', 440, 800)} sizes="(min-width: 900px) 27vw, 44vw" alt="" {...rise(6)} />

      <div className="hero__inner">
        {withPhoto && (
          <motion.div className="hero__photo" {...rise(1)}>
            <PhotoSlot item={HERO_PHOTO} loading="eager" />
          </motion.div>
        )}
        <div className="hero__copy">
          <motion.p className="eyebrow" {...rise(0)}>
            The wedding celebration of
          </motion.p>
          <h1 className="hero__names">
            <motion.span className="hero__name hero__name--e" {...rise(1)}>Ekta</motion.span>
            <motion.span className="hero__amp" {...rise(2)}>&amp;</motion.span>
            <motion.span className="hero__name hero__name--p" {...rise(3)}>Prithvi</motion.span>
          </h1>
          <motion.span className="hero__rule" aria-hidden="true" {...rise(4)} />
          <motion.p className="hero__date" {...rise(4)}>{WEDDING.dateRange}</motion.p>
          <motion.p className="hero__line" {...rise(5)}>Two hearts, one beautiful beginning.</motion.p>
        </div>
      </div>

      <button type="button" className="hero__scroll" onClick={() => scrollToId('welcome')} aria-label="Scroll to the welcome message">
        <ChevronDown size={20} strokeWidth={1.1} />
      </button>
    </section>
  )
}
