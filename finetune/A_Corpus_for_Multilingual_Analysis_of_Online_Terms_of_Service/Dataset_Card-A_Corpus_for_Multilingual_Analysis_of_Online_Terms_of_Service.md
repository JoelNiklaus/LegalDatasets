---
TODO: Add YAML tags here. Copy-paste the tags obtained with the online tagging app: https://huggingface.co/spaces/huggingface/datasets-tagging
---

# Dataset Card for A Corpus for Multilingual Analysis of Online Terms of Service

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:**
- **Repository:** claudette.eui.eu/corpus_multilingual_NLLP2021.zip
- **Paper:** Drawzeski, K., Galassi, A., Jablonowska, A., Lagioia, F., Lippi, M., Micklitz, H. W., Sartor, G., Tagiuri, G., & Torroni, P. (2021). A Corpus for Multilingual Analysis of Online Terms of Service. Proceedings of the Natural Legal Language Processing Workshop 2021, 1–8. https://doi.org/10.18653/v1/2021.nllp-1.1
- **Leaderboard:**
- **Point of Contact:** [Joel Niklaus](joel.niklaus.2@bfh.ch)

### Dataset Summary

*"We present the first annotated corpus for multilingual analysis of potentially unfair clauses in online Terms of Service [=ToS]. The data set comprises a total of 100 contracts, obtained from 25 documents annotated in four different languages: English, German, Italian, and Polish. For each contract, potentially unfair clauses for the consumer are annotated, for nine different unfairness categories. We show how a simple yet efficient annotation projection technique based on sentence embeddings could be used to automatically transfer annotations across languages."* (Drawzeski et al., 2021)

### Supported Tasks and Leaderboards

The dataset can be used for multi-label text classification tasks, more specifically, for classifying unfair clauses in ToS. 

### Languages

English, German, Italian, and Polish.

## Dataset Structure

### Data Instances

The dataset contains two main folders: `original_text` and `original_xml`. Each folder contains the subfolder `de`(=German), `en`(=English), `it`(=Italian), `pl`(=Polish); each of them containing documents with the ToS for the following Services: *Booking, Dropbo, Electronic_Arts, Evernote, Facebook, Garmin, Google, Grindr, Linkedin, Mozilla, Pinterest, Quora, Ryanair, Skype, Skyscanner, Snap, Spotify, Terravision, Tinder, Tripadvisor, Tumblr, Uber, Weebly, Yelp, Zynga*. The `original_text` folder contains txt files the and `original_xml` folder contains annotated xml files. 

### Data Fields

The xml files in the folder `original_xml` have been annotated using nine tags that represent different categories of clause unfairness. These tags are:
-	`<a>` = Arbitration: *”This clause requires or allows the parties to resolve their disputes through an arbitration process, before the case could go to court. It is therefore considered a kind of forum selection clause. However, such a clause may or may not specify that arbitration should occur within a specific jurisdiction. Clauses stipulating that the arbitration should (1) take place in a state other than the state of consumer’s residence and/or (2) be based not on law but on arbiter’s discretion were marked as clearly unfair.”* (Lippi et al., 2019)
- `<ch>` = Unilateral change: *"This clause specifies the conditions under which the service provider could amend and modify the terms of service and/or the service itself. Such clauses were always considered as potentially unfair. This is because the ECJ has not yet issued a judgment in this regard, though the Annex to the Direc- tive contains several examples supporting such a qualification."* (Lippi et al., 2019)
- `<cr>` = Content removal : *"This gives the provider a right to modify/delete user’s content, including in-app purchases, and sometimes specifies the conditions under which the service provider may do so. As in the case of unilateral termination, clauses that indicate conditions for content removal were marked as potentially unfair, whereas clauses stipulating that the service provider may remove content in his full discretion, and/or at any time for any or no reasons and/or without notice nor possibility to retrieve the content were marked as clearly unfair."* (Lippi et al., 2019)
- `<j>` = Jurisdiction : *"This type of clause stipulates what courts will have the competence to adjudicate disputes under the contract. Jurisdiction clauses giving consumers a right to bring disputes in their place of residence were marked as clearly fair, whereas clauses stating that any judicial proceeding takes a residence away (i.e. in a different city, different country) were marked as clearly unfair. This assessment is grounded in ECJ’s case law, see for example Oceano case number C-240/98."* (Lippi et al., 2019)
- `<law>` = Choice of law: *"This clause specifies what law will govern the contract, meaning also what law will be applied in potential adjudication of a dispute arising under the contract. Clauses defining the applicable law as the law of the consum- er’s country of residence were marked as clearly fair [...]"* (Lippi et al., 2019)
- `<ltd>` = Limitation of liability: *"This clause stipulates that the duty to pay damages is limited or excluded, for certain kinds of losses and under certain conditions. Clauses that explicitly affirm non-excludable providers’ liabilities were marked as clearly fair."* (Lippi et al., 2019)
-	`<ter>` = Unilateral termination:  *"This clause gives provider the right to suspend and/or terminate the service and/or the contract, and sometimes details the circumstances under which the provider claims to have a right to do so. Unilateral termination clauses that specify reasons for termination were marked as potentially unfair. Whereas clauses stipulating that the service provider may suspend or terminate the service at any time for any or no reasons and/or without notice were marked as clearly unfair."* (Lippi et al., 2019)
-	`<use>` = Contract by using: *"This clause stipulates that the consumer is bound by the terms of use of a specific service, simply by using the service, without even being required to mark that he or she has read and accepted them. We always marked such clauses as potentially unfair. The reason for this choice is that a good argument can be offered for these clauses to be unfair, because they originate an imbalance in rights and duties of the parties, but this argument has no decisive authoritative backing yet, since the ECJ has never assessed a clause of this type."* (Lippi et al., 2019)
-	`<pinc>` = Privacy included: These tags *"identify clauses stating that consumers consent to the privacy policy simply by using the service. Such clauses have been always considered potentially unfair"* (Drawzeski et al., 2021)



