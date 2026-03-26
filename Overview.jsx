export default function Overview() {
  return (
    <div>
      <div className="overview-hero">
        <div className="page-header" style={{ marginBottom: 0 }}>
          <div className="badge">Project 2305613</div>
          <h1>OTT Monetization Analysis</h1>
          <p>
            A multi-module ML dashboard powered by Random Forest models.
            Predict churn, forecast revenue, segment users, and evaluate content
            monetization potential — all in one place.
          </p>
        </div>

        <div className="model-info-grid">
          {[
            { label: 'Core Algorithm',    val: 'Random Forest' },
            { label: 'Training Samples',  val: '5,000 users' },
            { label: 'Active Predictors', val: '4 Models' },
            { label: 'Backend',           val: 'FastAPI' },
            { label: 'Frontend',          val: 'React + Vite' },
            { label: 'Deployment',        val: 'Vercel + Render' },
          ].map(i => (
            <div className="model-info-item" key={i.label}>
              <div className="mi-label">{i.label}</div>
              <div className="mi-val">{i.val}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="card-grid card-grid-2" style={{ marginBottom: 16 }}>
        {[
          { label: 'Churn Accuracy',    val: '~87%',  color: '#ef4444', desc: 'Binary classification' },
          { label: 'Revenue MAE',       val: '~₹42',  color: '#f5a623', desc: 'Monthly revenue regression' },
          { label: 'Segment Accuracy',  val: '~91%',  color: '#3ecfcf', desc: '4-class classification' },
          { label: 'Content Accuracy',  val: '~83%',  color: '#7c5cbf', desc: 'Revenue potential binary' },
        ].map(s => (
          <div className="stat-card" key={s.label}>
            <div className="stat-label">{s.label}</div>
            <div className="stat-value" style={{ color: s.color }}>{s.val}</div>
            <div className="stat-sub">{s.desc}</div>
          </div>
        ))}
      </div>

      <div className="card">
        <div className="form-section-title">Why Random Forest?</div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 16 }}>
          {[
            { title: 'Multi-Task', body: 'Works for both classification (churn, segments) and regression (revenue) — one model family covers all 4 tasks.' },
            { title: 'No Heavy Tuning', body: 'Performs well out-of-the-box on tabular OTT data. No complex hyperparameter search needed for a student project.' },
            { title: 'Interpretable', body: 'Built-in feature importance scores show which factors (watch hours, tenure, charges) drive each prediction — ideal for PPT slides.' },
          ].map(r => (
            <div key={r.title} style={{ padding: '16px', background: 'var(--surface)', borderRadius: 10, border: '1px solid var(--border)' }}>
              <div style={{ fontFamily: 'Syne', fontWeight: 700, marginBottom: 6, fontSize: 14 }}>{r.title}</div>
              <div style={{ fontSize: 13, color: 'var(--muted)', lineHeight: 1.6 }}>{r.body}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
