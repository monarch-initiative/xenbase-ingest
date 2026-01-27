import pytest
from non_entrez_orthologs import transform_record
from biolink_model.datamodel.pydanticmodel_v2 import GeneToGeneHomologyAssociation


@pytest.fixture
def row_with_all_ids():
    """Row with OMIM, MGI, and ZFIN IDs."""
    return {
        "Xenbase": "XB-GENE-1000023",
        "OMIM": "601496",
        "MGI": "MGI:88190",
        "ZFIN": "ZDB-GENE-030131-9442",
        "GEISHA": "",
    }


@pytest.fixture
def row_with_only_mgi():
    """Row with only MGI ID."""
    return {
        "Xenbase": "XB-GENE-1000024",
        "OMIM": "",
        "MGI": "MGI:88191",
        "ZFIN": "",
        "GEISHA": "",
    }


@pytest.fixture
def row_with_no_orthologs():
    """Row with no ortholog IDs."""
    return {
        "Xenbase": "XB-GENE-1000025",
        "OMIM": "",
        "MGI": "",
        "ZFIN": "",
        "GEISHA": "",
    }


def test_transform_produces_three_associations(row_with_all_ids):
    """Test that transform produces associations for OMIM, MGI, and ZFIN."""
    associations = transform_record(None, row_with_all_ids)

    assert len(associations) == 3

    objects = [a.object for a in associations]
    assert "OMIM:601496" in objects
    assert "MGI:MGI:88190" in objects
    assert "ZFIN:ZDB-GENE-030131-9442" in objects

    for assoc in associations:
        assert isinstance(assoc, GeneToGeneHomologyAssociation)
        assert assoc.subject == "Xenbase:XB-GENE-1000023"
        assert assoc.predicate == "biolink:orthologous_to"


def test_transform_produces_single_association(row_with_only_mgi):
    """Test that transform produces only MGI association when others are empty."""
    associations = transform_record(None, row_with_only_mgi)

    assert len(associations) == 1
    assert associations[0].object == "MGI:MGI:88191"


def test_transform_handles_no_orthologs(row_with_no_orthologs):
    """Test that transform returns empty list when no orthologs."""
    associations = transform_record(None, row_with_no_orthologs)

    assert len(associations) == 0
