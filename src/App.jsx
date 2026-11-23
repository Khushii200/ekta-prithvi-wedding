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
import { GALLERY_PHOTOS } from './data/photos.js'

// Every load starts at the envelope, so the browser must not restore the old scroll position.
if ('scrollRestoration' in history) history.scrollRestoration = 'manual'

export default function App() {
  const [opened, setOpened] = useState(false)
  const mainRef = useRef(null)

  const finish = useCallback(() => {
    window.scrollTo(0, 0)
    setOpened(true)
  }, [])

  const replay = useCallback(() => {
    window.scrollTo(0, 0)
    setOpened(false)
  }, [])

  useEffect(() => {
    document.documentElement.classList.toggle('intro-open', !opened)
    if (mainRef.current) mainRef.current.inert = !opened
  }, [opened])

  return (
    <MotionConfig reducedMotion="user">
      {!opened && <EnvelopeIntro onDone={finish} />}

      <div ref={mainRef} className="site">
        <Navigation visible={opened} />
        <main>
          <Hero ready={opened} />
          <Welcome />
          <WeddingEvents />
          <Venue />
          <Countdown />
          {GALLERY_PHOTOS.length > 0 && <Gallery />}
          <RSVP />
        </main>
        <Footer onReplay={replay} />
        {opened && <MusicPlayer />}
      </div>
    </MotionConfig>
  )
}
