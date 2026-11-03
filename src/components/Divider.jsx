import { art } from '../lib/assets.js'

// A loose wash of colour that bleeds across the seam between two sections.
export function Bleed({ tone }) {
  return (
    <div className="bleed" aria-hidden="true">
      <img src={art(`wash-${tone}`)} alt="" loading="lazy" decoding="async" />
    </div>
  )
}

export default function Divider({ art: name, narrow }) {
  return (
    <div className={`divider ${narrow ? 'divider--narrow' : ''}`} aria-hidden="true">
      <img src={art(name)} alt="" width={narrow ? 570 : 1050} height={narrow ? 240 : 180} loading="lazy" decoding="async" />
    </div>
  )
}
