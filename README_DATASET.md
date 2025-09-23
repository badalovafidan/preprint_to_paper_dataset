# PreprintToPaper dataset: connecting bioRxiv preprints with journal publications 
	
## Description
Some preprints get published, while others remain preprints without ever being formally published in a journal. The PreprintToPaper dataset is the first of its kind, as it attempts to automatically collect publication information from bioRxiv preprints and track whether submitted preprints have resulted in a publication.

The dataset generated in this study was retrieved from the bioRxiv preprint server and the Crossref metadata API in July 2024. The dataset covers two time periods: the pre-pandemic period (2016–2018) and the COVID-19 pandemic period (2020–2022). The dataset contains detailed metadata about preprints and their published versions, including **titles, authors, abstracts, institutions, submission and publication dates, licenses, and subject categories**. The metadata was processed to facilitate analysis, for example, by standardizing date formats, normalizing author names, and selecting the first and last version of each preprint.

The PreprintToPaper dataset offers diverse opportunities to study changes in titles, abstracts, and author composition over different stages of a preprint, starting from the initial submission through revision stages to the final published version.



**Main file provided:**  
- `PreprintToPaper.csv` — This is the main dataset containing all processed preprints from both time periods.


## Keywords
BioRxiv, Crossref, preprints, publications

## Paper
A paper describing this dataset is currently under preparation.

## Usage

