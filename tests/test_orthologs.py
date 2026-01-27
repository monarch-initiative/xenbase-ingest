import pytest
from unittest.mock import MagicMock
from orthologs import transform_record
from biolink_model.datamodel.pydanticmodel_v2 import GeneToGeneHomologyAssociation


@pytest.fixture
def sample_row():
    """Sample row from xenbase ortholog data."""
    return {
        "entrez_id": "5594",
        "xb_genepage_id": "XB-GENEPAGE-478047",
        "xb_gene_symbol": "mapk1",
        "xb_gene_name": "mitogen-activated protein kinase 1",
    }


@pytest.fixture
def mock_koza_transform():
    """Mock koza_transform with lookup function."""
    mock = MagicMock()
    # Simulate the genepage-2-gene mapping returning specific gene IDs
    def lookup_side_effect(genepage_id, field, map_name):
        if map_name == 'genepage-2-gene':
            if field == 'tropicalis_id':
                return 'XB-GENE-478048'
            elif field == 'laevis_l_id':
                return 'XB-GENE-6252539'
            elif field == 'laevis_s_id':
                return 'XB-GENE-17340263'
        return None
    mock.lookup = MagicMock(side_effect=lookup_side_effect)
    return mock


def test_transform_produces_associations(sample_row, mock_koza_transform):
    """Test that transform produces orthology associations."""
    associations = transform_record(mock_koza_transform, sample_row)

    # Should produce 3 associations (one per gene ID from mapping)
    assert len(associations) == 3

    for assoc in associations:
        assert isinstance(assoc, GeneToGeneHomologyAssociation)
        assert assoc.predicate == "biolink:orthologous_to"
        assert assoc.object == "NCBIGene:5594"
        assert assoc.primary_knowledge_source == "infores:xenbase"


def test_transform_fallback_to_genepage(sample_row):
    """Test fallback to genepage_id when no mapping found."""
    mock_transform = MagicMock()
    mock_transform.lookup = MagicMock(return_value=None)

    associations = transform_record(mock_transform, sample_row)

    # Should produce 1 association with genepage_id as fallback
    assert len(associations) == 1
    assert associations[0].subject == "Xenbase:XB-GENEPAGE-478047"
