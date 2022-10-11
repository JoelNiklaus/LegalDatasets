from datasets import load_dataset

from utils import save_and_compress

"""
Case law and Legislation from Denmark 
"""

danish_dataset = load_dataset('DDSC/partial-danish-gigaword-no-twitter', split='train')
legislation = danish_dataset.filter(lambda example: example['source'] == 'retsinformationdk')  # legislation
caselaw = danish_dataset.filter(lambda example: example['source'] == 'retspraksis')  # caselaw

legislation = legislation.add_column("type", ["legislation"] * len(legislation))
caselaw = caselaw.add_column("type", ["caselaw"] * len(caselaw))

legislation = legislation.add_column("language", ["da"] * len(legislation))
caselaw = caselaw.add_column("language", ["da"] * len(caselaw))

legislation = legislation.add_column("jurisdiction", ["Denkmark"] * len(legislation))
caselaw = caselaw.add_column("jurisdiction", ["Denkmark"] * len(caselaw))

print(legislation)

save_and_compress(legislation, 'legislation_denmark')
save_and_compress(caselaw, 'caselaw_denmark')
