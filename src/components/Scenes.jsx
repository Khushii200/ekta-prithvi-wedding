import { useEffect, useRef, useState } from 'react'
import { useReducedMotion } from 'framer-motion'
import { art } from '../lib/assets.js'
import '../scenes.css'

// Six painted, always-moving scenes. The couple's faces are cut directly from
// their portrait; outfits, guests and settings are drawn here. Every animated
// group rotates or moves around its own local origin, so a joint is simply
// wherever its parent group was translated to.

const delay = (s) => ({ animationDelay: `${s}s` })

function Flame({ x = 0, y = 0, s = 1 }) {
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      <defs><radialGradient id="flame-glow"><stop offset="0%" stopColor="#ffd98a" stopOpacity=".75" /><stop offset="100%" stopColor="#ffc35a" stopOpacity="0" /></radialGradient></defs>
      <circle className="a-glow" r="42" cy="-16" fill="url(#flame-glow)" />
      <path className="a-flick" d="M0 2C-16-6-13-24 0-42C13-24 16-6 0 2Z" fill="#f5792a" />
      <path className="a-flick" style={delay(-0.3)} d="M0 2C-8-3-7-14 0-24C7-14 8-3 0 2Z" fill="#ffe08a" />
    </g>
  )
}

// Mehendi uses the couple's own painting, cut out and split into moving layers.
const LAYERS = {
  'mehendi-body': [0, 291, 1199, 865],
  'mehendi-henna': [401, 877, 376, 95],
  'mehendi-hand': [315, 741, 258, 229],
  'mehendi-groom-head': [326, 135, 339, 403],
  'mehendi-bride-head': [656, 210, 404, 379],
  'mehendi-earring': [899, 400, 66, 95],
  'vrat-body': [0, 28, 1199, 1268],
  'vrat-hand': [540, 707, 163, 157],
  'vrat-bride-head': [292, 139, 443, 436],
  'vrat-earring-l': [384, 394, 67, 77],
  'vrat-earring-r': [611, 380, 54, 56],
  'vrat-groom-head': [575, 25, 359, 454],
  'vrat-diya': [377, 1235, 146, 77],
  'cocktail-groom-head': [357, 30, 328, 346],
  'cocktail-earring': [855, 377, 67, 93],
  'cocktail-martini': [695, 642, 213, 216],
  'cocktail-whisky': [436, 601, 162, 181],
  'cocktail-skirt': [531, 908, 678, 381],
  'cocktail-bride-head': [687, 217, 350, 289],
  'cocktail-glitter-a': [532, 907, 676, 380],
  'cocktail-glitter-b': [532, 907, 676, 380],
  'cocktail-body': [3, 244, 1121, 1045],
  'hasta-groom-head': [348, 20, 396, 430],
  'hasta-hand': [495, 407, 78, 118],
  'hasta-strand-l': [297, 605, 193, 686],
  'hasta-strand-r': [430, 775, 97, 516],
  'hasta-veil': [974, 613, 238, 678],
  'hasta-earring': [843, 491, 85, 119],
  'hasta-bride-head': [673, 268, 436, 390],
  'hasta-body': [3, 225, 1128, 1064],
  'jaan-parasol': [132, 410, 361, 437],
  'jaan-horse-head': [425, 767, 149, 301],
  'jaan-medal': [394, 1123, 69, 151],
  'jaan-ornament': [57, 1058, 129, 200],
  'jaan-guest-arm': [1, 837, 72, 120],
  'jaan-groom-head': [283, 591, 107, 134],
  'jaan-earring': [676, 888, 32, 49],
  'jaan-bride-head': [592, 826, 162, 157],
  'jaan-skirt': [438, 1104, 503, 533],
  'jaan-body': [3, 419, 804, 1235],
  'reception-skirt': [476, 731, 776, 520],
  'reception-arms': [523, 72, 259, 407],
  'reception-bride-head': [747, 252, 265, 240],
  'reception-groom-head': [347, 120, 190, 230],
  'reception-hand': [1061, 898, 80, 129],
  'reception-body': [205, 72, 935, 1177],
}

function Layer({ name, px = 0, py = 0 }) {
  const [x, y, width, height] = LAYERS[name]
  return <image href={art(name)} x={x - px} y={y - py} width={width} height={height} />
}

