import { useMemo } from 'react'
import { art } from '../lib/assets.js'

// A handful of painted petals drifting down behind the page. Hidden for reduced motion.
export default function Petals() {
  const petals = useMemo(
    () =>
      Array.from({ length: 8 }, (_, i) => ({
        src: art(`petal-${(i % 3) + 1}`),
        left: `${6 + ((i * 37) % 90)}%`,
        size: 14 + ((i * 7) % 12),
        duration: 24 + ((i * 11) % 18),
        delay: -((i * 9) % 30),
        drift: (i % 2 ? 1 : -1) * (30 + ((i * 13) % 50)),
      })),
    [],
  )
  return (
    <div className="petals" aria-hidden="true">
      {petals.map((p, i) => (
        <img
          key={i}
          src={p.src}
          alt=""
          style={{ left: p.left, width: p.size, height: p.size, animationDuration: `${p.duration}s`, animationDelay: `${p.delay}s`, '--drift': `${p.drift}px` }}
        />
      ))}
    </div>
  )
}