### Data Splits

No split provided.

## Dataset Creation

### Curation Rationale

The EU legislation is published in all official languages. This multilingualism comes with costs and challenges, such as cross-linguistical interpretability. The EU has refrained from regulating languages in which standard terms in consumer contracts should be drafted, allowing for differing approaches to emerge in various jurisdictions. Consumer protection authorities and non-governmental organizations in Europe tend to operate only in their respective languages. Therefore, consumer protection technologies are needed that are capable of dealing with multiple languages. The dataset at hand can be used for the automated detection of unfair clauses in ToS which, in most cases, are available in multiple languages. 

### Source Data

#### Initial Data Collection and Normalization

*"The analysed ToS were retrieved from the [Claudette pre-existing corpus](http://claudette.eui.eu/ToS.zip), covering 100 English ToS (Lippi et al., 2019; Ruggeri et al., 2021). Such terms mainly concern popular digital services provided to consumers, including leading online platforms (such as search engines and social media). The predominant language of drafting of these ToS is English, with differing availability of corre- sponding ToS in other languages. To carry out the present study, the ultimate 25 ToS were selected on the basis of three main criteria: a) their availability in the four selected languages; b) the possibility of identifying a correspondence between the different versions, given their publication date; and c) the similarity of their structure (e.g. number of clauses, sections, etc.). To illustrate, while ToS in both German and Italian were identified for 63 out of the 100 ToS contained in the pre-existing Claudette training corpus, Polish versions were found for only 42 of these 63 ToS. Out of the 42 ToS available in the four languages, we selected those with the more closely corresponding versions based on criteria b) and c) above. Perfect correspondence across the 4 languages, however, could not be achieved for all 25 ToS."* (Drawzeski et al., 2021)

#### Who are the source language producers?

The ToS are produced by lawyers??????

### Annotations

#### Annotation process

The dataset at hand is described (Drawzeski et al., 2021). The ToS of the dataset were retrieved from the pre-existing and mono-lingual (English) Claudette corpus which is described in (Lippi et al., 2019). (Drawzeski et al., 2021) *“investigate methods for automatically transferring the annotations made on ToS in the context of the Claudette project onto the corresponding versions of the same documents in a target language, where such resources and expertise may be lacking.”* Therefore, in the following, we will present the annotation process for the Claudette corpus as described in (Lippi et al., 2019). 

*”The corpus consists of 50 relevant on-line consumer contracts, i.e., ToS of on-line platforms. Such contracts were selected among those offered by some of the major players in terms of number of users, global relevance, and time the service was established. Such contracts are usually quite detailed in content, are frequently updated to reflect changes both in the service and in the applicable law, and are often available in different versions for different jurisdictions. Given multiple versions of the same contract, we selected the most recent version available on-line to European customers. The mark-up was done in XML by three annotators, which jointly worked for the formulation of the annotation guidelines. The whole annotation process included several revisions, where some corrections were also suggested by an analysis of the false positives and false negatives retrieved by the initial machine learning prototypes. Due to the large interaction among the annotators during this process, in order to assess inter-annotation agreement, a further test set consisting of 10 additional contracts was tagged, following the final version of the guidelines. […] We produced an additional test set consisting of 10 more annotated contracts. Such documents were independently tagged by two distinct annotators who had carefully studied the guidelines. In order to quantitatively measure the inter-annotation agreement, for this test set we computed the standard Cohen’s 𝜅 metric […] which resulted to be 0.871 […].”*


#### Who are the annotators?

Not specified.

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

It is very likely that some ToS in German, Italian and Polish are direct translations from English. Drawzeski et al. (2021) write: *“Although we could not assess this comprehensively in the present study, we infer from the wording of the ToS that at least in 9 out of 25 cases, German, Italian and Polish documents were indeed translations of the English originals.”*

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

(Drawzeski et al., 2021)

### Licensing Information

[More Information Needed]

### Citation Information


```
@inproceedings{drawzeski-etal-2021-corpus,
  address = {Punta Cana, Dominican Republic},
  author = {Drawzeski, Kasper and Galassi, Andrea and Jablonowska, Agnieszka and Lagioia, Francesca and Lippi, Marco and Micklitz, Hans Wolfgang and Sartor, Giovanni and Tagiuri, Giacomo and Torroni, Paolo},
  booktitle = {Proceedings of the Natural Legal Language Processing Workshop 2021},
  doi = {10.18653/v1/2021.nllp-1.1},
  month = {nov},
  pages = {1--8},
  publisher = {Association for Computational Linguistics},
  title = {{A Corpus for Multilingual Analysis of Online Terms of Service}},
  url = {https://aclanthology.org/2021.nllp-1.1},
  year = {2021}
}
```
```
@article{Lippi2019,
  author = {Lippi, Marco and Pa{\l}ka, Przemys{\l}aw and Contissa, Giuseppe and Lagioia, Francesca and Micklitz, Hans-Wolfgang and Sartor, Giovanni and Torroni, Paolo},
  doi = {10.1007/s10506-019-09243-2},
  issn = {1572-8382},
  journal = {Artificial Intelligence and Law},
  number = {2},
  pages = {117--139},
  title = {{CLAUDETTE: an automated detector of potentially unfair clauses in online terms of service}},
  url = {https://doi.org/10.1007/s10506-019-09243-2},
  volume = {27},
  year = {2019}
}
```


### Contributions

Thanks to [@JoelNiklaus](https://github.com/joelniklaus) and [@kapllan](https://github.com/kapllan) for adding this dataset.
