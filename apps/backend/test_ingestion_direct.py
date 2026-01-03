"""
Direct import test to isolate ingestion pipeline failure point.
Artifacts saved to: test/artifacts/web_ingest_dream_flow/cycle-10/
"""
import sys
import os
import traceback
from pathlib import Path
from datetime import datetime
from uuid import UUID, uuid4

# Add repo root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

artifact_dir = Path(__file__).parent.parent.parent / "test" / "artifacts" / "web_ingest_dream_flow" / "cycle-10"
artifact_dir.mkdir(parents=True, exist_ok=True)

test_log = artifact_dir / "direct_import_test.log"

def log_output(msg):
    with open(test_log, "a", encoding="utf-8") as f:
        f.write(f"{msg}\n")
    print(msg)

log_output(f"=== Direct Import Test - {datetime.now().isoformat()} ===\n")

# Test 1: Import shared schema
try:
    from packages.shared_schema.src.schemas import DreamIngestionObject, InputModality
    log_output("[PASS] Imported DreamIngestionObject from shared_schema")
except Exception as e:
    log_output(f"[FAIL] Schema import failed:\n{traceback.format_exc()}")
    sys.exit(1)

# Test 2: Create valid DreamIngestionObject
try:
    test_dream = DreamIngestionObject(
        dream_id=uuid4(),
        user_id=UUID("550e8400-e29b-41d4-a716-446655440000"),
        timestamp_ingested=datetime.now(),
        input_modality=InputModality.TEXT,
        content_raw="Deterministic test dream content"
    )
    log_output(f"[PASS] Created DreamIngestionObject: {test_dream.dream_id}")
except Exception as e:
    log_output(f"[FAIL] DreamIngestionObject instantiation failed:\n{traceback.format_exc()}")
    sys.exit(1)

# Test 3: Import SafetySentinel
try:
    from apps.backend.src.agents.safety_sentinel import SafetySentinel
    safety_sentinel = SafetySentinel()
    log_output("[PASS] Imported and instantiated SafetySentinel")
except Exception as e:
    log_output(f"[FAIL] SafetySentinel import failed:\n{traceback.format_exc()}")
    sys.exit(1)

# Test 4: Safety validation
try:
    safety_result = safety_sentinel.validate_content(test_dream.content_raw)
    log_output(f"[PASS] Safety validation: {safety_result}")
except Exception as e:
    log_output(f"[FAIL] Safety validation failed:\n{traceback.format_exc()}")
    sys.exit(1)

# Test 5: Import PsycheOrchestrator
try:
    from apps.backend.src.agents.orchestrator import PsycheOrchestrator
    orchestrator = PsycheOrchestrator()
    log_output("[PASS] Imported and instantiated PsycheOrchestrator")
except Exception as e:
    log_output(f"[FAIL] PsycheOrchestrator import failed:\n{traceback.format_exc()}")
    sys.exit(1)

# Test 6: Call orchestrator.ingest_dream (the critical failure point)
try:
    log_output("[INFO] Calling orchestrator.ingest_dream()...")
    result = orchestrator.ingest_dream(test_dream)
    log_output(f"[PASS] Orchestrator returned result keys: {list(result.keys())}")
    log_output(f"Result preview: {str(result)[:500]}")
except Exception as e:
    log_output(f"[FAIL] orchestrator.ingest_dream() raised exception:")
    log_output(traceback.format_exc())
    log_output("\n=== CHAIN-OF-VERIFICATION ROOT CAUSE ===")
    log_output(f"Exception Type: {type(e).__name__}")
    log_output(f"Exception Message: {str(e)}")
    sys.exit(1)

log_output("\n=== ALL TESTS PASSED ===")
