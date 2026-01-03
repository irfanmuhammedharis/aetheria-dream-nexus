"""
Uvicorn wrapper with comprehensive exception logging to artifacts directory.
"""
import sys
import traceback
import uvicorn
from pathlib import Path

# Configure unbuffered output
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

artifact_dir = Path(__file__).parent.parent.parent / "test" / "artifacts" / "web_ingest_dream_flow" / "cycle-10"
artifact_dir.mkdir(parents=True, exist_ok=True)
exception_log = artifact_dir / "backend_exception_trace.log"

# Monkey-patch sys.excepthook to capture uncaught exceptions
original_excepthook = sys.excepthook

def exception_logging_hook(exc_type, exc_value, exc_traceback):
    with open(exception_log, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*80}\n")
        f.write(f"UNCAUGHT EXCEPTION: {exc_type.__name__}\n")
        f.write(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        f.write(f"\n{'='*80}\n")
    original_excepthook(exc_type, exc_value, exc_traceback)

sys.excepthook = exception_logging_hook

if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug", reload=False)
    except Exception as e:
        with open(exception_log, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"STARTUP EXCEPTION: {type(e).__name__}\n")
            f.write(traceback.format_exc())
            f.write(f"\n{'='*80}\n")
        raise
