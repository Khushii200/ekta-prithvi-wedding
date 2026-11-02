import { art } from '../lib/assets.js'

export default function Divider({ art: name, narrow }) {
  return (
    <div className={`divider ${narrow ? 'divider--narrow' : ''}`} aria-hidden="true">
      <img src={art(name)} alt="" width={narrow ? 570 : 1050} height={narrow ? 240 : 180} loading="lazy" decoding="async" />
    </div>
  )
}
