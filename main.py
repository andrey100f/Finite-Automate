from automate import Automate


def write_file(filename, automate):
    with open(filename, 'w') as file:
        file.write("Multimea starilor: " + ', '.join(map(str, automate.states)))
        file.write("\nMultimea starilor finale: " + ', '.join(map(str, automate.final_states)))
        file.write("\nAlfabetul: {" + ', '.join(map(str, automate.alphabet)) + "}\n\n")

        file.write("Tranzitiile:\n")
        for tup in automate.transitions:
            word, dic = tup
            line = f"{word} {' '.join([f'{key} {value}' for key, value in dic.items()])}"
            file.write(f"{line}\n")


def main():
    automate_identifiers = Automate("config_identifiers.txt")
    automate_numeric_constants = Automate("config_numeric_constants.txt")

    automate_identifiers.configure_automate()
    automate_numeric_constants.configure_automate()

    write_file("result_automate_identifiers.txt", automate_identifiers)
    write_file("result_automate_numeric_constants.txt", automate_numeric_constants)

    while True:
        print("1. Automat de identificatori.")
        print("2. Automat de constante.")
        print("x. Exit")

        choice = input("Alegeti o optiune: ")

        if choice == "1":
            automate = automate_identifiers
        elif choice == "2":
            automate = automate_numeric_constants
        elif choice == "x":
            print("Se va iesi din program...")
            break
        else:
            print("Optiune gresita...Reincercati")
            continue

        while True:
            print("1. Vezi urmatoarea stare.")
            print("2. Verifica o secventa.")
            print("x. Mergi inapoi.")

            choice = input("Alege o optiune: ")
            if choice == "1":
                user_input = input("Dati starea si simbolul: ")
                text = user_input.split()
                state = text[0]
                symbol = text[1]

                if state not in automate.states:
                    print("Starea nu este valida! Reincercati\n")
                    continue
                if symbol not in automate.alphabet:
                    print("Simbolul nu este valid! Reincercati\n")
                    continue

                next_states = []
                for transition in automate.transitions:
                    if transition[0] == state:
                        for key, value in transition[1].items():
                            if key == symbol:
                                next_states.append(value)

                if len(next_states) == 0:
                    print("Nu se ajunge in nici o stare!\n")
                    continue
                else:
                    print("Se ajunge in: " + ', '.join(map(str, next_states)) + "\n")
                    continue
            elif choice == "2":
                sequence = input("Dati secventa: ")
                print(automate.verify_dfa_sequence(sequence))
            elif choice == "x":
                break
            else:
                print("Optiune gresita...Reincercati!!")


if __name__ == '__main__':
    main()
