from bs4 import BeautifulSoup
from matplotlib import pyplot as plt

tei_doc_Slv = '../texts/lvl1/SLV30001.xml'
tei_doc_Portugues = '../texts/lvl1/POR0076_FraFBen_Franceses.xml'
tei_doc_Pol = '../texts/lvl1/POL0093_zeromski_syzyfowe-prace.xml'

with open(tei_doc_Slv, 'r', encoding='utf-8') as tei:
    soup_Slv = BeautifulSoup(tei, 'lxml-xml')

with open(tei_doc_Portugues, 'r', encoding='utf-8') as tei:
    soup_Portugues = BeautifulSoup(tei, 'lxml-xml')

with open(tei_doc_Pol, 'r', encoding='utf-8') as tei:
    soup_Pol = BeautifulSoup(tei, 'lxml-xml')

def tokenize_text(soup):
    text = soup.find_all('p')
    tokens = []
    for p in text:
        words = p.get_text().split()
        tokens.extend(words)
    return tokens

def get_frequency_distribution(tokens):
    freq_dist = {}
    for token in tokens:
        token = token.lower()
        if token in freq_dist:
            freq_dist[token] += 1
        else:
            freq_dist[token] = 1

    freq_dist = sorted(freq_dist.items(), key=lambda x: x[1], reverse=True)
    return freq_dist

def zipf_law(freq_dist_list, titles):
    plt.figure(figsize=(10, 6))
    for i in range(len(freq_dist_list)):
        ranks = []
        for j in range(len(freq_dist_list[i])):
            ranks.append(j + 1)
        frequencies = []
        for j in range(len(freq_dist_list[i])):
            frequencies.append(freq_dist_list[i][j][1])
        plt.loglog(ranks, frequencies, label=titles[i])

    plt.title("Zipf's Law")
    plt.xlabel("Rank (log scale)")
    plt.ylabel("Frequency (log scale)")
    plt.legend()
    plt.grid(True)
    plt.show()
    
def heaps_law(tokens_list, titles):
    plt.figure(figsize=(10, 6))
    for i in range(len(tokens_list)):
        tokens = tokens_list[i]
        text_length = []
        vocab_size = []
        vocab = set()
        for j in range(len(tokens)):
            vocab.add(tokens[j].lower())
            text_length.append(j + 1)
            vocab_size.append(len(vocab))
        plt.loglog(text_length, vocab_size, label=titles[i])
        
    plt.title("Heaps' Law")
    plt.xlabel("Text Length (log scale)")
    plt.ylabel("Vocabulary Size (log scale)")
    plt.legend()
    plt.grid(True)
    plt.show()
    
tokens_Slv = tokenize_text(soup_Slv)
tokens_Portugues = tokenize_text(soup_Portugues)
tokens_Pol = tokenize_text(soup_Pol)
freq_dist_Slv = get_frequency_distribution(tokens_Slv)
freq_dist_Portugues = get_frequency_distribution(tokens_Portugues)
freq_dist_Pol = get_frequency_distribution(tokens_Pol)
zipf_law([freq_dist_Slv, freq_dist_Portugues, freq_dist_Pol],
         ['Slovenian', 'Portuguese', 'Polish'])
heaps_law([tokens_Slv, tokens_Portugues, tokens_Pol],
            ['Slovenian', 'Portuguese', 'Polish'])