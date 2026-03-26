import { useState } from 'react'
import { predict } from '../api'

const DEFAULTS = {
  age: 32, monthly_charges: 399, tenure_months: 14,
  num_profiles: 2, weekly_watch_hours: 12, support_tickets: 1,
  subscription_type: 1, payment_method: 0,
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
            <div className="fi-header">
              <span>{k}</span>
              <span>{(v*100).toFixed(1)}%</span>
            </div>
            <div className="fi-bar-bg">
              <div className="fi-bar-fill" style={{ width: `${(v/max)*100}%`, background: color }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default function ChurnPredictor() {
  const [form, setForm] = useState(DEFAULTS)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const set = (k, v) => setForm(f => ({ ...f, [k]: parseFloat(v) }))

  const submit = async () => {
    setLoading(true); setError(null); setResult(null)
    try { setResult(await predict('churn', form)) }
    catch(e) { setError(e.message) }
    finally { setLoading(false) }
  }

  const riskColor = { 'High Risk': '#ef4444', 'Medium Risk': '#f59e0b', 'Low Risk': '#22c55e' }

  return (
    <div>
      <div className="page-header">
        <div className="badge" style={{ background: 'rgba(239,68,68,0.12)', borderColor: 'rgba(239,68,68,0.3)', color: '#ef4444' }}>Churn Prediction</div>
        <h1>Will This User Churn?</h1>
        <p>Enter user details to predict probability of subscription cancellation.</p>
      </div>

      <div className="card-grid card-grid-2">
        <div className="card">
          <div className="form-section-title">User Profile</div>
          <div className="form-grid">
            {[
              ['age','Age (years)','number',18,70],
              ['monthly_charges','Monthly Charges (₹)','number',99,999],
              ['tenure_months','Tenure (months)','number',1,72],
              ['num_profiles','Number of Profiles','number',1,5],
              ['weekly_watch_hours','Weekly Watch Hours','number',1,40],
              ['support_tickets','Support Tickets','number',0,20],
            ].map(([k,label,type,min,max]) => (
              <div className="form-group" key={k}>
                <label>{label}</label>
                <input type={type} min={min} max={max} value={form[k]}
                  onChange={e => set(k, e.target.value)} />
              </div>
            ))}
          </div>

          <div className="form-section-title">Subscription Details</div>
          <div className="form-grid">
            <div className="form-group">
              <label>Subscription Type</label>
              <select value={form.subscription_type} onChange={e => set('subscription_type', e.target.value)}>
                <option value={0}>Basic</option>
                <option value={1}>Standard</option>
                <option value={2}>Premium</option>
              </select>
            </div>
            <div className="form-group">
              <label>Payment Method</label>
              <select value={form.payment_method} onChange={e => set('payment_method', e.target.value)}>
                <option value={0}>Credit/Debit Card</option>
                <option value={1}>Digital Wallet</option>
                <option value={2}>Net Banking</option>
              </select>
            </div>
          </div>

          <button className="predict-btn" onClick={submit} disabled={loading}>
            {loading ? <span className="loading-dots"><span>•</span><span>•</span><span>•</span></span> : 'Predict Churn Risk →'}
          </button>
          {error && <div className="error-msg">⚠ {error} — Is the backend running?</div>}
        </div>

        <div className="card">
          {!result ? (
            <div style={{ color: 'var(--muted)', fontSize: 14, marginTop: 20, textAlign: 'center', paddingTop: 60 }}>
              <div style={{ fontSize: 40, marginBottom: 12 }}>📊</div>
              Fill in the form and hit predict to see results
            </div>
          ) : (
            <div className="result-panel" style={{ margin: 0, background: 'transparent', border: 'none', padding: 0 }}>
              <div className="result-title">Churn Probability</div>
              <div className="result-main" style={{ color: riskColor[result.risk_label] || 'var(--text)' }}>
                {(result.churn_probability * 100).toFixed(1)}%
              </div>
              <div className="result-label">
                Risk Level: <strong style={{ color: riskColor[result.risk_label] }}>{result.risk_label}</strong>
              </div>
              <FeatureImportance data={result.feature_importance} color="#ef4444" />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
