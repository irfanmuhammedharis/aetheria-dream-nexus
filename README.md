# Aetheria Nexus Dashboard

**10-Dimensional Psycho-Astrological Dream Analysis Platform**

A liminal terminal interface that synthesizes Jungian archetypes, Vedic astrology, Arabic hermetic traditions, and biometric data into a coherent psychological ecosystem.

## 🌙 Overview

Aetheria combines ancient wisdom traditions with modern data science to create a comprehensive dream analysis system. The platform integrates:

- **Jungian Archetypal Analysis** (Shadow-Weave)
- **Vedic Astrology** (27 Nakshatras, Vimshottari Dashas, Persian Firdaria)
- **Arabic Hermetic Lots** (Lot of Fortune, Lot of Spirit)
- **Celestial Transits** (Real-time planetary positions via Swiss Ephemeris)
- **Biometric Correlation** (HRV, sleep phase data)
- **High-Performance Visualization** (React Native Skia)

## 🏗️ Architecture

### Monorepo Structure
```
├── apps/
│   ├── backend/          # FastAPI + Swiss Ephemeris
│   │   ├── routes/       # API endpoints
│   │   └── services/     # Analysis engine, time keeper
│   ├── mobile/           # React Native CLI (Bare)
│   │   └── AetheriaMobile/
│   │       ├── src/
│   │       │   ├── components/  # PsychicAura (Skia)
│   │       │   └── screens/     # NexusDashboard
│   └── web/              # Vite + React
├── packages/
│   └── shared-schema/    # Pydantic schemas
└── test/                 # Test artifacts
```

### DecagonAnalysisObject (10 Dimensions)

1. **Shadow-Weave**: Jungian archetypal activations
2. **Celestial Transit**: Current planetary pressures
3. **Nakshatra Snapshot**: Lunar mansion analysis (27 divisions)
4. **Arabic Lots**: Hermetic fortune calculations
5. **Dasha Period**: Vedic planetary time-lords
6. **Somatic Resonance**: HRV/biometric correlations
7. **Ancestral Ghost**: Lineage patterns (optional)
8. **Collective Ripple**: Cultural zeitgeist resonance (optional)
9. **Digital Doppelganger**: AI shadow reflection (optional)
10. **Firdaria Phase**: Persian time-lord system

## 🚀 Quick Start

### Backend (FastAPI)

```bash
cd apps/backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Add your DEEPSEEK_API_KEY

# Run server
python -m uvicorn main:app --host 127.0.0.1 --port 8002
```

### Mobile (React Native)

```bash
cd apps/mobile/AetheriaMobile
yarn install

# iOS
cd ios && pod install && cd ..
yarn ios

# Android
yarn android
```

### Test DecagonAnalyzer

```bash
cd apps/backend
python test_decagon_analyzer.py
```

## 📊 API Endpoints

### POST `/api/v1/analyze`
Analyzes a dream with birth data, returns 10-dimensional analysis.

**Request:**
```json
{
  "dream_content": "I saw a black serpent in a flooded basement...",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "birth_datetime": "1990-05-15T03:30:00Z",
  "birth_latitude": 28.6139,
  "birth_longitude": 77.2090,
  "dream_datetime": "2026-01-03T06:45:00Z"
}
```

**Response:** `DecagonAnalysisObject` with all 10 analysis dimensions.

### GET `/health`
Health check endpoint.

## 🎨 Design Philosophy

**"Liminal Forge" / "Alchemical Terminal" Aesthetic**

- **Colors**: Void Black (#0A0A0B), Quicksilver (#C0C0C0), Aetherial Gold (#D4AF37)
- **Feel**: Dark, occult, high-fidelity, "creepy lab-grade terminal"
- **Visualization**: 3-layer radial graph (Nakshatras outer, Houses middle, HRV core)

## 🔬 Technical Highlights

- **Deterministic Calculations**: All astronomy via Swiss Ephemeris C-library (pyswisseph)
- **No LLM Math**: Planetary positions, Nakshatras, Dashas, Arabic Lots use pure formulas
- **Type-Safe**: Pydantic (Python), TypeScript (Mobile/Web)
- **High-Performance Graphics**: React-Native-Skia for 60fps radial visualizations

## 📦 Dependencies

### Backend
- FastAPI, Uvicorn
- pyswisseph (Swiss Ephemeris)
- Pydantic
- Redis, Pinecone (optional)

### Mobile
- React Native CLI (Bare workflow)
- @shopify/react-native-skia
- react-native-reanimated
- react-navigation

## 🧪 Testing

Follow `testdev.txt` instructions for deterministic 10-cycle test→dev loop:

```bash
# See test/test_decagon_analysis_api.txt for current test status
```

## 📄 License

MIT

## 🤝 Contributing

This is an experimental psychological/astrological research platform. Contributions welcome for:
- Additional Nakshatra deity/theme mappings
- Full Vimshottari Dasha balance calculations
- Apple HealthKit biometric integration
- Haptic feedback patterns

## 🌟 Features Implemented

✅ DecagonAnalysisObject schema (10 dimensions)  
✅ Swiss Ephemeris integration (Nakshatras, Arabic Lots, Firdaria)  
✅ Analysis engine orchestrator  
✅ FastAPI routes (`/api/v1/analyze`)  
✅ Skia-based PsychicAura visualization (3-layer radial graph)  
✅ NexusDashboard screen with mock data  
✅ Standalone DecagonAnalyzer test suite  

## 🔮 Roadmap

- [ ] Complete 27 Nakshatra deity/theme mappings
- [ ] Full Vimshottari Dasha calculation with balance
- [ ] Apple HealthKit integration
- [ ] Pinecone semantic search for collective resonance
- [ ] Real-time HRV visualization
- [ ] Haptic feedback patterns
- [ ] Redis caching layer

---

**Built with ancient wisdom and modern precision.**
