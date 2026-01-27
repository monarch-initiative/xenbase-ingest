# xenbase-ingest

Xenbase gene to phenotype and orthology ingests

## Setup

```bash
just setup
```

## Usage

### Download source data

```bash
just download
```

### Run transforms

```bash
# Run all transforms
just transform-all

# Run specific transform
just transform <transform_name>
```

### Run tests

```bash
just test
```

## Adding New Ingests

Use the `create-koza-ingest` Claude skill to add new ingests to this repository.

## About Xenbase

Xenbase is a web-accessible resource that integrates all the diverse biological, genomic, genotype and phenotype data available from Xenopus research.

- [Xenbase Bulk Data](http://www.xenbase.org/other/static-xenbase/ftpDatafiles.jsp)
- [Xenbase FTP](http://ftp.xenbase.org/pub/)

## Ingests

### Gene to Phenotype

This ingest is built against a one-off OBAN formatted file, which makes for a transformation which only requires adding a curie prefix and connecting column names to biolink attributes. Evidence codes are provided as ECO terms but not yet captured in the output.

**Biolink captured:**

* biolink:Gene
    * id

* biolink:PhenotypicFeature
    * id

* biolink:GeneToPhenotypicFeatureAssociation
    * id (random uuid)
    * subject (gene.id)
    * predicate (has_phenotype)
    * object (phenotypicFeature.id)
    * publications
    * aggregating_knowledge_source (["infores:monarchinitiative"])
    * primary_knowledge_source (infores:xenbase)

### Orthologs

Ortholog associations between Xenbase genes and genes from other organisms.

**Biolink captured:**

* biolink:Gene
    * id

* biolink:GeneToGeneHomologyAssociation
    * id (random uuid)
    * subject (gene.id)
    * predicate (orthologous_to)
    * object (gene.id)
    * aggregating_knowledge_source (["infores:monarchinitiative"])
    * primary_knowledge_source (infores:xenbase)

## Citation

Fisher et al. 2023, Genetics, 2023;, iyad018, doi:10.1093/genetics/iyad018

## License

BSD-3-Clause
