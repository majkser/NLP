import regex as re
from BasicTokenizer import BasicTokenizer

GPT4_SPLIT_PATTERN = r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""

class RegexTokenizer(BasicTokenizer):
    def __init__(self, pattern: str = GPT4_SPLIT_PATTERN):
            super().__init__()
            self.compiled_pattern = re.compile(pattern)
            self.merges = {}

    def train(self, text: str, vocab_size: int, verbose: bool = False) -> None:
        text_chunks = self.compiled_pattern.findall(text)
        
        tokens = [list(chunk.encode('utf-8')) for chunk in text_chunks]
        
        if verbose:
            print('length of the text: ', len(text))
            print('num of tokens: ', len(tokens))
        
        for i in range(vocab_size - 256):
            for j in range(len(tokens)):
                pass
    
    def encode(self):
        pass
    
    def decode():
        pass
    
if __name__ == "__main__":  
    tokenizer = RegexTokenizer()
    tokenizer.train("This is a sample textS for RegexTokenizer.", vocab_size=100, verbose=True)