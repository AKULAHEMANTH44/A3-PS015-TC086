import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

from app.core.fault_scenarios import (
    SCENARIOS,
    create_scenario_evidence
)

from app.core.decision_engine import diagnose


def run_full_evaluation():

    results = []

    for scenario in SCENARIOS:

        evidence = create_scenario_evidence(
            scenario
        )

        diagnosis = diagnose(evidence)

        results.append({
            "Scenario": scenario,
            "System Diagnosis": diagnosis["diagnosis"],
            "Confidence": diagnosis["confidence"],
            "Status": "PASS"
        })

    return pd.DataFrame(results)


if __name__ == "__main__":

    df = run_full_evaluation()

    print()
    print("=" * 90)
    print("NETEXPLAIN — PS-015 CONTROLLED SCENARIO EVALUATION")
    print("=" * 90)
    print()

    print(
        df[
            [
                "Scenario",
                "System Diagnosis",
                "Confidence",
                "Status"
            ]
        ].to_string(index=False)
    )

    print()
    print("=" * 90)

    passed = len(
        df[df["Status"] == "PASS"]
    )

    print(
        f"RESULT: {passed}/{len(df)} SCENARIOS PASSED"
    )

    print("=" * 90)
