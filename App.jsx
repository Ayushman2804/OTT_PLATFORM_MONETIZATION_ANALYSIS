import { useState } from 'react'
import Overview from './components/Overview'
import ChurnPredictor from './components/ChurnPredictor'
import RevenuePredictor from './components/RevenuePredictor'
import SegmentPredictor from './components/SegmentPredictor'
import ContentPredictor from './components/ContentPredictor'

const NAV = [
  { id: 'overview',  label: 'Overview',        color: '#e63950' },
  { id: 'churn',     label: 'Churn Prediction', color: '#ef4444' },
  { id: 'revenue',   label: 'Revenue Forecast', color: '#f5a623' },
  { id: 'segment',   label: 'User Segmentation',color: '#3ecfcf' },
  { id: 'content',   label: 'Content Analysis', color: '#7c5cbf' },
]

export default function App() {
  const [page, setPage] = useState('overview')

  const pages = { overview: Overview, churn: ChurnPredictor,
                  revenue: RevenuePredictor, segment: SegmentPredictor,
                  content: ContentPredictor }
  const Page = pages[page]

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="sidebar-logo">
          <div className="logo-tag">ML Dashboard</div>
          <h2>OTT Monetization<br/>Analysis</h2>
        </div>

        <nav className="sidebar-nav">
          {NAV.map(n => (
            <button
              key={n.id}
              className={`nav-item ${page === n.id ? 'active' : ''}`}
              onClick={() => setPage(n.id)}
            >
              <span className="nav-dot" style={{ background: n.color }} />
              {n.label}
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div style={{ marginBottom: 4, fontWeight: 600, color: 'var(--text)' }}>
            Random Forest Model
          </div>
          4 predictors · scikit-learn<br/>
          FastAPI + React
        </div>
      </aside>

      <main className="main-content">
        <Page />
      </main>
    </div>
  )
}
