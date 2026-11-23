import { Share2 } from 'lucide-react'
import { art } from '../lib/assets.js'
import { CLOSING_PHOTO, hasPhoto } from '../data/photos.js'
import { WEDDING } from '../data/events.js'
import PhotoSlot from './PhotoSlot.jsx'
import Reveal from './Reveal.jsx'

const SHARE_TEXT = `You are cordially invited to the wedding celebration of Ekta and Prithvi, ${WEDDING.dateRange}.`
const WHATSAPP_URL = `https://wa.me/?text=${encodeURIComponent(`${SHARE_TEXT}\n\n${WEDDING.siteUrl}`)}`

export default function Footer({ onReplay }) {
  return (
    <footer className="close">
      <Reveal className="close__inner">
        <div className="wreath">
          {hasPhoto(CLOSING_PHOTO) ? (
            <div className="wreath__photo">
              <PhotoSlot item={CLOSING_PHOTO} />
            </div>
          ) : (
            <span className="wreath__mark" aria-hidden="true">
              E<i>&amp;</i>P
            </span>
          )}
          <img className="wreath__art" src={art('wreath')} alt="" loading="lazy" />
        </div>
        <p className="close__line">We can't wait to celebrate with you</p>
        <p className="close__love">With love,</p>
        <p className="close__names">Ekta &amp; Prithvi</p>
        <p className="close__date">{WEDDING.dateRange}</p>
        <div className="close__actions">
          <a className="btn" href={WHATSAPP_URL} target="_blank" rel="noopener noreferrer">
            <Share2 size={15} strokeWidth={1.3} aria-hidden="true" /> Share on WhatsApp
          </a>
          <button type="button" className="link-btn" onClick={onReplay}>
            Open the envelope again
          </button>
        </div>
      </Reveal>
    </footer>
  )
}
