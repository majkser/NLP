import re

patterns = [
    (r"\b(cze[sś][ćc])|hej|elo|witam|dzie[ńn] dobry\b", "Cześć! Jak mogę Ci pomóc w sprawie rezerwacji wakacji?"),
    (r"\bgdzie|kierunek|(pole[ćc])\b", "Polecam wycieczki do Grecji i Hiszpanii - jeśli lubisz słońce i plaże! Natomiast jeśli preferujesz góry, to Szwajcaria lub Austria będzie idealna."),
    (r"\bhotel|nocleg|nocowanie|nocowa[cć]|motel|spa[ćc]\b", "Mamy szeroki wybór noclegów, od luksusowych po budżetowe. Wszystkie opcje noclegów możesz znaleźć na naszej stronie internetowej w zakładce 'Nocleg' - istnieje możliwość sortowania według ceny, lokalizacji i opinii."),
    (r"\b((dokument)y?|wiz[ay]|paszport|dow[óo]d)u?\b", "Do krajów Unii Europejskiej wystarczy ważny dowód osobisty lub paszport. W przypadku podróży do krajów spoza UE, może być wymagana wiza - sprawdź to przed wyjazdem."),
    (r"\brabat|zni[zż]ka|last minute|first minute\b", "Wszystkie aktualne promocje i oferty specjalne znajdziesz na naszej stronie internetowej w zakładce 'Promocje'."),
    (r"^.*(usu[ńn]|usun[aą][ćc])\s+konto.*$", "Aby usunąć konto, skontaktuj się z naszym działem obsługi klienta (tel: +48 777 777 777)."),
    (r"\b((cz[lł]owiek)(iem)*|telefon|kontakt|(konsultant)(em)*)\b", "Aby porozmawiać z naszym konsultantem, zadzwoń pod numer +48 123 456 789 lub napisz na email: kontakt@example.pl"),
    (r"\b(skarg[eęa]|reklamacj[eęa])\b", "W przypadku skarg lub reklamacji, prosimy o kontakt z naszym działem obsługi klienta pod numerem +48 987 654 321 lub poprzez email: reklamacje@example.pl."),
]

compiled_patterns = [(re.compile(pattern, re.IGNORECASE), response) for pattern, response in patterns]

def get_response(user_input):
    for pattern, response in compiled_patterns:
        if pattern.search(user_input):
            return response
    return "Możemy porozmawiać jedynie na temat rezerwacji wakacji."

def main():
    print("Witaj! Jestem Eliza, Twoja wirtualna asystentka do rezerwacji wakacji. Aby skończyć rozmowę, wpisz 'exit' lub 'koniec'.")
    while True:
        user_input = input("Ty: ")
        if user_input.lower() in ['exit', 'koniec']:
            print("Eliza: Do widzenia! Miłego dnia!")
            break
        response = get_response(user_input)
        print(f"Eliza: {response}")
        
if __name__ == "__main__":
    main()