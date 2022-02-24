from urllib.parse import urlparse
import plotly.express as px

import pandas as pd
from datasets import load_dataset, tqdm

link_path = 'data/domains/links.csv'

retrieve_domains = True

if retrieve_domains:

    mc4 = load_dataset("mc4", languages=['de'], streaming=True, split="train")
    mc4 = mc4.remove_columns('text')

    print(f"Building a histogram of domains in mc4")
    batch_size = int(1e5)


    def save_and_reset(links):
        print(f"Saving {batch_size} links to the file system")
        df = pd.DataFrame(links)
        df.to_csv(link_path, mode='a', header=False)
        return {"url": [], "domain": []}


    links = {"url": [], "domain": []}
    df = pd.DataFrame(links)
    df.to_csv(link_path)
    for idx, doc in enumerate(mc4):
        url = doc['url']
        domain = urlparse(url).netloc
        links["url"].append(url)
        links["domain"].append(domain)

        if idx % batch_size == 0:
            links = save_and_reset(links)

print(f"Reading domain names from {link_path}")
df = pd.read_csv(link_path)
print("Computing value counts of domains")
domains = df.domain.value_counts().rename_axis('unique_domains').reset_index(name='counts')
domains.to_csv('data/domains/domains_all.csv')

top_ks = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000]

for top_k in top_ks:
    print(f"Processing top {top_k} value counts")
    top_k_df = domains.head(top_k)
    top_k_df.to_csv(f'data/domains/domains_top_{top_k:04d}.csv')
    fig = px.histogram(top_k_df, x="unique_domains", y="counts")
    fig.write_image(f'data/domains/domain-histogram_{top_k:04d}.png')

print("Finished running script")
