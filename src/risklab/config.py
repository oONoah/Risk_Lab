from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATA_RAW = ROOT / "data" / "raw"    
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_SIMULATED = ROOT / "data" / "simulated"

RESULTS = ROOT / "results"