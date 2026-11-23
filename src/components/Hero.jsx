import { useRef } from 'react'
import { motion, useReducedMotion, useScroll, useTransform } from 'framer-motion'
import { ChevronDown } from 'lucide-react'
import { artSet } from '../lib/assets.js'
import { HERO_PHOTO, hasPhoto } from '../data/photos.js'
import { WEDDING } from '../data/events.js'
import PhotoSlot from './PhotoSlot.jsx'
import { scrollToId } from './Navigation.jsx'
import { EASE, Letters, Sparkles } from './Motion.jsx'

const SIZES = '(min-width: 900px) 27vw, 44vw'

export default function Hero({ ready }) {
  const withPhoto = hasPhoto(HERO_PHOTO)
  const ref = useRef(null)
  const reduced = useReducedMotion()
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start start', 'end start'] })
  const copyY = useTransform(scrollYProgress, [0, 1], [0, 110])
  const copyOpacity = useTransform(scrollYProgress, [0, 0.78], [1, 0])
  const sprayUp = useTransform(scrollYProgress, [0, 1], [0, -90])
  const sprayDown = useTransform(scrollYProgress, [0, 1], [0, 70])

  const rise = (delay) => ({
    initial: { opacity: 0, y: 16 },
    animate: ready ? { opacity: 1, y: 0 } : { opacity: 0, y: 16 },
    transition: { duration: 1.05, delay, ease: EASE },
  })
  const bloom = (delay) => ({
    initial: { opacity: 0, scale: 0.45, rotate: -14 },
    animate: ready ? { opacity: 1, scale: 1, rotate: 0 } : { opacity: 0, scale: 0.45, rotate: -14 },
    transition: { type: 'spring', stiffness: 46, damping: 13, delay },
    style: { originX: 0, originY: 0 },
  })

  return (
    <section ref={ref} id="home" className={`hero ${withPhoto ? 'hero--photo' : ''} ${ready ? 'is-ready' : ''}`}>
      <span className="hero__frame" aria-hidden="true" />
      {ready && <Sparkles count={14} seed={2} />}
      <motion.div className="hero__spray hero__spray--tl" style={reduced ? undefined : { y: sprayUp }}>
        <motion.img {...artSet('corner-a', 440, 800)} sizes={SIZES} alt="" {...bloom(0.5)} />
      </motion.div>
      <motion.div className="hero__spray hero__spray--br" style={reduced ? undefined : { y: sprayDown }}>
        <motion.img {...artSet('corner-b', 440, 800)} sizes={SIZES} alt="" {...bloom(0.75)} />
      </motion.div>

      <motion.div className="hero__inner" style={reduced ? undefined : { y: copyY, opacity: copyOpacity }}>
        {withPhoto && (
          <motion.div className="hero__photo" {...rise(0.3)}>
            <PhotoSlot item={HERO_PHOTO} loading="eager" />
          </motion.div>
        )}
        <div className="hero__copy">
          <motion.p className="eyebrow" {...rise(0.15)}>
            The wedding celebration of
          </motion.p>
          <h1 className="hero__names" aria-label="Ekta & Prithvi">
            <span className="hero__name hero__name--e">
              <Letters text="Ekta" ready={ready} delay={0.35} step={0.08} />
            </span>
            <motion.span
              className="hero__amp"
              aria-hidden="true"
              initial={{ opacity: 0, scale: 0.2, rotate: -70 }}
              animate={ready ? { opacity: 1, scale: 1, rotate: 0 } : { opacity: 0, scale: 0.2, rotate: -70 }}
              transition={{ type: 'spring', stiffness: 90, damping: 11, delay: 0.82 }}
            >
              &amp;
            </motion.span>
            <span className="hero__name hero__name--p">
              <Letters text="Prithvi" ready={ready} delay={0.98} step={0.07} />
            </span>
          </h1>
          <motion.span
            className="hero__rule"
            aria-hidden="true"
            initial={{ scaleY: 0 }}
            animate={{ scaleY: ready ? 1 : 0 }}
            transition={{ duration: 0.8, delay: 1.55, ease: EASE }}
          />
          <motion.p className="hero__date" {...rise(1.75)}>{WEDDING.dateRange}</motion.p>
          <motion.p className="hero__line" {...rise(1.95)}>Two hearts, one beautiful beginning.</motion.p>
        </div>
      </motion.div>

      <button type="button" className="hero__scroll" onClick={() => scrollToId('welcome')} aria-label="Scroll to the welcome message">
        <ChevronDown size={20} strokeWidth={1.1} />
      </button>
    </section>
  )
}
