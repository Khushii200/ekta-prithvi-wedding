import { useCallback, useEffect, useRef, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { ChevronLeft, ChevronRight, X } from 'lucide-react'
import { GALLERY } from '../data/photos.js'
import PhotoSlot from './PhotoSlot.jsx'
import Reveal from './Reveal.jsx'

function Lightbox({ index, setIndex, onClose }) {
  const closeRef = useRef(null)
  const n = GALLERY.length
  const prev = useCallback(() => setIndex((i) => (i - 1 + n) % n), [n, setIndex])
  const next = useCallback(() => setIndex((i) => (i + 1) % n), [n, setIndex])
  const item = GALLERY[index]

  useEffect(() => {
    closeRef.current?.focus()
    const onKey = (e) => {
      if (e.key === 'Escape') onClose()
      if (e.key === 'ArrowLeft') prev()
      if (e.key === 'ArrowRight') next()
      if (e.key === 'Tab') {
        const f = e.currentTarget.querySelectorAll?.('.lightbox button') ?? document.querySelectorAll('.lightbox button')
        const first = f[0]
        const last = f[f.length - 1]
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault()
          last.focus()
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault()
          first.focus()
        }
      }
    }
    document.addEventListener('keydown', onKey)
    document.documentElement.classList.add('intro-open')
    return () => {
      document.removeEventListener('keydown', onKey)
      document.documentElement.classList.remove('intro-open')
    }
  }, [onClose, prev, next])

  return (
    <motion.div
      className="lightbox"
      role="dialog"
      aria-modal="true"
      aria-label={`Photograph ${index + 1} of ${n}: ${item.label}`}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <button ref={closeRef} type="button" className="lightbox__btn lightbox__close" onClick={onClose} aria-label="Close photograph">
        <X size={22} strokeWidth={1.3} />
      </button>
      <button type="button" className="lightbox__btn lightbox__prev" onClick={prev} aria-label="Previous photograph">
        <ChevronLeft size={26} strokeWidth={1.2} />
      </button>
      <AnimatePresence mode="wait" initial={false}>
        <motion.figure
          key={index}
          className="lightbox__fig"
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.25 }}
        >
          <PhotoSlot item={item} loading="eager" fit="contain" />
          <figcaption>
            {item.label} <span>{index + 1} of {n}</span>
          </figcaption>
        </motion.figure>
      </AnimatePresence>
      <button type="button" className="lightbox__btn lightbox__next" onClick={next} aria-label="Next photograph">
        <ChevronRight size={26} strokeWidth={1.2} />
      </button>
    </motion.div>
  )
}

export default function Gallery() {
  const [index, setIndex] = useState(null)
  const lastTrigger = useRef(null)
  const close = useCallback(() => {
    setIndex(null)
    lastTrigger.current?.focus()
  }, [])

  return (
    <section id="gallery" className="gallery">
      <Reveal className="section-head">
        <h2 className="h2">Little Moments, Big Memories</h2>
      </Reveal>
      <div className="gallery__grid">
        {GALLERY.map((item, i) => (
          <button
            key={item.file}
            type="button"
            className={`gallery__item gallery__item--${item.slot}`}
            onClick={(e) => {
              lastTrigger.current = e.currentTarget
              setIndex(i)
            }}
            aria-label={`Open ${item.label}`}
          >
            <PhotoSlot item={item} />
          </button>
        ))}
      </div>
      <AnimatePresence>{index !== null && <Lightbox index={index} setIndex={setIndex} onClose={close} />}</AnimatePresence>
    </section>
  )
}
