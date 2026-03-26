import { useState } from 'react'
import { predict } from '../api'

const DEFAULTS = {
  genre_action:1, genre_drama:0, genre_comedy:0, genre_documentary:0,
  avg_rating:7.5, release_year:2023, duration_minutes:120,
  language_hindi:1, language_english:0,
}

export default function ContentPredictor() {
  const [form, setForm] = useState(DEFAULTS)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const set = (k,v) => setForm(f => ({...f,[k]:parseFloat(v)}))
  const toggle = (k) => setForm(f => ({...f,[k]: f[k]===1?0:1}))

  const submit = async () => {
    setLoading(true); setError(null); setResult(null)
    try { setResult(await predict('content', form)) }
    catch(e) { setError(e.message) }
    finally { setLoading(false) }
  }

  const labelColor = { 'High Revenue':'#22c55e', 'Medium Revenue':'#f59e0b', 'Low Revenue':'#ef4444' }

  return (
    <div>
      <div className="page-header">
        <div className="badge" style={{ background:'rgba(124,92,191,0.12)', borderColor:'rgba(124,92,191,0.3)', color:'#7c5cbf' }}>Content Analysis</div>
        <h1>Content Revenue Potential</h1>
        <p>Predict whether a piece of content will drive high, medium, or low ad/subscription revenue.</p>
      </div>

      <div className="card-grid card-grid-2">
        <div className="card">
          <div className="form-section-title">Content Metadata</div>
          <div className="form-grid">
            <div className="form-group">
              <label>Average Rating (1–10)</label>
              <input type="number" min={1} max={10} step={0.1} value={form.avg_rating} onChange={e=>set('avg_rating',e.target.value)} />
            </div>
            <div className="form-group">
              <label>Release Year</label>
              <input type="number" min={2010} max={2025} value={form.release_year} onChange={e=>set('release_year',e.target.value)} />
            </div>
            <div className="form-group">
              <label>Duration (minutes)</label>
              <input type="number" min={10} max={300} value={form.duration_minutes} onChange={e=>set('duration_minutes',e.target.value)} />
            </div>
          </div>

          <div className="form-section-title">Genres</div>
          <div style={{ display:'flex', gap:10, flexWrap:'wrap', marginBottom:20 }}>
            {['genre_action','genre_drama','genre_comedy','genre_documentary'].map(g => (
              <button key={g}
                onClick={() => toggle(g)}
                style={{
                  padding:'8px 16px', borderRadius:20, border:'1px solid',
                  borderColor: form[g] ? '#7c5cbf' : 'var(--border)',
                  background: form[g] ? 'rgba(124,92,191,0.2)' : 'var(--surface)',
                  color: form[g] ? '#c4b0f0' : 'var(--muted)',
                  fontSize:13, fontWeight:600, cursor:'pointer', transition:'all 0.15s'
                }}>
                {g.replace('genre_','').charAt(0).toUpperCase()+g.replace('genre_','').slice(1)}
              </button>
            ))}
          </div>

          <div className="form-section-title">Language</div>
          <div style={{ display:'flex', gap:10, marginBottom:20 }}>
            {['language_hindi','language_english'].map(l => (
              <button key={l}
                onClick={() => toggle(l)}
                style={{
                  padding:'8px 16px', borderRadius:20, border:'1px solid',
                  borderColor: form[l] ? '#7c5cbf' : 'var(--border)',
                  background: form[l] ? 'rgba(124,92,191,0.2)' : 'var(--surface)',
                  color: form[l] ? '#c4b0f0' : 'var(--muted)',
                  fontSize:13, fontWeight:600, cursor:'pointer', transition:'all 0.15s'
                }}>
                {l.replace('language_','').charAt(0).toUpperCase()+l.replace('language_','').slice(1)}
              </button>
            ))}
          </div>

          <button className="predict-btn" style={{ background:'#7c5cbf' }} onClick={submit} disabled={loading}>
            {loading ? <span className="loading-dots"><span>•</span><span>•</span><span>•</span></span> : 'Analyse Content →'}
          </button>
          {error && <div className="error-msg">⚠ {error} — Is the backend running?</div>}
        </div>

        <div className="card">
          {!result ? (
            <div style={{ color:'var(--muted)', fontSize:14, textAlign:'center', paddingTop:60 }}>
              <div style={{ fontSize:40, marginBottom:12 }}>📺</div>
              Configure content and analyse revenue potential
            </div>
          ) : (
            <div>
              <div className="result-title">Revenue Potential Score</div>
              <div className="result-main" style={{ color: labelColor[result.label] }}>
                {(result.revenue_potential * 100).toFixed(1)}%
              </div>
              <div className="result-label">
                Prediction: <strong style={{ color: labelColor[result.label] }}>{result.label}</strong>
              </div>

              <div style={{ marginTop:28 }}>
                <div className="result-title">Confidence Meter</div>
                <div style={{ height:12, background:'var(--border)', borderRadius:6, overflow:'hidden', marginTop:8 }}>
                  <div style={{
                    height:'100%', borderRadius:6, transition:'width 0.7s',
                    width:`${result.revenue_potential*100}%`,
                    background:`linear-gradient(90deg, #7c5cbf, ${labelColor[result.label]})`,
                  }} />
                </div>
                <div style={{ display:'flex', justifyContent:'space-between', fontSize:11, color:'var(--muted)', marginTop:4 }}>
                  <span>Low</span><span>Medium</span><span>High</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
