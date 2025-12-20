# run_all_tests.py
import subprocess
import sys
import os
from pathlib import Path

def main():
    test_dir = Path("Test_cases")
    if not test_dir.exists():
        print("Test_cases directory not found", file=sys.stderr)
        sys.exit(1)

    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(test_dir), "-v", "--tb=short"],
        cwd=os.getcwd()
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()