# Czech Court Decision Corpus

- [Dataset Infos](https://lindat.mff.cuni.cz/repository/xmlui/handle/11372/LRT-3052)
- [Paper](https://arxiv.org/abs/1910.09513)

This is the Czech Court Decisions Corpus (CzCDC 1.0). This corpus contains whole texts of the decisions from three top-tier courts (Supreme, Supreme Administrative and Constitutional court) in Czech republic. Court decisions are published from 1st January 1993 to 30th September 2018.

The language of decisions is Czech. Content of decisions is unedited and obtained directly from the competent court.

Decisions are in .txt format in three folders divided by courts.

Corpus contains three .csv files containing the list of all decisions with four columns:
- name of the file: exact file name of a decision with extension .txt;
- decision identifier (docket number): official identification of the decision as issued by the court;
- date of decision: in ISO 8601 (YYYY-MM-DD);
- court abbreviation: SupCo for Supreme Court, SupAdmCo for Supreme Administrative Court, ConCo for Constitutional Court

Statistics:
- SupCo: 111 977 decisions, 23 699 639 lines, 224 061 129 words, 1 462 948 200 bits;
- SupAdmCo: 52 660 decisions, 18 069 993 lines, 137 839 985 words, 1 067 826 507 bits;
- ConCo: 73 086 decisions, 6 178 371 lines, 98 623 753 words, 664 657 755 bits
- all courts combined: 237 723 decisions, 47 948 003 lines, 460 524 867 words, 3 195 432 462 bits