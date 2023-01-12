from datasets import load_dataset

def get_random_samples(dataset_name, language, n=20):
  dataset = load_dataset(dataset_name, language, split="train", streaming=True)
  shuffled_dataset = dataset.shuffle(seed=42, buffer_size=10_000)
  return list(shuffled_dataset.take(n))

# Manual Review of 20 random examples (December 24, 2022 by Joel Niklaus, German native, English & Spanish fluent, French intermediate, Italian basic)
# General Notes: there are some interesting texts in there that would likely not be included in our other sources

# Indices: 198132077, 198885299, 197489274, 198255299, 198782729, 198641086, 198727515, 198679342, 199147087, 198281610, 197422643, 197639165, 198601519, 197407898, 198926545, 198100010, 198109986, 198516750, 198758556, 197415150 ==> 20/20 positive 
# Note: seems good heuristic here
random_samples = get_random_samples("joelito/mc4_legal", "de", 20)

# Indices: 395235230, 397478402, 396157138, 393853661 ==> 4/20 positive 
# Notes: didn't find pattern for how to reduce false positive rate ==> maybe get better search terms
random_samples = get_random_samples("joelito/mc4_legal", "en", 20) 

# Indices: 208215748, 210446732, 206394829, 208577313, 210142647, 209760189, 210001216, 209861976, 211256379, 208642854, 206200813, 206818059, 209639675, 206158798, 210562569, 208121355, 208154488, 209389343, 210073916, 206173824  ==> 20 / 20 positive
# Notes: Add new terms such as Decisión nº, Resolución, Real Decreto
random_samples = get_random_samples("joelito/mc4_legal", "es", 20)

# Indices: 4762465, 670694, 4440390, 4040779, 4290306, 4140934, 5563095, 512503, 4882866, 2382727, 2415617, 3677255, 486609 ==> 13 / 20 positive
# Notes: arrêt has many false positives, require whitespace before "art" to prevent false positives like "Part", many examples are from legifrance
random_samples = get_random_samples("joelito/mc4_legal", "fr", 20)

# Indices: 1185449, 340834, 1361903, 2054452, 1884816, 1934845, 2557778, 1396868, 255008, 525701, 1831357, 2242163, 1136278, 1152985, 1724540, 2028527 ==> 16 / 20 positive
# Notes: Add new terms such as Cass., provvedimento n., articolo
random_samples = get_random_samples("joelito/mc4_legal", "it", 20)

random_samples