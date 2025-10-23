from bs4 import BeautifulSoup
from matplotlib import pyplot as plt

tei_doc_Perdicao = '../texts/lvl1/POR0010_CamCB_Perdicao.xml'
tei_doc_Mulheres = '../texts/lvl1/POR0011_CamCB_Mulheres.xml'
tei_doc_Misterios = '../texts/lvl1/POR0012_CamCB_Misterios.xml'

with open(tei_doc_Perdicao, 'r', encoding='utf-8') as tei:
    soup_Perdicao = BeautifulSoup(tei, 'lxml-xml')

with open(tei_doc_Mulheres, 'r', encoding='utf-8') as tei:
    soup_Mulheres = BeautifulSoup(tei, 'lxml-xml')

with open(tei_doc_Misterios, 'r', encoding='utf-8') as tei:
    soup_Misterios = BeautifulSoup(tei, 'lxml-xml')

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
    
tokens_Perdicao = tokenize_text(soup_Perdicao)
freq_Perdicao = get_frequency_distribution(tokens_Perdicao)
tokens_Mulheres = tokenize_text(soup_Mulheres)
freq_Mulheres = get_frequency_distribution(tokens_Mulheres)
tokens_Misterios = tokenize_text(soup_Misterios)
freq_Misterios = get_frequency_distribution(tokens_Misterios)
zipf_law([freq_Perdicao, freq_Mulheres, freq_Misterios],
          ["Perdicao", "Mulheres", "Misterios"])
heaps_law([tokens_Perdicao, tokens_Mulheres, tokens_Misterios],
          ["Perdicao", "Mulheres", "Misterios"])