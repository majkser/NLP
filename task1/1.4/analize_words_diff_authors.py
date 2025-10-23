from bs4 import BeautifulSoup
from matplotlib import pyplot as plt

tei_doc_Agitador = '../texts/lvl1/POR0075_ForCPin_Agitador.xml'
tei_doc_Franceses = '../texts/lvl1/POR0076_FraFBen_Franceses.xml'
tei_doc_Deserto = '../texts/lvl1/POR0077_JosJRBas_Deserto.xml'

with open(tei_doc_Agitador, 'r', encoding='utf-8') as tei:
    soup_Agitador = BeautifulSoup(tei, 'lxml-xml')

with open(tei_doc_Franceses, 'r', encoding='utf-8') as tei:
    soup_Franceses = BeautifulSoup(tei, 'lxml-xml')

with open(tei_doc_Deserto, 'r', encoding='utf-8') as tei:
    soup_Deserto = BeautifulSoup(tei, 'lxml-xml')

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
    
tokens_Agitador = tokenize_text(soup_Agitador)
tokens_Franceses = tokenize_text(soup_Franceses)
tokens_Deserto = tokenize_text(soup_Deserto)
freq_dist_Agitador = get_frequency_distribution(tokens_Agitador)
freq_dist_Franceses = get_frequency_distribution(tokens_Franceses)
freq_dist_Deserto = get_frequency_distribution(tokens_Deserto)
zipf_law([freq_dist_Agitador, freq_dist_Franceses, freq_dist_Deserto],
         ['Pinto, Fortunato Correia', 'Benevides, Francisco da Fonseca', 'Bastos, José Joaquim Rodrigues de'])
heaps_law([tokens_Agitador, tokens_Franceses, tokens_Deserto],
          ['Pinto, Fortunato Correia', 'Benevides, Francisco da Fonseca', 'Bastos, José Joaquim Rodrigues de'])