import { useEffect, useRef, useState } from 'react'
import { Music, Pause } from 'lucide-react'
import { musicFile } from '../lib/assets.js'

// Plays only when the guest presses the button. Nothing starts on its own.
export default function MusicPlayer() {
  const audio = useRef(null)
  const [playing, setPlaying] = useState(false)
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    const a = audio.current
    return () => a?.pause()
  }, [])

  if (!musicFile || failed) return null

  const toggle = async () => {
    const a = audio.current
    if (playing) {
      a.pause()
      setPlaying(false)
      return
    }
    try {
      a.volume = 0.55
      await a.play()
      setPlaying(true)
    } catch {
      setPlaying(false)
    }
  }

  return (
    <div className="music">
      <audio ref={audio} src={musicFile} loop preload="none" onError={() => setFailed(true)} />
      <button type="button" className={`music__btn ${playing ? 'is-on' : ''}`} onClick={toggle} aria-pressed={playing} aria-label={playing ? 'Pause music' : 'Play music'} title={playing ? 'Pause music' : 'Play music'}>
        {playing ? <Pause size={17} strokeWidth={1.4} /> : <Music size={17} strokeWidth={1.4} />}
      </button>
    </div>
  )
}
