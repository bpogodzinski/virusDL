from pathlib import Path
DATA1_PATH = Path(__file__).parent / '..' / '..' / 'data'
DATA1_VIRUS_PATH = DATA1_PATH / 'virus'
DATA1_HOST_PATH = DATA1_PATH / 'host'
TAXONOMY_RANKS = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
RESULTS_PATH = DATA1_PATH / 'results'