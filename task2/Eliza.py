import re

patterns = [
    (r"\b(cze[sś][cć])|hej|elo|witam\b", "Cześć! Jak mogę Ci pomóc w sprawie rezerwacji wakacji?"),
]

compiled_patterns = [(re.compile(pattern, re.IGNORECASE), response) for pattern, response in patterns]

def get_response(user_input):
    for pattern, response in compiled_patterns:
        if pattern.search(user_input):
            return response
    return "Możemy porozmawiać jedynie na temat rezerwacji wakacji."

def main():
    print("Witaj! Jestem Eliza, Twoja wirtualna asystentka do rezerwacji wakacji.")
    while True:
        user_input = input("Ty: ")
        if user_input.lower() in ['exit', 'quit', 'koniec']:
            print("Eliza: Do widzenia! Miłego dnia!")
            break
        response = get_response(user_input)
        print(f"Eliza: {response}")
        
if __name__ == "__main__":
    main()