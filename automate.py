class Automate:
    def __init__(self, config_file):
        self.config_file = config_file
        self.states = []
        self.alphabet = []
        self.transitions = []
        self.final_states = []
        self.initial_state = "q0"

    def configure_automate(self):
        is_final = {}

        with open(self.config_file, "r") as file:
            lines = file.read()

        lines = lines.split("\n")

        for line in lines:
            atoms = line.split(" ")
            initial_state = atoms[0]
            transition = atoms[1]
            finals = atoms[2]

            if "|" in finals:
                final_state = finals.split("|")
            else:
                final_state = [finals]
            if initial_state not in self.states:
                self.states.append(initial_state)
            is_final[initial_state] = False

            for final in final_state:
                if final not in self.states:
                    self.states.append(final)

                if final not in is_final:
                    is_final[final] = True

            if len(transition) == 1:
                for final in final_state:
                    self.transitions.append((initial_state, {transition: final}))
                if transition not in self.alphabet:
                    self.alphabet.append(transition)
            else:
                if "..." not in transition:
                    for char in transition:
                        for final in final_state:
                            self.transitions.append((initial_state, {char: final}))
                        if char not in self.alphabet:
                            self.alphabet.append(char)
                else:
                    first = transition[0]
                    last = transition[4]

                    for char in range(ord(first), ord(last) + 1):
                        for final in final_state:
                            self.transitions.append((initial_state, {chr(char): final}))
                        if chr(char) not in self.alphabet:
                            self.alphabet.append(chr(char))

        for key, value in is_final.items():
            if value is True:
                self.final_states.append(key)

    def verify_dfa_sequence(self, sequence):
        invalid_sequence = "Secventa nu este acceptata"
        current_state = self.initial_state

        length = 0
        for symbol in sequence:
            length += 1
            found = False
            for transition in self.transitions:
                if length < len(sequence):
                    if (transition[0] == current_state and symbol in transition[1] and
                            transition[1][symbol] not in self.final_states):
                        current_state = transition[1][symbol]

                        if length != len(sequence) and sequence[length] != "." and current_state != "q1":
                            current_state = "q2"
                        elif sequence[length] == ".":
                            current_state = "q3"

                        found = True
                        break
                else:
                    if (transition[0] == current_state and symbol in transition[1] and
                            transition[1][symbol] in self.final_states):
                        current_state = transition[1][symbol]
                        found = True
                        break

            if found is False:
                return invalid_sequence

        return "Secventa este acceptata" if current_state in self.final_states else invalid_sequence
