import { art, photo } from '../lib/assets.js'

// Shows the real photograph when its file exists, otherwise a painted placeholder.
export default function PhotoSlot({ item, className = '', loading = 'lazy', fit = 'cover' }) {
  const src = photo(item.file)
  if (src) {
    return <img className={`photo ${className}`} src={src} alt={item.label} loading={loading} decoding="async" style={{ objectFit: fit }} />
  }
  return (
    <div className={`photo photo--empty ${className}`} role="img" aria-label={`${item.label}, photograph to be added`}>
      <img src={art(item.placeholder)} alt="" loading={loading} decoding="async" />
      <span className="photo__note">{item.label}</span>
    </div>
  )
}
