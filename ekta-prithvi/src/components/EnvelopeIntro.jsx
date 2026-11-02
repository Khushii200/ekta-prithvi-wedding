import { useEffect, useRef, useState } from 'react'
import { AnimatePresence, motion, useReducedMotion } from 'framer-motion'
import { art } from '../lib/assets.js'
import { WEDDING } from '../data/events.js'

const wait = (ms) => new Promise((r) => setTimeout(r, ms))
const EASE = [0.45, 0.05, 0.2, 1]
const ORDER = ['idle', 'seal', 'flap', 'rise', 'expand', 'fade']

export default function EnvelopeIntro({ onDone }) {
  const reduced = useReducedMotion()
  const [stage, setStage] = useState('idle')
  const [card, setCard] = useState({ x: 0, y: 0, scale: 1 })
  const cardRef = useRef(null)
  const alive = useRef(true)
  const at = (s) => ORDER.indexOf(stage) >= ORDER.indexOf(s)

  useEffect(() => {
    alive.current = true
    return () => {
      alive.current = false
    }
  }, [])

  const skip = async () => {
    if (!alive.current) return
    alive.current = false
    setStage('fade')
    await wait(reduced ? 150 : 450)
    onDone()
  }

  const open = async () => {
    if (stage !== 'idle') return
    if (reduced) return skip()
    const step = async (name, ms, before) => {
      if (!alive.current) return false
      before?.()
      setStage(name)
      await wait(ms)
      return alive.current
    }
    if (!(await step('seal', 620))) return
    if (!(await step('flap', 1000))) return
    const h = cardRef.current?.offsetHeight ?? 300
    const riseY = -h * 0.44
    if (!(await step('rise', 1150, () => setCard({ x: 0, y: riseY, scale: 1 })))) return
    const expand = () => {
      const r = cardRef.current.getBoundingClientRect()
      const vw = window.innerWidth
      const vh = window.innerHeight
      setCard({
        x: vw / 2 - (r.left + r.width / 2),
        y: riseY + (vh / 2 - (r.top + r.height / 2)),
        scale: Math.max(vw / r.width, vh / r.height) * 1.12,
      })
    }
    if (!(await step('expand', 1250, expand))) return
    if (!(await step('fade', 650))) return
    alive.current = false
    onDone()
  }

  return (
    <motion.div
      className="intro"
      animate={{ opacity: stage === 'fade' ? 0 : 1 }}
      transition={{ duration: 0.6, ease: 'easeInOut' }}
      role="dialog"
      aria-label="Wedding invitation envelope"
    >
      <img className="intro__corner intro__corner--tl" src={art('corner-b')} alt="" />
      <img className="intro__corner intro__corner--br" src={art('corner-a')} alt="" />

      <div className="intro__stage">
        <motion.div
          className={`envelope ${stage === 'idle' ? 'envelope--float' : ''}`}
          animate={{ y: at('rise') ? 'min(16vh, 90px)' : 0 }}
          transition={{ duration: 1.1, ease: EASE }}
          onClick={open}
          aria-hidden="true"
        >
          <motion.div className="envelope__body" animate={{ opacity: at('expand') ? 0 : 1 }} transition={{ duration: 0.5 }}>
            <div className="envelope__back">
              <img src={art('env-liner')} alt="" />
            </div>
            <div className="envelope__shadow" />
          </motion.div>

          {/* The flap: paper outside, painted lining inside. It drops behind the card once open. */}
          <motion.div
            className="flap"
            style={{ zIndex: at('rise') ? 1 : 5 }}
            initial={{ rotateX: 0 }}
            animate={{ rotateX: at('flap') ? 180 : 0, opacity: at('expand') ? 0 : 1 }}
            transition={{ rotateX: { duration: 1, ease: EASE }, opacity: { duration: 0.4 } }}
          >
            <div className="flap__shade" />
            <div className="flap__face flap__face--front">
              <img src={art('env-flap')} alt="" />
            </div>
            <div className="flap__face flap__face--back">
              <img src={art('env-liner')} alt="" />
            </div>
          </motion.div>

          <motion.div
            ref={cardRef}
            className="inner-card"
            style={{ zIndex: at('expand') ? 6 : 2 }}
            animate={card}
            transition={{ duration: stage === 'expand' ? 1.2 : 1.1, ease: EASE }}
          >
            <motion.div
              className="inner-card__text"
              animate={{ opacity: at('expand') ? 0 : 1 }}
              transition={{ duration: 0.45 }}
            >
              <img src={art('flourish')} alt="" />
              <span className="inner-card__small">The wedding celebration of</span>
              <span className="inner-card__names">Ekta &amp; Prithvi</span>
              <span className="inner-card__small">{WEDDING.dateRange}</span>
            </motion.div>
          </motion.div>

          <motion.div className="pocket" style={{ zIndex: 3 }} animate={{ opacity: at('expand') ? 0 : 1 }} transition={{ duration: 0.5 }}>
            <img src={art('env-pocket')} alt="" />
            <span className="pocket__text">A wedding invitation</span>
          </motion.div>

          {/* The wax seal cracks in two and the halves fall away */}
          {!at('flap') && (
            <div className="seal">
              {stage === 'seal' ? (
                <>
                  <motion.img
                    src={art('seal')}
                    alt=""
                    className="seal__half seal__half--l"
                    animate={{ x: -22, y: 46, rotate: -16, opacity: 0 }}
                    transition={{ duration: 0.62, ease: 'easeIn' }}
                  />
                  <motion.img
                    src={art('seal')}
                    alt=""
                    className="seal__half seal__half--r"
                    animate={{ x: 22, y: 58, rotate: 14, opacity: 0 }}
                    transition={{ duration: 0.62, ease: 'easeIn' }}
                  />
                </>
              ) : (
                <img src={art('seal')} alt="" />
              )}
            </div>
          )}
        </motion.div>

        <AnimatePresence>
          {stage === 'idle' && (
            <motion.div className="intro__call" exit={{ opacity: 0, y: 10 }} transition={{ duration: 0.4 }}>
              <p className="intro__invited">YOU ARE CORDIALLY INVITED</p>
              <button type="button" className="btn" onClick={open}>
                OPEN YOUR INVITATION
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {stage !== 'fade' && (
        <button type="button" className="intro__skip" onClick={skip}>
          Skip animation
        </button>
      )}
    </motion.div>
  )
}
