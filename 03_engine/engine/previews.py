from __future__ import annotations

from data import JOB_SPECIALIZATIONS


def show_job_specialization_preview(job: str) -> None:
    specializations = [
        specialization
        for specialization in JOB_SPECIALIZATIONS.values()
        if specialization.get("source_job") == job and specialization.get("status") == "preview"
    ]
    if specializations:
        print("\n職業特化預覽（目前尚未生效）")
        for specialization in specializations:
            print(f"- {specialization['name']}")
            print(f"  {specialization['summary']}")
            print(f"  定位：{specialization['identity']}")
            print(f"  效果預告：{specialization['effect_preview']}")
