# MARCELL

[Project Link](http://marcell-project.eu/)

## Bulgarian Legislation

[Download](https://elrc-share.eu/repository/browse/marcell-bulgarian-legislative-subcorpus-v2/946267fe8d8711eb9c1a00155d026706d2c9267e5cdf4d75b5f02168f01906c6/)

The MARCELL Bulgarian subcorpus consists of 29,648 documents (at the end of March 2021) which are classified into
fifteen types. The time span of the documents is 1946–2021.
The data has been retrieved from the Bulgarian State Gazette (http://dv.parliament.bg), the Bulgarian government
official journal, publishing documents from the official institutions like government, National Assembly of Bulgaria,
Constitutional Court, etc. A C++ based NLP Pipeline for Bulgarian, constructed such as to answer the requirements of the
project for autonomy and sustainability, is continuously feeding the Bulgarian corpus with newly issued legislative
documents. Data is extracted from a single web source and further transformed. The transformation phase makes changes to
the data format, filters document tapes, organises data in structures, and accumulates data with metadata and linguistic
information. The annotation modules of the pipeline integrate a sentence splitter, a tokeniser, a part-of-speech tagger,
a lemmatiser, a UD parser, a named entity recogniser, a noun phrase parser, an IATE term annotator, an Eurovoc
descriptor annotator and an Eurovoc MT annotator (https://www.aclweb.org/anthology/2020.lrec-1.863/). The documents are
classified into the EuroVoc Top Level Domains. The classification module is made available as a part of the Bulgarian
NLP Pipeline.

## Hungarian Legislation

[Download](https://elrc-share.eu/repository/browse/marcell-hungarian-legislative-subcorpus-v2/a87295ec8d6511eb9c1a00155d0267065f7e56dc7db34ce5aaae0b48a329daaa/)

The Hungarian corpus representing the Hungarian national legislation contains 26821 documents retrieved from PDF files
of the official gazette Magyar Közlöny which is freely available online for download. There are 11 different text types
in the corpus covering different kinds of legal texts: law, regulation, decree, etc. The documents were published in the
period between 1991 and 2019.
The data was analysed with the e-magyar text processing system. The system was enhanced with detokenization
functionality (precisely for the requirements of the MARCELL project) to provide SpaceAfter=No annotation indicating no
whitespace between two tokens in the original text. Additional scripts were created for extracting the necessary
metadata, for converting to CoNLL-U Plus format, for annotating IATE terms and EuroVoc descriptors in the text, as well
as for classifying the documents into top-level EuroVoc domains. EuroVoc MT codes corresponding to the EuroVoc
descriptors were also added to the annotation.
The raw data is 31.2M tokens, the analysed corpus is 2.9GB in CoNLL-U Plus format.

## Polish Legislation

[Download](https://elrc-share.eu/repository/browse/marcell-polish-legislative-subcorpus-v2/dd14fa1c8d6811eb9c1a00155d026706c4718ddc9c6e4a92a88923816ca8b219/)

The Polish corpus contains 27485 documents of 21 types representing universally binding legal acts (laws, regulations,
etc.) or binding internal acts (such as resolutions of the Sejm, Senate and some state administration bodies, e.g. the
Council of Ministers). The time span of the documents is 1972–2021 and the set covers only the documents in effect.
The data were retrieved from Dziennik Ustaw and Monitor Polski, the official and publicly available sources of Polish
law, publishing Acts of Parliament, Regulations of the Ministers, uniform acts and amendments. The data was converted
from editable PDF files to textual format (unfortunately an XML version of those documents was unavailable), tokenized
and morphologically analysed with Morfeusz2 morphological analyser, disambiguated with Concraft-pl tagger, named entity
recognition with Liner2 and dependency-parsed with COMBO parser. Additional scripts were created (and used) for IATE
terms and EuroVoc descriptors annotation.
According to the Polish law, pursuant to Article 4(1) of the Act of 4 February 1994 on copyright and related rights,
normative acts and their official drafts are not subject to copyright and as such are in the public domain.

## Romanian Legislation

[Download](https://elrc-share.eu/repository/browse/marcell-romanian-legislative-subcorpus-v2/2da548428b9d11eb9c1a00155d026706ce94a6b59ffc4b0e9fb5cd9cebe6889e/)

The Romanian corpus contains 163,274 files, which represent the body of national legislation ranging from 1881 to 2021.
This corpus includes mainly: governmental decisions, ministerial orders, decisions, decrees and laws. All the texts were
obtained via crawling from the public Romanian legislative portal . We have not distinguished between in force and "out
of force" laws because it is difficult to do this automatically and there is no external resource to use to distinguish
between them. The texts were extracted from the original HTML format and converted into TXT files. Each file has
multiple levels of annotation: firstly the texts were tokenized, lemmatized and morphologically annotated using the
Tokenizing, Tagging and Lemmatizing (TTL) text processing platform developed at RACAI, then dependency parsed with
NLP-Cube, named entities were identified using a NER tool developed at RACAI, nominal phrases were identified also with
TTL, while IATE terms and EuroVoc descriptors were identified using an internal tool. All processing tools were
integrated into an end-to-end pipeline available within the RELATE platform and as a dockerized version. The files were
annotated with the latest version of the pipeline completed within Activity 4 of the MARCELL project.

## Slovak Legislation

[Download](https://elrc-share.eu/repository/browse/marcell-slovak-legislative-subcorpus-v2/6bdee1d68c8311eb9c1a00155d0267063398d3f1a3af40e1b728468dcbd6efdd/)

The Slovak corpus (33 million tokens) contains documents of legally binding acts starting from the year 1993 (following
minor orthography reform in 1991, but it also coincides with the independence of Slovakia). The data is obtained from
the Slov-Lex legislative and information portal archive of the acts approved by the Slovak Parliament. The data has been
converted from the original HTML format, filtered by date and document length, tokenized, lemmatized and morphologically
annotated with the Slovak MorphoDita model and dependency parsed with UDPipe.

## Slovenian Legislation

[Download](https://elrc-share.eu/repository/browse/marcell-slovenian-legislative-subcorpus-v2/e2a779868d4611eb9c1a00155d026706983c845a30d741b78e051faf91828b0d/)

The Slovenian corpus contains 25 thousand documents (5 GB in size, 148 M tokens), ranging from 1974 to 2020. The data
was obtained from the Slovenian Open Data Portal. The original file type is JSON which contains individual document in
HTML format. The data in the corpus was extracted from the HTML documents, tokenized with the Slovenian tokenizer
Obeliks4j (Grcar et al., 2012), and lemmatized, tagged and dependency parsed with a fork of the StanfordNLP parser (Peng
et al., 2018) trained on ssj500k training corpus (Krek et al., 2017). Additional scripts have been created to extract
metadata and annotate IATE terms and EuroVoc descriptions. The legislation is published in the Slovenian Open Data
Portal under the CC-BY 4.0 license.