### Data Collection
- Preprint metadata were retrieved via the bioRxiv API (https://api.biorxiv.org/details/[server]/[interval]/[cursor]/[format]).  
- Published paper metadata were retrieved via the Crossref API based on published DOI (https://api.crossref.org/works/[doi]).  

As a result, **48,300** preprint records were obtained for the 2016–2018 period and **152,869** for the 2020–2022 period.  

### Data Processing
- If both the initial and last versions of the preprint were available during the relevant period, both versions were retained. If only one version was available and it was the initial version, that version was retained. If only non-initial versions were available during the relevant period, the records were deleted. 
- Unlinked publications in bioRxiv were identified by checking preprints. The preprints were identified by checking preprints against two criteria: title similarity and author similarity. Title similarity was measured using a matching score, and only cases with a score between 0.75 and 1 were considered. For the 19,090 rows that met this threshold, an additional author match score was calculated to more accurately identify unlinked publications. 
- The dataset was categorized into 3 groups: **published, preprint only and gray zone**. See explanations below:
   - **Published:**  Preprints that were already linked on bioRxiv to a published article.
   - **Preprint Only:**  Preprints that did not have any corresponding published version and could not be linked in bioRxiv.
   - **Gray zone:** Preprints with potential matches based on title and author similarity, but without a confirmed publication DOI link. 
  

After data processing, in total, **33,687** preprints remained for the period 2016–2018, and **111,830** preprints for the period 2020–2022.  

### Final Dataset
The dataset includes **145,517** preprints, of which:  
- **90,614** were linked to journal publications,  
- **35,813** remain "Preprint Only",  
- **19,090** are "Gray Zone".  

### Summary Statistics
| Period | Gray Zone | Preprint Only | Published | Total Preprints |
|--------|-----------|---------------|-------------------|-----------------|
| **2016**   | 359       | 1,019         | 3,343             | 4,721           |
| **2017**   | 841       | 2,314         | 8,191             | 11,346          |
| **2018**   | 1,121     | 4,115         | 12,943            | 18,179          |
| **2020**   | 3,746     | 8,884         | 26,081            | 38,711          |
| **2021**   | 5,292     | 8,987         | 22,539            | 36,818          |
| **2022**   | 7,731     | 10,494        | 17,517            | 35,742          |
| **Total** | **19,090** | **35,813**        | **90,614**            | **145,517**         |

## Main Dataset Column Descriptions

| **Column Name**                          | **Description**                                                                 |
|--------------------------------------|-----------------------------------------------------------------------------|
| biorxiv_doi                          | DOI for the bioRxiv preprint                                                |
| biorxiv_title_1st                    | Preprint title – initial version                                            |
| biorxiv_title_last                   | Preprint title – last version                                               |
| biorxiv_authors_1st                  | Preprint authors – initial version                                          |
| biorxiv_authors_last                 | Preprint authors – last version                                             |
| biorxiv_author_corresponding_1st     | Corresponding author – initial version                                      |
| biorxiv_author_corresponding_last    | Corresponding author – last version                                         |
| biorxiv_author_corresponding_institution | Affiliation of corresponding author                                     |
| biorxiv_submission_date_1st          | Submission date – initial version                                           |
| biorxiv_submission_date_last         | Submission date – last version                                              |
| custom_biorxivVersion_dateDifference        | Number of days between initial and last submission                          |
| biorxiv_version_last                 | Last preprint version number (e.g., 5 if 5 versions have been submitted)                                                |
| biorxiv_type                         | Preprint type on bioRxiv (e.g., confirmatory, contradictory, new result)    |
| biorxiv_license                      | Preprint license                                                            |
| biorxiv_category                     | Subject category assigned by bioRxiv (e.g., bioinformatics, genetics)       |
| biorxiv_jatsxml                      | JATS XML structure (if available). This provides a link to the JATS XML file of the preprint. The file contains both **metadata** and **full text** of preprint.                                           |
| biorxiv_abstract_1st                 | Abstract – initial version                                                  |
| biorxiv_abstract_last                | Abstract – last version                                                     |
| biorxiv_published_doi                | DOIs of published versions of preprints. The values come from two sources: (1) DOIs directly provided by bioRxiv for preprints with an official published link, and (2) DOIs additionally identified for preprints in the gray zone, where a publication was found but not directly linked in bioRxiv.                               |
| custom_status                        | Custom classification of the preprint status: Published, Preprint Only, or Gray Zone |
| crossref_journal_name                | Journal name where the preprint was published (retrieved from Crossref)     |
| crossref_title                       | Published paper title (listed in Crossref)                                  |
| crossref_authors                     | Published paper author list from Crossref                                   |
| crossref_publication_date            | Publication date (either online publication or issue date)                  |
| crossref_publication_date_type       | Indicates whether the final date was from online publication or issue       |
| custom_submission&publication_dateDiff       | Days from preprint submission to publication       |
| author_count_diff                    | Difference in the number of authors between the bioRxiv preprint and its published version. Positive = Positive values indicate more authors, negative = negative values indicate fewer |
| title_match_score                    | Text similarity score (e.g., from SequenceMatcher) between the bioRxiv preprint title and the published article title. Only pairs with a score between 0.75 and 1.0 were considered potential matches|
| author_match_score                   | Similarity score between preprint and published author lists, used to assess how closely the authors of a preprint match those of the corresponding published paper, particularly in gray zone cases. This score helps validate whether a gray zone publication link is correct   |


---

## Additional Human-Annotated Subset

In addition to the main dataset, a human-annotated subset is provided to support the evaluation of the automatic matching procedure. This subset includes preprints with custom_status = "gray zone" and a title match score of 0.75. The score is based on the similarity between titles and ranges from 0.75 to 1. The threshold of 0.75 was chosen based on checks performed on preprints with an official publication link in bioRxiv. In these checks, the similarity between preprint titles and the titles of their published versions was calculated, and in 91% of cases the score was ≥ 0.75. The results are presented in the file PreprintToPaper_GrayZone.csv. Matches in this subset were reviewed by two annotators using abstracts and, in some cases, full texts. This subset serves as an additional dataset for assessing the accuracy of the automatic matching procedure.  

- **File name:** `PreprintToPaper_GrayZone.csv`  

## Column Descriptions

| **Column Name**           | **Description**                                                         |
|-----------------------|---------------------------------------------------------------------|
| year                  | Preprint submission year                                            |
| biorxiv_doi           | bioRxiv preprint DOI                                                |
| suspected_published_doi | Suspected DOI of the published article. Contains DOIs identified for **gray zone** preprints, where a potential published version was found but cannot be fully confirmed.                                   |
| author_match_score    | This score was used in the gray zone subset with 0.75 title match score to validate potential matches. Cases with a high author match score (close to 1) were in the majority confirmed as true matches by both annotators, while cases with a score of 0 were evaluated as non-matched.                                             |
| annotator1 / annotator2     | Labels from two annotators (`True`, `False`, `NA`)                  |

  
