import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

spec = importlib.util.spec_from_file_location("enrichment", ROOT / "enrichment.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_source_facts_are_preserved_when_provided():
    record = {
        "pets_allowed": False,
        "security_deposit": 1800,
        "available_date": "2026-11-01",
        "lease_terms": ["12 months"],
        "minimum_lease_months": 12,
        "description": "Original listing text with no fabricated claims.",
    }

    enriched = module.rule_based_enrich(record)

    assert enriched["pets_allowed"] is False
    assert enriched["security_deposit"] == 1800
    assert enriched["available_date"] == "2026-11-01"
    assert enriched["lease_terms"] == ["12 months"]
    assert enriched["minimum_lease_months"] == 12


def test_source_values_are_not_forced_to_defaults_in_pipeline_enrichment():
    record = {
        "pets_allowed": False,
        "security_deposit": 2200,
        "available_date": "2026-12-01",
        "lease_terms": ["6 months"],
        "minimum_lease_months": 6,
        "description": "Original listing copy preserving factual source details.",
    }

    enriched, _ = module.apply_enrichment_pipeline([record])

    assert enriched[0]["pets_allowed"] is False
    assert enriched[0]["security_deposit"] == 2200
    assert enriched[0]["available_date"] == "2026-12-01"
    assert enriched[0]["lease_terms"] == ["6 months"]
    assert enriched[0]["minimum_lease_months"] == 6
