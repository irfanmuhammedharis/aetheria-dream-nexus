# Aetheria Directory Structure

## Overview
This document outlines the directory structure for the Aetheria project, following the Separation of Concerns principle as defined in Section 2 of doc.md. The structure implements the Agents-as-Tools pattern with clear boundaries between mobile frontend, backend services, and shared schemas.

## Root Structure
```
aetheria/
├── apps/
│   ├── backend/          # Python FastAPI backend (W-01 to W-06 agents)
│   └── mobile/           # React Native CLI (Bare) frontend
├── packages/
│   └── shared-schema/    # Cross-platform schemas (Python & TypeScript)
├── docs/                 # Documentation and specifications
└── infrastructure/       # Docker, deployment configs
```

## Backend Structure (apps/backend)
```
apps/backend/
├── src/
│   ├── agents/           # Worker agents (W-01 to W-06)
│   │   ├── orchestrator.py      # W-01: Psyche_Orchestrator
│   │   ├── jungian_decoder.py   # W-02: Shadow Weaver
│   │   ├── celestial_engine.py  # W-03: Time Keeper
│   │   ├── resonance_librarian.py # W-04: Search Worker
│   │   ├── safety_sentinel.py   # W-05: Guard
│   │   └── growth_architect.py  # W-06: Growth Agent
│   ├── core/             # Core services
│   │   ├── context_registry.py  # Context management
│   │   ├── event_ingestor.py    # CloudEvents handling
│   │   └── vector_store.py      # Pinecone integration
│   ├── api/              # FastAPI routes
│   │   ├── routes/
│   │   │   ├── dreams.py
│   │   │   ├── analysis.py
│   │   │   └── health.py
│   │   └── dependencies.py
│   ├── models/           # Pydantic models
│   ├── services/         # Business logic
│   └── utils/            # Utilities
├── tests/                # Unit and integration tests
├── alembic/              # Database migrations
├── requirements.txt      # Python dependencies
├── Dockerfile            # Backend container
└── main.py               # Application entry point
```

## Mobile Structure (apps/mobile)
```
apps/mobile/
├── android/              # Android native code
├── ios/                  # iOS native code
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── ShadowTapestry.tsx
│   │   ├── ResonanceMap.tsx
│   │   └── AudioPlayer.tsx
│   ├── screens/          # Screen components
│   │   ├── DreamLogScreen.tsx
│   │   ├── AnalysisScreen.tsx
│   │   └── OnboardingScreen.tsx
│   ├── navigation/       # React Navigation setup
│   ├── services/         # API clients, local storage
│   ├── hooks/            # Custom React hooks
│   ├── utils/            # Utilities
│   └── types/            # TypeScript type definitions
├── assets/               # Images, fonts, audio
├── package.json
├── metro.config.js
├── babel.config.js
├── tsconfig.json
└── index.js
```

## Shared Schema Structure (packages/shared-schema)
```
packages/shared-schema/
├── src/
│   ├── schemas.py        # Python Pydantic models
│   ├── schemas.ts        # TypeScript interfaces/Zod schemas
│   └── index.ts          # TypeScript exports
├── tests/
├── package.json          # For TypeScript compilation
└── pyproject.toml        # For Python packaging
```

## Infrastructure Structure (infrastructure)
```
infrastructure/
├── docker/
│   ├── backend.Dockerfile
│   ├── mobile.Dockerfile
│   └── docker-compose.yml
├── k8s/                  # Kubernetes manifests
├── terraform/            # Infrastructure as Code
└── ci-cd/                # GitHub Actions, etc.
```

## Verification Log
- Verified against Section 2.1 (Worker Roles) and Section 5.1 (Agent Graph) of doc.md for agent separation.
- Verified against Section 1.2 (Architectural Principles) for Separation of Concerns.
- Verified against Section 7 (Implementation Roadmap) for phase-based structure.
- Assumption: Added tests/, assets/, and infrastructure/ directories as they are implied by modern development practices but not explicitly detailed in doc.md.</content>
<parameter name="filePath">d:\react native\dream talk\directory_structure.md