import { motion } from 'framer-motion'

// A soft rise into place, once, as the element scrolls into view.
export default function Reveal({ children, delay = 0, y = 22, className, as = 'div', ...rest }) {
  const M = motion[as]
  return (
    <M
      className={className}
      initial={{ opacity: 0, y }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '0px 0px -8% 0px' }}
      transition={{ duration: 0.9, delay, ease: [0.22, 0.7, 0.3, 1] }}
      {...rest}
    >
      {children}
    </M>
  )
}
