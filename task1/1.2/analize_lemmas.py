from bs4 import BeautifulSoup
from matplotlib import pyplot as plt

tei_doc_Crioulo = '../texts/lvl2/POR0020_AbeBot_Crioulo.xml'
tei_doc_Lavos = '../texts/lvl2/POR0053_AbeBot_Lavos.xml'
tei_doc_Amanha = '../texts/lvl2/POR0054_AbeBot_Amanha.xml'

with open(tei_doc_Crioulo, 'r', encoding='utf-8') as tei:
    soup_Crioulo = BeautifulSoup(tei, 'lxml-xml')

with open(tei_doc_Lavos, 'r', encoding='utf-8') as tei:
    soup_Lavos = BeautifulSoup(tei, 'lxml-xml')

with open(tei_doc_Amanha, 'r', encoding='utf-8') as tei:
    soup_Amanha = BeautifulSoup(tei, 'lxml-xml')

def get_lemmas(soup):
    text = soup.find_all('w')
    lemmas = []
    for w in text:
        words = w['lemma'].split()
        lemmas.extend(words)
    return lemmas

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
    
lemmas_Crioulo = get_lemmas(soup_Crioulo)
lemmas_Lavos = get_lemmas(soup_Lavos)
lemmas_Amanha = get_lemmas(soup_Amanha)
freq_dist_Crioulo = get_frequency_distribution(lemmas_Crioulo)
freq_dist_Lavos = get_frequency_distribution(lemmas_Lavos)
freq_dist_Amanha = get_frequency_distribution(lemmas_Amanha)
zipf_law([freq_dist_Crioulo, freq_dist_Lavos, freq_dist_Amanha],
         ['Crioulo', 'Lavos', 'Amanha'])
heaps_law([lemmas_Crioulo, lemmas_Lavos, lemmas_Amanha],
          ['Crioulo', 'Lavos', 'Amanha'])