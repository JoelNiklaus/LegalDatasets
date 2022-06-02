"""
This file scrapes data from Google Scholar and Semantic Scholar to build a database of legal texts
Google Scholar: https://pypi.org/project/scholarly/
Semantic Scholar: https://www.semanticscholar.org/product/api

Maybe with this the full texts can be retrieved: https://serpapi.com/google-scholar-organic-results, but it is pricey

It is not possible to download the full texts. It may also be illegal. That's why we just download the abstracts.

This might not be necessary anymore, because we recieved a file from the Federal Supreme Court with Swiss commentaries
"""
import re

from scholarly import scholarly

"""
Two approaches:
1. Approach:
        go via research interests (search_keyword):
        take all publications of all authors with these interests
    Problem:
        How can we filter out the interests that are not law-oriented?
2. Approach:
        go via citations:
        Start with a set of authors and papers that cite their papers
    Problem:
        For how many levels should we do this?
        Which authors should we select to start?
"""


def scrape_google_scholar():
    def get_citing_pubs_of_author():
        # Retrieve the author's data, fill-in, and print
        search_query = scholarly.search_author_id('7iTqlzcAAAAJ')  # Daniel Hürlimann
        author = scholarly.fill(search_query)
        print(author)

        # Print the titles of the author's publications
        print([pub['bib']['title'] for pub in author['publications']])

        # Take a closer look at the first publication
        pub = scholarly.fill(author['publications'][0])
        print(pub)

        # Which papers cited that publication?
        print([citation['bib']['title'] for citation in scholarly.citedby(pub)])

    starting_keywords = ['Information Law', 'Intellectual Property Law', 'Property Law', 'Administrative Law',
                         'Corporate Law', 'Expert Law', 'Techical Law', 'Constitutional Law', 'Contract Law', ]

    def is_lawyer(author):
        affiliation = author['affiliation'].lower()
        return re.search(r"law|legal", affiliation) is not None

    def get_law_literature_keywords(starting_keywords):
        final_keywords = starting_keywords.copy()
        for keyword in starting_keywords:
            search_query = scholarly.search_keyword(keyword)
            for i in range(100):
                try:
                    author = next(search_query)
                    if is_lawyer(author):
                        final_keywords.extend(author['interests'])
                        author = scholarly.fill(author)
                        scholarly.pprint(author)

                        # Print the author's publications
                        for pub in author['publications']:
                            pub = scholarly.fill(pub)
                            scholarly.pprint(pub)
                            print(pub['bib']['title'])
                            print(pub['bib']['abstract'])
                            if 'public_access' in pub and pub['public_access']:
                                print(pub['pub_url'])
                            else:
                                print("No public access url available")

                except StopIteration:
                    break
        return final_keywords

    final_keywords = get_law_literature_keywords(starting_keywords)
    print(final_keywords)


def scrape_semantic_scholar():
    pass


if __name__ == '__main__':
    scrape_google_scholar()
