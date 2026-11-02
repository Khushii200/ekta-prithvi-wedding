import { useRef, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { Minus, Plus } from 'lucide-react'
import { art } from '../lib/assets.js'
import { EVENTS, formatDate } from '../data/events.js'
import { submitRsvp, validateRsvp } from '../lib/rsvp.js'
import Reveal from './Reveal.jsx'

const EMPTY = { name: '', phone: '', guests: 1, events: [], dietary: '', message: '', website: '' }

function Field({ id, label, optional, error, children }) {
  return (
    <div className={`field ${error ? 'field--error' : ''}`}>
      <label htmlFor={id}>
        {label} {optional && <span className="field__opt">optional</span>}
      </label>
      {children}
      {error && (
        <p className="field__err" id={`${id}-err`}>
          {error}
        </p>
      )}
    </div>
  )
}

export default function RSVP() {
  const [v, setV] = useState(EMPTY)
  const [errors, setErrors] = useState({})
  const [status, setStatus] = useState('idle') // idle | sending | failed | done
  const [stored, setStored] = useState(false)
  const formRef = useRef(null)

  const set = (k) => (e) => {
    setV((s) => ({ ...s, [k]: e.target.value }))
    if (errors[k]) setErrors((x) => ({ ...x, [k]: undefined }))
  }
  const toggle = (name) => {
    setV((s) => ({ ...s, events: s.events.includes(name) ? s.events.filter((n) => n !== name) : [...s.events, name] }))
    if (errors.events) setErrors((x) => ({ ...x, events: undefined }))
  }
  const bump = (d) => setV((s) => ({ ...s, guests: Math.min(20, Math.max(1, (Number(s.guests) || 0) + d)) }))

  const onSubmit = async (e) => {
    e.preventDefault()
    if (v.website) return // filled in only by spam bots
    const errs = validateRsvp(v)
    setErrors(errs)
    if (Object.keys(errs).length) {
      const first = ['name', 'phone', 'guests', 'events'].find((k) => errs[k])
      const el = formRef.current?.querySelector(first === 'events' ? 'input[type=checkbox]' : `#rsvp-${first}`)
      el?.focus()
      return
    }
    setStatus('sending')
    try {
      const { website, ...data } = v
      const res = await submitRsvp({ ...data, guests: Number(v.guests), events: v.events })
      setStored(res.stored)
      setStatus('done')
    } catch {
      setStatus('failed')
    }
  }

  return (
    <section id="rsvp" className="rsvp">
      <Reveal className="section-head">
        <h2 className="h2">Will You Join Us?</h2>
        <p className="prose">We would love to celebrate these special moments with you.</p>
      </Reveal>

      <div className="rsvp__sheet">
        <AnimatePresence mode="wait" initial={false}>
          {status === 'done' ? (
            <motion.div
              key="thanks"
              className="thanks"
              role="status"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.4 }}
            >
              <motion.img
                src={art('seal')}
                alt=""
                className="thanks__seal"
                initial={{ scale: 1.7, opacity: 0, rotate: -10 }}
                animate={{ scale: 1, opacity: 1, rotate: 0 }}
                transition={{ type: 'spring', stiffness: 170, damping: 15, delay: 0.1 }}
              />
              <h3 className="thanks__title">Thank you, {v.name.trim().split(' ')[0]}</h3>
              {stored ? (
                <p className="prose">Your reply has reached Ekta and Prithvi. We can't wait to see you.</p>
              ) : (
                <p className="prose thanks__warn">
                  Online replies are not switched on yet, so this reply has not been saved. Please let the family know
                  directly as well.
                </p>
              )}
              <button type="button" className="link-btn" onClick={() => setStatus('idle')}>
                Change this reply
              </button>
            </motion.div>
          ) : (
            <motion.form
              key="form"
              ref={formRef}
              className="form"
              onSubmit={onSubmit}
              noValidate
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <Field id="rsvp-name" label="Guest name" error={errors.name}>
                <input id="rsvp-name" type="text" autoComplete="name" value={v.name} onChange={set('name')} aria-required="true" aria-invalid={!!errors.name} aria-describedby={errors.name ? 'rsvp-name-err' : undefined} />
              </Field>

              <div className="form__pair">
                <Field id="rsvp-phone" label="Phone number" optional error={errors.phone}>
                  <input id="rsvp-phone" type="tel" autoComplete="tel" inputMode="tel" value={v.phone} onChange={set('phone')} aria-invalid={!!errors.phone} aria-describedby={errors.phone ? 'rsvp-phone-err' : undefined} />
                </Field>
                <Field id="rsvp-guests" label="Number of guests" error={errors.guests}>
                  <div className="stepper">
                    <button type="button" onClick={() => bump(-1)} aria-label="One guest fewer">
                      <Minus size={16} strokeWidth={1.4} />
                    </button>
                    <input id="rsvp-guests" type="number" min="1" max="20" inputMode="numeric" value={v.guests} onChange={set('guests')} aria-required="true" aria-invalid={!!errors.guests} aria-describedby={errors.guests ? 'rsvp-guests-err' : undefined} />
                    <button type="button" onClick={() => bump(1)} aria-label="One guest more">
                      <Plus size={16} strokeWidth={1.4} />
                    </button>
                  </div>
                </Field>
              </div>

              <fieldset className={`choices ${errors.events ? 'field--error' : ''}`} aria-describedby={errors.events ? 'rsvp-events-err' : undefined}>
                <legend>Events attending</legend>
                <div className="choices__grid">
                  {EVENTS.map((ev) => {
                    const d = formatDate(ev.date)
                    return (
                      <label key={ev.id} className={`choice ${v.events.includes(ev.name) ? 'is-on' : ''}`}>
                        <input id={`rsvp-event-${ev.id}`} type="checkbox" checked={v.events.includes(ev.name)} onChange={() => toggle(ev.name)} />
                        <span className="choice__box" aria-hidden="true" />
                        <span className="choice__name">{ev.name}</span>
                        <span className="choice__date">{d.day} Dec</span>
                      </label>
                    )
                  })}
                </div>
                {errors.events && (
                  <p className="field__err" id="rsvp-events-err">
                    {errors.events}
                  </p>
                )}
              </fieldset>

              <Field id="rsvp-dietary" label="Dietary preferences" optional>
                <input id="rsvp-dietary" type="text" value={v.dietary} onChange={set('dietary')} />
              </Field>
              <Field id="rsvp-message" label="A message for the couple" optional>
                <textarea id="rsvp-message" rows="3" value={v.message} onChange={set('message')} />
              </Field>

              <div className="hp" aria-hidden="true">
                <label htmlFor="rsvp-website">Website</label>
                <input id="rsvp-website" type="text" tabIndex={-1} autoComplete="off" value={v.website} onChange={set('website')} />
              </div>

              {status === 'failed' && (
                <p className="form__fail" role="alert">
                  Your reply could not be sent. Check your connection and try again.
                </p>
              )}
              <button type="submit" className="btn btn--solid" disabled={status === 'sending'}>
                {status === 'sending' ? 'SENDING YOUR REPLY' : 'CONFIRM ATTENDANCE'}
              </button>
            </motion.form>
          )}
        </AnimatePresence>
      </div>
    </section>
  )
}
