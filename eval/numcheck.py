"""Re-export of src/summary_numbers.py (the number check moved to src/ so the agent and workflow can use it before accepting a summary)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from summary_numbers import *  # noqa: E402,F401,F403
from summary_numbers import _matches  # noqa: E402,F401

if __name__ == "__main__":
    import summary_numbers
    summary_numbers.__dict__  # noqa: B018
    print("numcheck re-export ok")
