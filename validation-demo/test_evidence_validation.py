"""Unit tests using only synthetic records."""

from datetime import date

import pytest
from pydantic import ValidationError

from evidence_validation import EvidenceRecord, example_record


def test_valid_record_is_accepted():
    record = EvidenceRecord.model_validate(example_record())
    assert record.record_id == "DEMO-001"
    assert record.source_date == date(2026, 1, 5)


def test_missing_optional_source_date_is_accepted():
    sample = example_record()
    sample.pop("source_date")
    assert EvidenceRecord.model_validate(sample).source_date is None


@pytest.mark.parametrize("field", ["record_id", "source_company_id", "source_title"])
def test_blank_required_text_is_rejected(field):
    sample = example_record()
    sample[field] = "   "
    with pytest.raises(ValidationError):
        EvidenceRecord.model_validate(sample)


def test_same_company_is_rejected():
    sample = example_record()
    sample["target_company_id"] = sample["source_company_id"]
    with pytest.raises(ValidationError, match="must be different"):
        EvidenceRecord.model_validate(sample)


def test_future_source_date_is_rejected():
    sample = example_record()
    sample["source_date"] = "2026-01-11"
    with pytest.raises(ValidationError, match="later than retrieved_at"):
        EvidenceRecord.model_validate(sample)


def test_invalid_stance_is_rejected():
    sample = example_record()
    sample["stance"] = "unknown"
    with pytest.raises(ValidationError):
        EvidenceRecord.model_validate(sample)


def test_missing_required_field_is_rejected():
    sample = example_record()
    sample.pop("retrieved_at")
    with pytest.raises(ValidationError):
        EvidenceRecord.model_validate(sample)


def test_text_is_trimmed():
    sample = example_record()
    sample["record_id"] = "  DEMO-001  "
    assert EvidenceRecord.model_validate(sample).record_id == "DEMO-001"
