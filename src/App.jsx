import { useCallback, useEffect, useRef, useState } from 'react'
import { MotionConfig } from 'framer-motion'
import EnvelopeIntro from './components/EnvelopeIntro.jsx'
import Navigation from './components/Navigation.jsx'
import Hero from './components/Hero.jsx'
import Welcome from './components/Welcome.jsx'
import WeddingEvents from './components/WeddingEvents.jsx'
import Venue from './components/Venue.jsx'
import Countdown from './components/Countdown.jsx'
import Gallery from './components/Gallery.jsx'
import RSVP from './components/RSVP.jsx'
import Footer from './components/Footer.jsx'
import MusicPlayer from './components/MusicPlayer.jsx'
import Petals from './components/Petals.jsx'
import Divider from './components/Divider.jsx'

const KEY = 'ep-invitation-opened'
const wasOpened = () => {
  try {
    return localStorage.getItem(KEY) === '1'
  } catch {
    return false
  }
}

export default function App() {
  const [opened, setOpened] = useState(wasOpened)
  const mainRef = useRef(null)

  const finish = useCallback(() => {
    setOpened(true)
    try {
      localStorage.setItem(KEY, '1')
    } catch {
      /* the invitation simply opens again next time */
    }
  }, [])

  const replay = useCallback(() => {
    try {
      localStorage.removeItem(KEY)
    } catch {
      /* nothing to clear */
    }
    window.scrollTo(0, 0)
    setOpened(false)
  }, [])

  useEffect(() => {
    document.documentElement.classList.toggle('intro-open', !opened)
    if (mainRef.current) mainRef.current.inert = !opened
  }, [opened])

  return (
    <MotionConfig reducedMotion="user">
      {/* Roughens the edges of paper cards */}
      <svg width="0" height="0" style={{ position: 'absolute' }} aria-hidden="true">
        <filter id="deckle">
          <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="4" />
          <feDisplacementMap in="SourceGraphic" scale="5" />
        </filter>
      </svg>

      {!opened && <EnvelopeIntro onDone={finish} />}

      <div ref={mainRef} className="site">
        <Navigation visible={opened} />
        {opened && <Petals />}
        <main>
          <Hero />
          <Welcome />
          <Divider art="garland" />
          <WeddingEvents />
          <Venue />
          <Countdown />
          <Divider art="sprig-b" narrow />
          <Gallery />
          <RSVP />
        </main>
        <Footer onReplay={replay} />
        {opened && <MusicPlayer />}
      </div>
    </MotionConfig>
  )
}
