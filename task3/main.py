from Smith_Waterman_algorithm import Smith_Waterman_algorithm

import Levenshtein
# Levenshtein.distance() - Mierzy, ile operacji (wstawienie, usunięcie, zamiana znaku) trzeba wykonać, aby zamienić jeden tekst w drugi.

def main():
    text_file = open('grimm-letters.txt')
    text = text_file.read()
    text_file.close()
    
    lines = text.splitlines()
    
    first_letter = ''
    second_letter = ''
    third_letter = ''
    
    for line in lines:
        if not line.strip():
            continue
        column_with_text = line.split('\t')[1]
        if line.startswith('1'):
            first_letter += column_with_text + '\n'
        elif line.startswith('2'):
            second_letter += column_with_text + '\n'
        elif line.startswith('3'):
            third_letter += column_with_text + '\n'
    
    print("Alignment between First and Second Letter:")
    first_alignment, second_alignment = Smith_Waterman_algorithm(first_letter.strip(), second_letter.strip())
    Levenshtein_distance = Levenshtein.distance(first_alignment, second_alignment)
    print(f"Levenshtein Distance: {Levenshtein_distance}\n")
    
    print("Alignment between First and Third Letter:")
    first_alignment, third_alignment = Smith_Waterman_algorithm(first_letter.strip(), third_letter.strip())
    Levenshtein_distance = Levenshtein.distance(first_alignment, third_alignment)
    print(f"Levenshtein Distance: {Levenshtein_distance}\n")
    
    print("Alignment between Second and Third Letter:")
    second_alignment, third_alignment = Smith_Waterman_algorithm(second_letter.strip(), third_letter.strip())
    Levenshtein_distance = Levenshtein.distance(second_alignment, third_alignment)
    print(f"Levenshtein Distance: {Levenshtein_distance}\n")
    
if __name__ == "__main__":
    main()