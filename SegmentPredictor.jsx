import { useState } from 'react'
import { predict } from '../api'

const DEFAULTS = {
  age: 25, weekly_watch_hours: 20, monthly_charges: 299,
  tenure_months: 10, num_profiles: 2, device_count: 2,
  content_categories_watched: 6, support_tickets: 0,
}

const SEG_COLORS = ['#ef4444','#f5a623','#3ecfcf','#7c5cbf']
const SEG_DESC = {
  'Casual Viewer':    'Low engagement, may downgrade. Target with retention offers.',
  'Power User':       'High engagement. Prime candidate for premium upsell.',
  'At-Risk User':     'Medium engagement but declining. Needs re-engagement campaigns.',
  'Premium Loyalist': 'High value, long tenure. Ideal brand ambassador.',
}

export default function SegmentPredictor() {
  const [form, setForm] = useState(DEFAULTS)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const set = (k,v) => setForm(f => ({...f,[k]:parseFloat(v)}))

  const submit = async () => {
    setLoading(true); setError(null); setResult(null)
    try { setResult(await predict('segment', form)) }
    catch(e) { setError(e.message) }
    finally { setLoading(false) }
  }

  return (
    <div>
      <div className="page-header">
        <div className="badge" style={{ background:'rgba(62,207,207,0.12)', borderColor:'rgba(62,207,207,0.3)', color:'#3ecfcf' }}>User Segmentation</div>
        <h1>User Segment Classifier</h1>
        <p>Classify a user into one of 4 monetization segments for targeted campaigns.</p>
      </div>

      <div className="card-grid card-grid-2">
        <div className="card">
          <div className="form-section-title">User Behaviour</div>
          <div className="form-grid">
            {[
              ['age','Age',18,70],
              ['weekly_watch_hours','Weekly Watch Hours',1,40],
              ['monthly_charges','Monthly Charges (₹)',99,999],
              ['tenure_months','Tenure (months)',1,72],
              ['num_profiles','Profiles',1,5],
              ['device_count','Devices',1,5],
              ['content_categories_watched','Content Categories',1,10],
              ['support_tickets','Support Tickets',0,20],
            ].map(([k,label,min,max]) => (
              <div className="form-group" key={k}>
                <label>{label}</label>
                <input type="number" min={min} max={max} value={form[k]} onChange={e=>set(k,e.target.value)} />
              </div>
            ))}
          </div>

          <button className="predict-btn" style={{ background:'#3ecfcf', color:'#080c14' }} onClick={submit} disabled={loading}>
            {loading ? <span className="loading-dots"><span>•</span><span>•</span><span>•</span></span> : 'Classify Segment →'}
          </button>
          {error && <div className="error-msg">⚠ {error} — Is the backend running?</div>}
        </div>

        <div className="card">
          {!result ? (
            <div style={{ color:'var(--muted)', fontSize:14, textAlign:'center', paddingTop:60 }}>
              <div style={{ fontSize:40, marginBottom:12 }}>👥</div>
              Classify the user to see their segment
            </div>
          ) : (
            <div>
              <div className="result-title">Predicted Segment</div>
              <div className="result-main" style={{ color: SEG_COLORS[result.segment_id], fontSize:32 }}>
                {result.segment_name}
              </div>
              <div className="result-label" style={{ marginBottom:8 }}>
                {SEG_DESC[result.segment_name]}
              </div>

              <div className="result-title" style={{ marginTop:24 }}>Segment Probabilities</div>
              <div className="seg-dist">
                {Object.entries(result.segment_distribution).map(([name, prob], i) => (
                  <div className="seg-row" key={name}>
                    <span className="seg-name" style={{ fontSize:12 }}>{name}</span>
                    <div className="seg-bar-bg">
                      <div className="seg-bar-fill" style={{ width:`${prob*100}%`, background: SEG_COLORS[i] }} />
                    </div>
                    <span className="seg-pct">{(prob*100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
