import { photo } from '../lib/assets.js'

// Shows the photograph when its file exists, and nothing otherwise.
export default function PhotoSlot({ item, className = '', loading = 'lazy', fit = 'cover' }) {
  const src = photo(item.file)
  if (!src) return null
  return <img className={`photo ${className}`} src={src} alt={item.label} loading={loading} decoding="async" style={{ objectFit: fit }} />
}
