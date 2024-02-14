from .DFA import DFA
from .NFA import NFA
from .Regex import parse_regex

EPSILON = ''

class Lexer:
    def __init__(self, spec: list[tuple[str, str]]) -> None:
        self.nfa_list = []
        for token_name, regex in spec:
            self.nfa_list.append((token_name, self.regex_to_nfa(regex)))

        self.unified_nfa = self.unify_nfa_list()
        self.dfa = self.unified_nfa.subset_construction()

    def regex_to_nfa(self, regex: str) -> NFA[int]:
        reg = parse_regex(regex)
        nfa = reg.thompson()
        return nfa
    
    def unify_nfa_list(self) -> NFA[int]:
        unified_nfa = NFA(set(), {0}, 0, {}, set())
        current_state = 1
        initial_states = set()
        new_nfa_list = []

        for token_name, nfa in self.nfa_list:

            nfa_remapped = nfa.remap_states(lambda x: x + current_state)

            unified_nfa.S.update(nfa_remapped.S)
            unified_nfa.K.update(nfa_remapped.K)
            unified_nfa.d.update(nfa_remapped.d)
            unified_nfa.F.update(nfa_remapped.F)

            initial_states.add(nfa_remapped.q0)

            current_state += len(nfa_remapped.K)
            new_nfa_list.append((token_name, nfa_remapped))

        unified_nfa.d[(unified_nfa.q0, EPSILON)] = initial_states

        self.nfa_list = new_nfa_list
        return unified_nfa

    def lex(self, word: str) -> list[tuple[str, str]] | None:
        result = []
        current_state = self.dfa.q0
        start_index = 0
        index = 0
        last_accepting_state = frozenset()
        last_accepting_index = -1

        while index < len(word):
            char = word[index]
            if char not in self.dfa.S:
                # Invalid character in the input word
                line = word[:index + 1].count('\n')
                if line > 0:
                    index = index - word[:index + 1].rfind('\n') - 1

                result = []
                result.append(("", f'No viable alternative at character {index}, line {line}'))
                return result

            current_state = self.dfa.d.get((current_state, char))

            if len(current_state) == 0:
                # No transition for the current character
                if len(last_accepting_state) != 0:
                    # Return the longest accepted prefix and continue lexing from the remaining word
                    token_name, _ = self.get_token_info_for_state(last_accepting_state)
                    result.append((token_name, word[start_index:last_accepting_index + 1]))
                    start_index = last_accepting_index + 1
                    index = start_index - 1
                    current_state = self.dfa.q0
                    last_accepting_state = frozenset()
                else:
                    # No valid prefix found, lexing fails
                    line = word[:index + 1].count('\n')
                    if line > 0:
                        index = index - word[:index + 1].rfind('\n') - 1

                    result = []
                    result.append(("", f'No viable alternative at character {index}, line {line}'))
                    return result
            elif current_state in self.dfa.F:
                # Found a final state, update last accepting state and index
                last_accepting_state = current_state
                last_accepting_index = index
            index += 1

        # Check if the last token is valid
        if len(last_accepting_state) != 0:
            token_name, _ = self.get_token_info_for_state(last_accepting_state)
            result.append((token_name, word[start_index:last_accepting_index + 1]))
        else:
            line = word[:index + 1].count('\n')
            if line > 0:
                index = index - word[:index + 1].rfind('\n') - 1

            # clear the result
            result = []
            result.append(("", f'No viable alternative at character EOF, line {line}'))
            return result

        return result

    def get_token_info_for_state(self, state):
        state_list = list(state)
        for token_name, nfa in self.nfa_list:
            search = True
            index = 0
            while search:
                if index >= len(state_list):
                    search = False
                    continue
                state = state_list[index]
                if state in nfa.K and state in nfa.F:
                    return token_name, nfa
                else:
                    index += 1
        return None