function Moving({ name, px, py, cls }) {
  return (
    <g transform={`translate(${px} ${py})`}>
      <g className={cls}><Layer name={name} px={px} py={py} /></g>
    </g>
  )
}

function MehendiCouple() {
  const reduced = useReducedMotion()
  return (
    <>
      <Layer name="mehendi-body" />
      {reduced ? (
        <Layer name="mehendi-henna" />
      ) : (
        <>
          <defs>
            <radialGradient id="henna-edge">
              <stop offset="88%" stopColor="#fff" />
              <stop offset="100%" stopColor="#fff" stopOpacity="0" />
            </radialGradient>
            <mask id="henna-reveal" maskUnits="userSpaceOnUse" x="380" y="850" width="420" height="140">
              <circle cx="560" cy="915" fill="url(#henna-edge)">
                <animate attributeName="r" dur="9s" repeatCount="indefinite" values="8;250;250;8" keyTimes="0;0.72;0.97;1" />
              </circle>
            </mask>
          </defs>
          <g mask="url(#henna-reveal)">
            <g className="m-henna"><Layer name="mehendi-henna" /></g>
          </g>
        </>
      )}
      <Moving name="mehendi-hand" px={320} py={915} cls="m-hand" />
      <Moving name="mehendi-groom-head" px={430} py={490} cls="m-groom" />
      <g transform="translate(840 575)">
        <g className="m-bride">
          <Layer name="mehendi-bride-head" px={840} py={575} />
          <g transform="translate(92 -163)">
            <g className="m-ear"><Layer name="mehendi-earring" px={932} py={412} /></g>
          </g>
        </g>
      </g>
    </>
  )
}

function JaanCouple() {
  return (
    <>
      <Moving name="jaan-parasol" px={405} py={838} cls="j-parasol" />
      <Layer name="jaan-body" />
      <Moving name="jaan-medal" px={428} py={1128} cls="j-medal" />
      <Moving name="jaan-horse-head" px={448} py={935} cls="j-horse" />
      <Moving name="jaan-groom-head" px={326} py={716} cls="j-groom" />
      <Moving name="jaan-guest-arm" px={26} py={948} cls="j-wave" />
      <Moving name="jaan-skirt" px={685} py={1106} cls="j-skirt" />
      <g transform="translate(672 975)">
        <g className="j-bride">
          <Layer name="jaan-bride-head" px={672} py={975} />
          <g transform="translate(19 -82)">
            <g className="m-ear"><Layer name="jaan-earring" px={691} py={893} /></g>
          </g>
        </g>
      </g>
      <Moving name="jaan-ornament" px={117} py={1250} cls="j-ornament" />
    </>
  )
}

function HastaCouple() {
  return (
    <>
      <Layer name="hasta-body" />
      <Moving name="hasta-strand-l" px={346} py={610} cls="h-strand" />
      <Moving name="hasta-strand-r" px={490} py={780} cls="h-strand h-strand--late" />
      <Moving name="hasta-groom-head" px={440} py={372} cls="h-groom" />
      <Layer name="hasta-hand" />
      <Moving name="hasta-veil" px={1045} py={640} cls="h-veil" />
      <g transform="translate(860 640)">
        <g className="h-bride">
          <Layer name="hasta-bride-head" px={860} py={640} />
          <g transform="translate(25 -142)">
            <g className="m-ear"><Layer name="hasta-earring" px={885} py={498} /></g>
          </g>
        </g>
      </g>
    </>
  )
}

function ReceptionCouple() {
  return (
    <>
      <Layer name="reception-body" />
      <Moving name="reception-skirt" px={878} py={738} cls="r-skirt" />
      <Layer name="reception-hand" />
      <Moving name="reception-arms" px={640} py={420} cls="r-arms" />
      <Moving name="reception-bride-head" px={870} py={475} cls="r-bride" />
      <Moving name="reception-groom-head" px={465} py={340} cls="r-groom" />
    </>
  )
}

function VratCouple() {
  return (
    <>
      <Layer name="vrat-body" />
      <Moving name="vrat-hand" px={545} py={825} cls="v-pat" />
      <g transform="translate(520 545)">
        <g className="m-bride">
          <Layer name="vrat-bride-head" px={520} py={545} />
          <g transform="translate(-104 -147)">
            <g className="m-ear"><Layer name="vrat-earring-l" px={416} py={398} /></g>
          </g>
          <g transform="translate(116 -161)">
            <g className="m-ear" style={delay(-0.7)}><Layer name="vrat-earring-r" px={636} py={384} /></g>
          </g>
        </g>
      </g>
      <Moving name="vrat-groom-head" px={840} py={480} cls="v-groom" />
      <g transform="translate(-249 -87)"><Layer name="vrat-diya" /></g>
      <Flame x={200} y={1162} s={1.05} />
    </>
  )
}

