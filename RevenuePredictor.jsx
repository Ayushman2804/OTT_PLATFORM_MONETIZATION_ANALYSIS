import { useState } from 'react'
import { predict } from '../api'

const DEFAULTS = {
  age: 28, tenure_months: 18, weekly_watch_hours: 15,
  num_profiles: 3, subscription_type: 1,
  content_categories_watched: 5, device_count: 2,
}

function FeatureImportance({ data, color }) {
  if (!data) return null
  const max = Math.max(...Object.values(data))
  return (
    <div>
      <div className="result-title" style={{ marginTop: 20 }}>Feature Importance</div>
      <div className="fi-list">
        {Object.entries(data).sort((a,b) => b[1]-a[1]).map(([k,v]) => (
          <div className="fi-item" key={k}>
            <div className="fi-header"><span>{k}</span><span>{(v*100).toFixed(1)}%</span></div>
            <div className="fi-bar-bg">
              <div className="fi-bar-fill" style={{ width:`${(v/max)*100}%`, background: color }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default function RevenuePredictor() {
  const [form, setForm] = useState(DEFAULTS)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const set = (k,v) => setForm(f => ({...f,[k]:parseFloat(v)}))

  const submit = async () => {
    setLoading(true); setError(null); setResult(null)
    try { setResult(await predict('revenue', form)) }
    catch(e) { setError(e.message) }
    finally { setLoading(false) }
  }

  return (
    <div>
      <div className="page-header">
        <div className="badge" style={{ background:'rgba(245,166,35,0.12)', borderColor:'rgba(245,166,35,0.3)', color:'#f5a623' }}>Revenue Forecast</div>
        <h1>Monthly Revenue Prediction</h1>
        <p>Forecast expected monthly revenue contribution from a user based on their profile.</p>
      </div>

      <div className="card-grid card-grid-2">
        <div className="card">
          <div className="form-section-title">User Details</div>
          <div className="form-grid">
            {[
              ['age','Age (years)',18,70],
              ['tenure_months','Tenure (months)',1,72],
              ['weekly_watch_hours','Weekly Watch Hours',1,40],
              ['num_profiles','Number of Profiles',1,5],
              ['content_categories_watched','Content Categories',1,10],
              ['device_count','Device Count',1,5],
            ].map(([k,label,min,max]) => (
              <div className="form-group" key={k}>
                <label>{label}</label>
                <input type="number" min={min} max={max} value={form[k]} onChange={e=>set(k,e.target.value)} />
              </div>
            ))}
          </div>

          <div className="form-group" style={{ marginBottom: 20 }}>
            <label>Subscription Type</label>
            <select value={form.subscription_type} onChange={e=>set('subscription_type',e.target.value)}>
              <option value={0}>Basic (₹99/mo)</option>
              <option value={1}>Standard (₹299/mo)</option>
              <option value={2}>Premium (₹599/mo)</option>
            </select>
          </div>

          <button className="predict-btn" style={{ background:'#f5a623' }} onClick={submit} disabled={loading}>
            {loading ? <span className="loading-dots"><span>•</span><span>•</span><span>•</span></span> : 'Forecast Revenue →'}
          </button>
          {error && <div className="error-msg">⚠ {error} — Is the backend running?</div>}
        </div>

        <div className="card">
          {!result ? (
            <div style={{ color:'var(--muted)', fontSize:14, textAlign:'center', paddingTop:60 }}>
              <div style={{ fontSize:40, marginBottom:12 }}>💰</div>
              Fill in the form to see revenue forecast
            </div>
          ) : (
            <div style={{ padding:0 }}>
              <div className="result-title">Predicted Monthly Revenue</div>
              <div className="result-main" style={{ color:'#f5a623' }}>
                ₹{result.predicted_monthly_revenue.toLocaleString()}
              </div>
              <div className="result-label">Estimated contribution per month</div>
              <FeatureImportance data={result.feature_importance} color="#f5a623" />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
