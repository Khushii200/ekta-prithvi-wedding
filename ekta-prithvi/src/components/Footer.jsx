import { art } from '../lib/assets.js'
import { CLOSING_PHOTO } from '../data/photos.js'
import PhotoSlot from './PhotoSlot.jsx'
import Reveal from './Reveal.jsx'

export default function Footer({ onReplay }) {
  return (
    <footer className="close">
      <img className="close__corner close__corner--l" src={art('corner-b')} alt="" loading="lazy" />
      <img className="close__corner close__corner--r" src={art('corner-a')} alt="" loading="lazy" />
      <Reveal className="close__inner">
        <div className="wreath">
          <div className="wreath__photo">
            <PhotoSlot item={CLOSING_PHOTO} />
          </div>
          <img className="wreath__art" src={art('wreath')} alt="" loading="lazy" />
        </div>
        <p className="close__line">WE CAN'T WAIT TO CELEBRATE WITH YOU</p>
        <p className="close__love">With love,</p>
        <p className="close__names">EKTA &amp; PRITHVI</p>
        <p className="close__date">26 – 30 DECEMBER 2026</p>
        <img className="close__flourish" src={art('flourish')} alt="" loading="lazy" />
        <button type="button" className="link-btn" onClick={onReplay}>
          Open the envelope again
        </button>
      </Reveal>
    </footer>
  )
}
