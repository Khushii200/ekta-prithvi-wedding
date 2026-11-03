import { ChevronDown } from 'lucide-react'
import { art } from '../lib/assets.js'
import { HERO_PHOTO } from '../data/photos.js'
import PhotoSlot from './PhotoSlot.jsx'
import { scrollToId } from './Navigation.jsx'

export default function Hero() {
  return (
    <section id="home" className="hero">
      <img className="hero__corner hero__corner--tl" src={art('corner-a')} alt="" />
      <img className="hero__corner hero__corner--tr" src={art('corner-c')} alt="" />
      <img className="hero__corner hero__corner--bl" src={art('corner-b')} alt="" />
      <img className="hero__corner hero__corner--br" src={art('corner-d')} alt="" />

      <div className="hero__grid">
        <p className="hero__eyebrow">THE WEDDING CELEBRATION OF</p>
        <h1 className="hero__names">
          <span className="hero__name hero__name--e">EKTA</span>
          <span className="hero__amp">&amp;</span>
          <span className="hero__name hero__name--p">PRITHVI</span>
        </h1>
        <div className="arch">
          <div className="arch__window">
            <PhotoSlot item={HERO_PHOTO} loading="eager" />
          </div>
          <img className="arch__art" src={art('arch')} alt="" />
        </div>
        <div className="hero__foot">
          <p className="hero__line">Two hearts, one beautiful beginning.</p>
          <p className="hero__date">26 – 30 DECEMBER 2026</p>
        </div>
      </div>

      <button type="button" className="hero__scroll" onClick={() => scrollToId('welcome')} aria-label="Scroll to the welcome message">
        <ChevronDown size={20} strokeWidth={1.2} />
      </button>
    </section>
  )
}
