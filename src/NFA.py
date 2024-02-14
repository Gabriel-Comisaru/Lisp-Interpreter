from .DFA import DFA

from dataclasses import dataclass
from collections.abc import Callable

EPSILON = ''  # this is how epsilon is represented by the checker in the transition function of NFAs

@dataclass
class NFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], set[STATE]]
    F: set[STATE]

    def epsilon_closure(self, state: STATE) -> set[STATE]:
        return self.epsilon_closure_helper(state, set())
    
    def epsilon_closure_helper(self, state: STATE, all_states: set[STATE]) -> set[STATE]:
        all_states.add(state)
        epsilon_transitions = self.d.get((state, EPSILON), []) # get all the epsilon transitions for the current state

        for s in epsilon_transitions:
            if s not in all_states: # if the state is not in the set of all states
                self.epsilon_closure_helper(s, all_states) # epsilon closure for the rest of the states

        return all_states
    
    def subset_construction(self) -> DFA[frozenset[STATE]]:
        
        current_states = self.epsilon_closure(self.q0)
        d = {}
        K = set()
        F = set()
        S = self.S
        q0 = frozenset(current_states)
        K.add(q0)
        queue = [q0]
        # as long as there are states to be processed
        while queue:
            current_state = queue.pop(0) # get the first state in the queue
            for letter in S: # for every letter in the alphabet
                new_state = set()
                for state in current_state:
                    if (state, letter) in self.d: # if there is a transition for the current state and letter
                        for s in self.d[(state, letter)]: # for every state in the transition
                            new_state.update(self.epsilon_closure(s)) # add the epsilon closure of the next state
                
                if new_state: # if the new state is not empty
                    new_state = frozenset(new_state) # make it immutable
                    if new_state not in K: # if the new state is not in K add it
                        K.add(new_state)
                        queue.append(new_state) # add it to the queue
                    d[(current_state, letter)] = new_state # add the transition to the new state
                    
        # verify if every state in K has a final state, if so add it to F            
        F.update(state for state in K if any(s in self.F for s in state))
        
        # add a sink state if there are any missing transitions
        for state in K:
            for letter in S:
                d.setdefault((state, letter), frozenset())
            
        # if there are any missing transitions from the sink state to itself, add them
        if any(len(d[(state, letter)]) == 0 for state in K for letter in S):
            sink_state = frozenset()
            for letter in S:
                d[(sink_state, letter)] = sink_state
            K.add(sink_state)

        return DFA(S, K, q0, d, F)

    def remap_states[OTHER_STATE](self, f: 'Callable[[STATE], OTHER_STATE]') -> 'NFA[OTHER_STATE]':
        
        remapped_states = {state: f(state) for state in self.K}
        remapped_q0 = f(self.q0)
        remapped_d = {(remapped_states[state], letter): {remapped_states[s] for s in next_states} for (state, letter), next_states in self.d.items()}
        remapped_F = {f(state) for state in self.F}

        return NFA(self.S, set(remapped_states.values()), remapped_q0, remapped_d, remapped_F)
