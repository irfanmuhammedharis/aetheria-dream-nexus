import { useMemo, useState } from 'react'
import './App.css'

type DreamInputModality = 'text' | 'voice_transcript'

type DreamIngestionObject = {
  dream_id: string
  user_id: string
  timestamp_ingested: string
  input_modality: DreamInputModality
  content_raw: string
}

type IngestDreamResponse = {
  status?: string
  archetype?: unknown
  transits?: unknown
  narrative?: unknown
  cohort?: unknown
  engagement_trigger?: unknown
}

function makeDreamId(): string {
  if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) {
    return crypto.randomUUID()
  }
  return '00000000-0000-4000-8000-000000000000'
}

function App() {
  const apiBaseUrl = useMemo(() => {
    const env = (import.meta as any).env?.VITE_API_BASE_URL as string | undefined
    return (env && env.trim()) || 'http://localhost:8000'
  }, [])

  const [view, setView] = useState<'log' | 'analysis'>('log')
  const [dreamText, setDreamText] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<IngestDreamResponse | null>(null)

  const submitDream = async () => {
    setError(null)
    setIsSubmitting(true)

    const dream: DreamIngestionObject = {
      dream_id: makeDreamId(),
      user_id: '00000000-0000-4000-8000-000000000001',
      timestamp_ingested: new Date().toISOString(),
      input_modality: 'text',
      content_raw: dreamText,
    }

    try {
      const resp = await fetch(`${apiBaseUrl}/ingest/dream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dream),
      })

      const data = (await resp.json()) as IngestDreamResponse
      if (!resp.ok) {
        setError(typeof data === 'object' ? JSON.stringify(data) : String(data))
        return
      }

      setResult(data)
      setView('analysis')
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setIsSubmitting(false)
    }
  }

  if (view === 'analysis') {
    const archetype = result?.archetype as any
    const transits = result?.transits as any
    const narrative = result?.narrative as string

    return (
      <div className="app-container">
        <div className="hero-section">
          <div className="cosmic-orb"></div>
          <h1 className="title">✨ Dream Analysis</h1>
          <p className="subtitle">Your subconscious decoded</p>
        </div>

        <div className="content-card analysis-view">
          {archetype && (
            <div className="insight-section">
              <h2 className="section-title">🌙 Archetypal Signature</h2>
              <div className="archetype-card">
                <div className="archetype-badge">{archetype.archetype_id}</div>
                <div className="valence-bar">
                  <div 
                    className="valence-fill" 
                    style={{ width: `${((archetype.valence + 1) / 2) * 100}%` }}
                  ></div>
                </div>
                <div className="integration-status">
                  Status: <span className="status-badge">{archetype.integration_status}</span>
                </div>
              </div>
            </div>
          )}

          {narrative && (
            <div className="insight-section">
              <h2 className="section-title">📖 Narrative Synthesis</h2>
              <div className="narrative-card">
                <p className="narrative-text">{narrative}</p>
              </div>
            </div>
          )}

          {transits && transits.lunar_phase !== undefined && (
            <div className="insight-section">
              <h2 className="section-title">🌌 Celestial Context</h2>
              <div className="celestial-card">
                <div className="lunar-phase">
                  <div className="moon-icon">🌙</div>
                  <div className="phase-info">
                    <span className="phase-label">Lunar Phase</span>
                    <span className="phase-value">{(transits.lunar_phase * 100).toFixed(1)}%</span>
                  </div>
                </div>
                {transits.active_aspects?.length > 0 && (
                  <div className="aspects-count">
                    {transits.active_aspects.length} active planetary aspects detected
                  </div>
                )}
              </div>
            </div>
          )}

          <details className="raw-data-toggle">
            <summary>View Raw Analysis Data</summary>
            <pre className="raw-json">{JSON.stringify(result, null, 2)}</pre>
          </details>

          <div className="action-buttons">
            <button className="btn btn-secondary" onClick={() => setView('log')}>
              ← Back
            </button>
            <button 
              className="btn btn-primary" 
              onClick={() => {
                setDreamText('')
                setResult(null)
                setView('log')
              }}
            >
              New Dream →
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="app-container">
      <div className="hero-section">
        <div className="cosmic-orb"></div>
        <h1 className="title">🌌 Aetheria Dream Journal</h1>
        <p className="subtitle">Unlock the wisdom hidden in your dreams</p>
      </div>

      <div className="content-card">
        <label className="input-label">
          <span className="label-text">Describe Your Dream</span>
          <span className="label-hint">Write freely—every detail matters</span>
        </label>
        
        <textarea
          value={dreamText}
          onChange={(e) => setDreamText(e.target.value)}
          rows={12}
          placeholder="I was standing in a vast field under a starlit sky...\n\nDescribe the setting, emotions, symbols, people, and any significant moments."
          className="dream-input"
        />

        <div className="character-count">
          {dreamText.length} characters
        </div>

        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            <div>
              <strong>Error:</strong> {error}
            </div>
          </div>
        )}

        <button 
          onClick={submitDream} 
          disabled={isSubmitting || !dreamText.trim()}
          className={`btn btn-primary btn-large ${isSubmitting ? 'btn-loading' : ''}`}
        >
          {isSubmitting ? (
            <>
              <span className="spinner"></span>
              Analyzing...
            </>
          ) : (
            <>
              Analyze Dream ✨
            </>
          )}
        </button>

        <div className="api-footer">
          <code className="api-badge">{apiBaseUrl}</code>
        </div>
      </div>
    </div>
  )
}

export default App
