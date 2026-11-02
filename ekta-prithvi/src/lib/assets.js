// Finds files by name, so replacing art or photos never needs a code change.
const files = import.meta.glob('../assets/**/*.{webp,png,jpg,jpeg,avif,svg,mp3,m4a,ogg,wav}', {
  eager: true,
  query: '?url',
  import: 'default',
})

const index = { illustrations: {}, photos: {}, music: [] }
for (const [path, url] of Object.entries(files)) {
  const base = path.split('/').pop().replace(/\.[^.]+$/, '')
  if (path.includes('/illustrations/')) index.illustrations[base] = url
  else if (path.includes('/photos/')) index.photos[base] = url
  else if (path.includes('/music/')) index.music.push(url)
}

export const art = (name) => index.illustrations[name]
export const photo = (name) => index.photos[name]
export const musicFile = index.music[0]
