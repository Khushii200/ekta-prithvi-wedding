import { useEffect, useRef, useState } from 'react'
import { useReducedMotion } from 'framer-motion'
import { art } from '../lib/assets.js'

const LIFE = 4.2
const DRAG = 2.1
const GRAVITY = 120
const GOLDS = ['#c9a96a', '#e2c98f', '#a98c5a']

// One burst of petals and gold dust as the invitation opens, then the canvas removes itself.
export default function PetalBurst() {
  const ref = useRef(null)
  const reduced = useReducedMotion()
  const [done, setDone] = useState(false)

  useEffect(() => {
    if (reduced) {
      setDone(true)
      return
    }
    const canvas = ref.current
    const ctx = canvas?.getContext('2d')
    if (!ctx) return
    const dpr = Math.min(window.devicePixelRatio || 1, 2)
    const w = window.innerWidth
    const h = window.innerHeight
    canvas.width = w * dpr
    canvas.height = h * dpr
    ctx.scale(dpr, dpr)

    const petals = [1, 2, 3].map((n) => {
      const img = new Image()
      img.src = art(`petal-${n}`)
      return img
    })
    const reach = Math.max(w, h)
    const parts = Array.from({ length: w < 700 ? 52 : 90 }, (_, i) => {
      const angle = Math.random() * Math.PI * 2
      const speed = reach * (0.25 + Math.random() * 0.75)
      return {
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed - reach * 0.18,
        size: i % 5 < 3 ? 12 + Math.random() * 16 : 2 + Math.random() * 3.5,
        petal: i % 5 < 3 ? petals[i % 3] : null,
        color: GOLDS[i % 3],
        spin: Math.random() * Math.PI * 2,
        spinV: (Math.random() - 0.5) * 5,
        phase: Math.random() * Math.PI * 2,
      }
    })

    let raf
    const start = performance.now()
    // Positions are worked out from elapsed time, so slow phones get the same burst with fewer frames.
    const frame = (now) => {
      const t = (now - start) / 1000
      const eased = (1 - Math.exp(-DRAG * t)) / DRAG
      ctx.clearRect(0, 0, w, h)
      ctx.globalAlpha = Math.min(1, Math.max(0, (LIFE - t) / 1.5))
      for (const p of parts) {
        const x = w / 2 + p.vx * eased + Math.sin(t * 2 + p.phase) * 14
        const y = h * 0.44 + (p.vy - GRAVITY / DRAG) * eased + (GRAVITY / DRAG) * t
        if (p.petal?.complete && p.petal.naturalWidth) {
          ctx.save()
          ctx.translate(x, y)
          ctx.rotate(p.spin + p.spinV * t)
          ctx.drawImage(p.petal, -p.size / 2, -p.size / 2, p.size, p.size)
          ctx.restore()
        } else if (!p.petal) {
          ctx.fillStyle = p.color
          ctx.beginPath()
          ctx.arc(x, y, p.size, 0, Math.PI * 2)
          ctx.fill()
        }
      }
      if (t < LIFE) raf = requestAnimationFrame(frame)
      else setDone(true)
    }
    raf = requestAnimationFrame(frame)
    // If the tab is in the background, frames stop: never leave petals frozen on the page.
    const stop = setTimeout(() => setDone(true), (LIFE + 0.4) * 1000)
    return () => {
      cancelAnimationFrame(raf)
      clearTimeout(stop)
    }
  }, [reduced])

  if (done) return null
  return <canvas ref={ref} className="burst" aria-hidden="true" />
}
