import { motion } from 'framer-motion'

export const EASE = [0.22, 0.7, 0.3, 1]

const HIDDEN = { y: '115%', rotate: 7, opacity: 0 }
const SHOWN = { y: 0, rotate: 0, opacity: 1 }

// Text that rises letter by letter from behind a mask.
export function Letters({ text, ready = true, inView = false, delay = 0, step = 0.055 }) {
  const trigger = inView ? { whileInView: SHOWN, viewport: { once: true, margin: '-6% 0px' } } : { animate: ready ? SHOWN : HIDDEN }
  return (
    <span className="letters" aria-hidden="true">
      {[...text].map((c, i) => (
        <span className="letters__mask" key={i}>
          <motion.span
            className="letters__char"
            style={{ '--i': i }}
            initial={HIDDEN}
            {...trigger}
            transition={{ duration: 0.95, delay: delay + i * step, ease: EASE }}
          >
            {c === ' ' ? ' ' : c}
          </motion.span>
        </span>
      ))}
    </span>
  )
}

const PARENT = { hidden: {}, show: { transition: { staggerChildren: 0.1 } } }
const CHILD = { hidden: { opacity: 0, y: 24 }, show: { opacity: 1, y: 0, transition: { duration: 0.85, ease: EASE } } }

// Children marked <Item> arrive one after another.
export function Stagger({ as = 'div', children, ...rest }) {
  const M = motion[as]
  return (
    <M variants={PARENT} initial="hidden" whileInView="show" viewport={{ once: true, margin: '-10% 0px' }} {...rest}>
      {children}
    </M>
  )
}

export function Item({ as = 'div', children, ...rest }) {
  const M = motion[as]
  return (
    <M variants={CHILD} {...rest}>
      {children}
    </M>
  )
}

// Small gold stars that twinkle. Positions are fixed so they never jump between renders.
export function Sparkles({ count = 10, seed = 1 }) {
  return (
    <span className="sparkles" aria-hidden="true">
      {Array.from({ length: count }, (_, i) => (
        <i
          key={i}
          style={{
            left: `${((i + 1) * 37 + seed * 13) % 96 + 2}%`,
            top: `${((i + 1) * 53 + seed * 29) % 92 + 4}%`,
            width: 7 + ((i * 5) % 10),
            height: 7 + ((i * 5) % 10),
            animationDuration: `${2.6 + (i % 4) * 0.7}s`,
            animationDelay: `${-(i * 0.73)}s`,
          }}
        />
      ))}
    </span>
  )
}
