from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class DFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], STATE]
    F: set[STATE]

    def accept(self, word: str) -> bool:
        state = self.q0
        # for every letter in the alphabet
        for letter in word:
            # if there is a transition for the current state and letter
            if (state, letter) in self.d:
                state = self.d[(state, letter)] # set the current state to the next state
            else:
                return False 
        # if the state we end up in is a final state, return true
        return state in self.F
        
    def remap_states[OTHER_STATE](self, f: Callable[[STATE], 'OTHER_STATE']) -> 'DFA[OTHER_STATE]':
        
        remapped_states = {state: frozenset(f(s) for s in state) for state in self.K}
        remapped_q0 = frozenset(f(s) for s in self.q0)
        remapped_d = {(frozenset(f(s) for s in state), letter): frozenset(f(next_state) for next_state in next_states) for (state, letter), next_states in self.d.items()}
        remapped_F = {frozenset(f(s) for s in state) for state in self.F}
        
        return DFA(self.S, set(remapped_states.values()), remapped_q0, remapped_d, remapped_F)


