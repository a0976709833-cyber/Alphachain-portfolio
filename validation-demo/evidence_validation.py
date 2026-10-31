"""Standalone, synthetic data-validation portfolio example.

This is NOT a copy of AlphaChain production code or a working research engine.
"""

from datetime import date
from typing import Literal

from pydantic import BaseModel, field_validator, model_validator


class EvidenceRecord(BaseModel):
    """Validate the shape and basic consistency of a sample evidence record."""

    record_id: str
    source_company_id: str
    target_company_id: str
    source_title: str
    stance: Literal["supporting", "counter"]
    source_date: date | None = None
    retrieved_at: date

    @field_validator(
        "record_id", "source_company_id", "target_company_id", "source_title"
    )
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("required text must not be blank")
        return value.strip()

    @model_validator(mode="after")
    def validate_consistency(self) -> "EvidenceRecord":
        if self.source_company_id == self.target_company_id:
            raise ValueError("source and target companies must be different")
        if self.source_date is not None and self.source_date > self.retrieved_at:
            raise ValueError("source_date cannot be later than retrieved_at")
        return self


def example_record() -> dict:
    """Return invented IDs and a fictitious document title for this demo."""
    return {
        "record_id": "DEMO-001",
        "source_company_id": "COMPANY-A",
        "target_company_id": "COMPANY-B",
        "source_title": "Fictional supplier announcement (demo only)",
        "stance": "supporting",
        "source_date": "2026-01-05",
        "retrieved_at": "2026-01-10",
    }


if __name__ == "__main__":
    from pydantic import ValidationError

    sample = example_record()
    try:
        record = EvidenceRecord.model_validate(sample)
        print(f"PASS: {record.record_id} accepted")
    except ValidationError as exc:
        print(f"FAIL: Unexpected error: {exc}")
        raise

    invalid = {**sample, "target_company_id": "COMPANY-A"}
    try:
        EvidenceRecord.model_validate(invalid)
    except ValidationError:
        print("PASS: Same-company relationship rejected")
    else:
        raise AssertionError("Same-company relationship was not rejected")
