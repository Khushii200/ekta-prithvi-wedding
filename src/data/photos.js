import { photo } from '../lib/assets.js'

// To add a real photograph, save it in src/assets/photos using the file name
// listed here (any of .jpg .jpeg .png .webp .avif). It appears automatically.
// Until then its space is left out, so guests never see an empty frame.
// Example: src/assets/photos/gallery-1.jpg

export const HERO_PHOTO = { file: 'couple-hero', label: 'Ekta and Prithvi' }
export const WELCOME_PHOTO = { file: 'welcome', label: 'Ekta and Prithvi' }
export const CLOSING_PHOTO = { file: 'closing', label: 'Ekta and Prithvi' }

export const GALLERY = [
  { file: 'gallery-1', label: 'Couple portrait' },
  { file: 'gallery-2', label: 'Candid moment' },
  { file: 'gallery-3', label: 'Engagement' },
  { file: 'gallery-4', label: 'Family' },
  { file: 'gallery-5', label: 'Couple portrait' },
  { file: 'gallery-6', label: 'Special moment' },
  { file: 'gallery-7', label: 'Engagement' },
  { file: 'gallery-8', label: 'Candid moment' },
  { file: 'gallery-9', label: 'Family' },
]

export const hasPhoto = (item) => Boolean(photo(item.file))
export const GALLERY_PHOTOS = GALLERY.filter(hasPhoto)
