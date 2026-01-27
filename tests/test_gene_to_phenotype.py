import pytest
from gene_to_phenotype import transform_record
from biolink_model.datamodel.pydanticmodel_v2 import (
    Gene,
    PhenotypicFeature,
    GeneToPhenotypicFeatureAssociation,
)


@pytest.fixture
def sample_row():
    """Sample row from xenbase gene-to-phenotype data."""
    return {
        "SUBJECT": "Xenbase:XB-GENE-1000023",
        "SUBJECT_LABEL": "aacs",
        "SUBJECT_TAXON": "NCBITaxon:8364",
        "SUBJECT_TAXON_LABEL": "Xenopus tropicalis",
        "OBJECT": "XPO:0102825",
        "OBJECT_LABEL": "abnormal cellular component organization in the whole organism",
        "RELATION": "RO:0002200",
        "RELATION_LABEL": "has phenotype",
        "EVIDENCE": "ECO:0000269",
        "EVIDENCE_LABEL": "experimental evidence used in manual assertion",
        "SOURCE": "PMID:12345678",
        "IS_DEFINED_BY": "xenbase",
        "QUALIFIER": "",
    }


@pytest.fixture
def row_without_source():
    """Row without publication source."""
    return {
        "SUBJECT": "Xenbase:XB-GENE-1000023",
        "SUBJECT_LABEL": "aacs",
        "SUBJECT_TAXON": "NCBITaxon:8364",
        "SUBJECT_TAXON_LABEL": "Xenopus tropicalis",
        "OBJECT": "XPO:0102825",
        "OBJECT_LABEL": "abnormal phenotype",
        "RELATION": "RO:0002200",
        "RELATION_LABEL": "has phenotype",
        "EVIDENCE": "ECO:0000269",
        "EVIDENCE_LABEL": "experimental evidence",
        "SOURCE": "",
        "IS_DEFINED_BY": "xenbase",
        "QUALIFIER": "",
    }


def test_transform_produces_three_entities(sample_row):
    """Test that transform produces gene, phenotype, and association."""
    entities = transform_record(None, sample_row)

    assert len(entities) == 3

    gene = entities[0]
    assert isinstance(gene, Gene)
    assert gene.id == "Xenbase:XB-GENE-1000023"
    assert "infores:xenbase" in gene.provided_by

    phenotype = entities[1]
    assert isinstance(phenotype, PhenotypicFeature)
    assert phenotype.id == "XPO:0102825"

    association = entities[2]
    assert isinstance(association, GeneToPhenotypicFeatureAssociation)
    assert association.subject == gene.id
    assert association.object == phenotype.id
    assert association.predicate == "biolink:has_phenotype"
    assert association.publications == ["PMID:12345678"]
    assert association.primary_knowledge_source == "infores:xenbase"


def test_transform_handles_missing_source(row_without_source):
    """Test that transform handles rows without publication source."""
    entities = transform_record(None, row_without_source)

    association = entities[2]
    assert association.publications is None


def test_transform_raises_on_qualifier(sample_row):
    """Test that transform raises if qualifier is present."""
    sample_row["QUALIFIER"] = "some_qualifier"

    with pytest.raises(ValueError, match="Didn't expect a qualifier"):
        transform_record(None, sample_row)