function CocktailCouple() {
  return (
    <>
      <defs>
        <radialGradient id="cocktail-glow">
          <stop offset="0%" stopColor="#f0c98a" stopOpacity=".42" />
          <stop offset="62%" stopColor="#d99f5e" stopOpacity=".16" />
          <stop offset="100%" stopColor="#d99f5e" stopOpacity="0" />
        </radialGradient>
      </defs>
      <ellipse className="a-glow" cx="606" cy="600" rx="640" ry="640" fill="url(#cocktail-glow)" />
      <Layer name="cocktail-body" />
      <g transform="translate(860 908)">
        <g className="c-skirt">
          <Layer name="cocktail-skirt" px={860} py={908} />
          <g className="c-glitter"><Layer name="cocktail-glitter-a" px={860} py={908} /></g>
          <g className="c-glitter c-glitter--late"><Layer name="cocktail-glitter-b" px={860} py={908} /></g>
        </g>
      </g>
      <Moving name="cocktail-whisky" px={580} py={760} cls="c-whisky" />
      <Moving name="cocktail-groom-head" px={445} py={350} cls="c-groom" />
      <g transform="translate(860 505)">
        <g className="c-bride">
          <Layer name="cocktail-bride-head" px={860} py={505} />
          <g transform="translate(26 -123)">
            <g className="m-ear"><Layer name="cocktail-earring" px={886} py={382} /></g>
          </g>
        </g>
      </g>
      <Moving name="cocktail-martini" px={885} py={805} cls="c-martini" />
    </>
  )
}

const SCENES = {
  mehendi: MehendiCouple,
  'jaan-swagat': JaanCouple,
  'hasta-melap': HastaCouple,
  reception: ReceptionCouple,
  vrat: VratCouple,
  cocktail: CocktailCouple,
}

export const SCENE_ALT = {
  mehendi: 'Animated illustration of Prithvi carefully applying henna to Ekta\'s hand as she rests her chin on her other hand and smiles at him',
  'jaan-swagat': 'Animated illustration of Prithvi arriving on a decorated white horse under a red parasol as Ekta greets him and guests celebrate',
  'hasta-melap': 'Animated illustration of Ekta in a pink veil placing a flower garland around Prithvi as they gaze at each other',
  reception: 'Animated illustration of Prithvi in a black tuxedo twirling Ekta in a flowing pink gown, their hands joined overhead',
  vrat: 'Animated illustration of Ekta and Prithvi sitting close together and smiling, her hand on his arm, beside a lit brass diya',
  cocktail: 'Animated illustration of Prithvi in a black suit and Ekta in a sparkling navy lehenga, smiling at each other with drinks in hand',
}

// Scenes built from the couple's own paintings sit directly on the page.
const FREE = { cocktail: [0, 24, 1213, 1272], 'hasta-melap': [0, 19, 1213, 1277], 'jaan-swagat': [0, 405, 941, 1265], mehendi: [0, 120, 1199, 1040], vrat: [0, 20, 1199, 1280], reception: [190, 60, 1064, 1194] }

export default function Scene({ id }) {
  const ref = useRef(null)
  const [on, setOn] = useState(true)
  const Painting = SCENES[id]
  const free = FREE[id]

  // Scenes run constantly while visible and rest off-screen to spare phone batteries.
  useEffect(() => {
    const el = ref.current
    if (!el || !('IntersectionObserver' in window)) return undefined
    const io = new IntersectionObserver(([entry]) => setOn(entry.isIntersecting), { rootMargin: '120px' })
    io.observe(el)
    return () => io.disconnect()
  }, [])

  return (
    <div ref={ref} className={`scene ${free ? 'scene--free' : ''} ${on ? '' : 'scene--rest'}`} style={free ? { aspectRatio: `${free[2]} / ${free[3]}` } : undefined}>
      <svg viewBox={free ? free.join(' ') : '0 0 600 600'} role="img" aria-label={SCENE_ALT[id]}>
        <Painting />
      </svg>
    </div>
  )
}
