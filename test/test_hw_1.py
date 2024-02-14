# import itertools
# import unittest
# from typing import Iterable

# from src.DFA import DFA
# from src.NFA import NFA


# class HW1Tests(unittest.TestCase):
#     score: int

#     def __init__(self, methodName: str = "runTest") -> None:
#         super().__init__(methodName)
#         self.__class__.score = 10 

#     @classmethod
#     def tearDownClass(cls):
#         print('\nHomework 1 - Total score:', cls.score, '/ 100\n')

#     def structural_check(self, dfa: DFA) -> None:
#         for c in dfa.S:
#             self.assertTrue(len(c) == 1, f'non-character in alphabet')

#         self.assertTrue(
#             dfa.F.issubset(dfa.K),
#             f'the set of final states is not a subset of the states',
#         )

#         self.assertTrue(dfa.q0 in dfa.K, f'the initial state is not a state')

#         for c, s in itertools.product(dfa.S, dfa.K):
#             self.assertTrue(
#                 (s, c) in dfa.d,
#                 f'state {s} does not have transitions defined on {c}',
#             )
#             self.assertTrue(
#                 dfa.d[s, c] in dfa.K,
#                 f'destination of transition from state {s} on {c} is not in the dfa'
#             )

#         for s, c in dfa.d.keys():
#             self.assertTrue(
#                 c in dfa.S and s in dfa.K,
#                 f'transition defined on illegal pair {s, c}',
#             )

#     def behaviour_check(self, dfa: DFA, tests: Iterable[tuple[str, bool]]) -> None:
#         for s, ref in tests:
#             self.assertEqual(
#                 dfa.accept(s), ref,
#                 f'dfa has unexpected behaviour on "{s}".'
#                 f' expected: {"accept" if ref else "reject"}'
#             )

#     def test_eps_closure_1(self):
#         nfa = NFA(
#             {'a', 'b'},
#             {0, 1, 2, 3, 4, 5, 6},
#             0,
#             {
#                 (0, ''): {1, 2},
#                 (1, ''): {0},
#                 (2, ''): {4, 6},
#                 (3, ''): {1},
#                 (4, 'a'): {5},
#                 (5, ''): {3},
#                 (6, 'b'): {7},
#                 (7, ''): {3}
#             },
#             {1},
#         )

#         self.assertCountEqual(nfa.epsilon_closure(1), {1, 0, 2, 4, 6})

#         self.__class__.score += 2

#     def test_eps_closure_2(self):
#         nfa = NFA(
#             {'1', '0'},
#             {1, 2, 3, 4, 5, 6},
#             1,
#             {
#                 (1, '1'): {2},
#                 (1, '0'): {5},
#                 (2, ''): {4},
#                 (2, '1'): {3},
#                 (3, '1'): {4},
#                 (5, ''): {2, 3},
#                 (5, '0'): {6},
#                 (6, '0'): {4}
#             },
#             {4},
#         )

#         self.assertCountEqual(nfa.epsilon_closure(5), {5, 2, 3, 4})

#         self.__class__.score += 2

#     def test_eps_closure_3(self):
#         nfa = NFA(
#             {'a', 'b'},
#             {0, 1, 2, 3, 4, 5, 6, 7},
#             0,
#             {
#                 (0, ''): {1},
#                 (1, ''): {2, 6},
#                 (2, 'a'): {3},
#                 (3, ''): {4},
#                 (4, 'b'): {5},
#                 (5, ''): {1},
#                 (6, 'a'): {7},
#                 (7, ''): {1}
#             },
#             {4}
#         )

#         self.assertCountEqual(nfa.epsilon_closure(1), {1, 2, 6})

#         self.__class__.score += 2

#     def test_single_non_accepting_state(self):
#         nfa = NFA({'a'}, {0}, 0, {}, set())

#         tests = [
#             ('', False),
#             ('a', False),
#             ('aa', False),
#             ('aaa', False)
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)

#         self.__class__.score += 2

#     def test_single_accepting_state_no_loops(self):
#         nfa = NFA({'a'}, {0}, 0, {}, {0})

#         tests = [
#             ('', True),
#             ('a', False),
#             ('aa', False),
#             ('aaa', False)
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)

#         self.__class__.score += 2

#     def test_dfa_1(self):
#         # reg = r'(a|(bb*a))(a|(bb*a))*'
#         nfa = NFA(
#             {'a', 'b'},
#             {0, 1, 2, 3},
#             0,
#             {
#                 (0, 'a'): {1},
#                 (0, ''): {2},
#                 (1, 'b'): {1},
#                 (1, 'a'): {2},
#                 (1, ''): {3},
#                 (2, ''): {3},
#                 (3, ''): {1},
#                 (3, 'a'): {2}
#             },
#             {2},
#         )

#         tests = [
#             ('aaaa', True),
#             ('bbbaaaabbaa', True),
#             ('ababababbbbaaab', False),
#             ('bbbbbbb', False),
#             ('abaaaaabab', False),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)

#         self.__class__.score += 4

#     def test_dfa_2(self):
#         nfa = NFA(
#             {'a', 'b'},
#             {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12},
#             0,
#             {
#                 (0, ''): {1, 5},
#                 (1, 'a'): {2},
#                 (2, 'b'): {3},
#                 (3, 'b'): {4},
#                 (4, ''): {12},
#                 (5, 'b'): {6},
#                 (6, ''): {7},
#                 (7, ''): {8, 11},
#                 (8, 'a'): {9},
#                 (9, 'b'): {10},
#                 (10, ''): {8, 11},
#                 (11, ''): {12},
#             },
#             {12},
#         )

#         tests = [
#             ('abb', True),
#             ('bbbaababaaaabbaa', False),
#             ('babababababab', True),
#             ('abbabbbabbababababb', False),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)

#         self.__class__.score += 4

#     def test_dfa_3(self):
#         nfa = NFA(
#             {'a', 'b'},
#             {0, 1, 2, 3},
#             0,
#             {
#                 (0, 'a'): {0, 1},
#                 (0, 'b'): {0},
#                 (1, 'a'): {2},
#                 (1, 'b'): {2},
#                 (2, 'a'): {3},
#                 (2, 'b'): {3},
#             },
#             {2, 3},
#         )

#         tests = [
#             ('abba', False),
#             ('bbbbabbabaa', True),
#             ('bbbbbbbbbba', False),
#             ('abababababababababababaab', True),
#             ('aaaaaaaabb', True),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)

#         self.__class__.score += 4

#     def test_dfa_4(self):
#         nfa = NFA(
#             {'a', 'b'},
#             {0, 1, 2, 3},
#             0,
#             {
#                 (0, 'a'): {1},
#                 (0, ''): {2},
#                 (1, 'a'): {2},
#                 (1, 'b'): {1},
#                 (1, ''): {3},
#                 (2, 'b'): {3},
#                 (3, 'a'): {2},
#                 (3, ''): {1},
#             },
#             {2},
#         )

#         tests = [
#             ('abbabbb', False),
#             ('abbbbbababababababbbbbbbba', True),
#             ('', True),
#             ('bababababa', True),
#             ('bbbbbbbbab', False),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)

#         self.__class__.score += 4

#     def test_dfa_5(self):
#         nfa = NFA(
#             {'0', '1'},
#             {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18},
#             0,
#             {
#                 (0, ''): {1, 3},
#                 (1, '1'): {2},
#                 (2, ''): {4},
#                 (3, ''): {4},
#                 (4, ''): {5},
#                 (5, ''): {6, 14},
#                 (6, '0'): {7},
#                 (7, ''): {8},
#                 (8, ''): {9, 11},
#                 (9, '0'): {10},
#                 (10, ''): {9, 11},
#                 (11, ''): {12},
#                 (12, '1'): {13},
#                 (13, ''): {6, 14},
#                 (14, ''): {15},
#                 (15, ''): {18, 16},
#                 (16, '0'): {17},
#                 (17, ''): {18, 16},
#             },
#             {18},
#         )

#         tests = [
#             ('00001', True),
#             ('100010000', True),
#             ('101001000100000000', True),
#             ('0000100000110000', False),
#             ('100010101010101000000001000', True),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)

#         self.__class__.score += 4

#     def test_dfa_6(self):
#         nfa = NFA(
#             {'0', '1'},
#             {0, 1, 2, 3, 4, 5, 6},
#             0,
#             {
#                 (0, '1'): {1},
#                 (0, ''): {1},
#                 (1, ''): {0, 2},
#                 (2, '0'): {3},
#                 (2, ''): {4},
#                 (3, '1'): {4},
#                 (4, ''): {2, 5},
#                 (5, ''): {6},
#                 (5, '1'): {6},
#                 (6, ''): {5}
#             },
#             {6},
#         )

#         tests = [
#             ('1011100', False),
#             ('0101111', True),
#             ('1111101010111', True),
#             ('01010100111', False),
#             ('1101111111', True),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)

#         self.__class__.score += 4

#     def test_dfa_7(self):
#         nfa = NFA(
#             {'0', '1'},
#             {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14},
#             1,
#             {
#                 (1, ''): {2, 11},
#                 (2, ''): {3, 5},
#                 (3, '1'): {4},
#                 (4, ''): {3, 5},
#                 (5, '0'): {6},
#                 (6, ''): {7, 9},
#                 (7, '1'): {8},
#                 (8, ''): {7, 9},
#                 (9, '0'): {10},
#                 (10, ''): {11},
#                 (11, ''): {12, 14},
#                 (12, '1'): {13},
#                 (13, ''): {12, 14}
#             },
#             {14},
#         )

#         tests = [
#             ('111111111111', True),
#             ('001111101010', False),
#             ('1111101110111111', True),
#             ('111011100010000101000', False),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)

#         self.__class__.score += 4

#     def test_dfa_8(self):
#         nfa = NFA(
#             {'a', 'b', 'c'},
#             {'s0', 's1', 's2', 's3'},
#             's0',
#             {
#                 ('s0', 'a'): {'s3'},
#                 ('s1', 'a'): {'s1', 's2'},
#                 ('s1', 'c'): {'s0', 's2'},
#                 ('s1', ''): {'s2'},
#                 ('s3', 'b'): {'s1'},
#                 ('s3', 'c'): {'s1', 's3'},
#                 ('s3', ''): {'s3'},
#             },
#             {'s1', 's2', 's3'},
#         )

#         tests = [
#             ('', False),
#             ('a', True),
#             ('b', False),
#             ('abaaaac', True),
#             ('abaaac', True),
#             ('abbaac', False),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)

#         self.__class__.score += 4

#     def test_dfa_9(self):
#         nfa = NFA(
#             {'a', 'b', 'c'},
#             {'s0', 's1', 's2', 's3'},
#             's0',
#             {
#                 ('s0', 'b'): {'s0', 's1'},
#                 ('s0', 'c'): {'s0', 's3'},
#                 ('s1', 'a'): {'s1', 's2'},
#                 ('s1', 'b'): {'s0'},
#                 ('s1', 'c'): {'s0'},
#                 ('s1', ''): {'s2'},
#                 ('s2', 'b'): {'s1', 's3'},
#                 ('s2', 'c'): {'s0', 's1'},
#                 ('s3', 'a'): {'s1'},
#                 ('s3', ''): {'s1', 's3'},
#             },
#             {'s2'},
#         )

#         tests = [
#             ('', False),
#             ('caaab', True),
#             ('caaa', True),
#             ('bababb', True),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)

#         self.__class__.score += 4

#     def test_dfa_10(self):
#         nfa = NFA(
#             {'a', 'b', 'c'},
#             {'s0', 's1', 's2', 's3'},
#             's0',
#             {
#                 ('s0', 'b') : {'s3'},
#                 ('s0', 'c') : {'s2'},
#                 ('s0', ''): {'s2', 's3'},
#                 ('s1', 'a') : {'s2', 's3'},
#                 ('s1', 'b') : {'s3'},
#                 ('s1', 'c') : {'s2', 's3'},
#                 ('s1', ''): {'s1', 's3'},
#                 ('s2', 'a') : {'s0'},
#                 ('s2', 'c') : {'s2'},
#                 ('s2', ''): {'s1'},
#                 ('s3', 'a') : {'s0', 's1'},
#                 ('s3', 'b') : {'s0', 's2'},
#             },
#             {'s1', 's2'},
#         )

#         tests = [
#             ('', True),
#             ('aaabcabc', True),
#             ('baabbac', True),
#             ('caccabab', True),
#             ('bbaab', True),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)

#         self.__class__.score += 4

#     def test_dfa_11(self):
#         nfa = NFA(
#             {'a', 'b', 'c'},
#             {'s0', 's1', 's2', 's3', 's4'},
#             's0',
#             {
#                 ('s0', 'b') : {'s2'},
#                 ('s0', 'c') : {'s3'},
#                 ('s1', 'a') : {'s1', 's4'},
#                 ('s1', 'b') : {'s0'},
#                 ('s1', 'c') : {'s2', 's3'},
#                 ('s1', ''): {'s3', 's4'},
#                 ('s2', 'a') : {'s2'},
#                 ('s2', ''): {'s1'},
#                 ('s3', 'b') : {'s1', 's3'},
#                 ('s3', 'c') : {'s0'},
#                 ('s3', ''): {'s3', 's4'},
#                 ('s4', 'b') : {'s1', 's4'},
#                 ('s4', ''): {'s1'},
#             },
#             {'s1', 's3', 's4'},
#         )

#         tests = [
#             ('', False),
#             ('aaabcabc', False),
#             ('baabbac', True),
#             ('caccabab', True),
#             ('bbaab', True),
#             ('babaabaabbc', True),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)
#         self.__class__.score += 4

#     def test_dfa_12(self):
#         nfa = NFA(
#             {'a', 'b', 'c'},
#             {'s0', 's1', 's2', 's3', 's4'},
#             's0',
#             {
#                 ('s0', 'a') : {'s3', 's4'},
#                 ('s0', 'c') : {'s2', 's3'},
#                 ('s0', ''): {'s1', 's4'},
#                 ('s1', 'a') : {'s2'},
#                 ('s1', 'b') : {'s4'},
#                 ('s1', 'c') : {'s0'},
#                 ('s2', 'a') : {'s3'},
#                 ('s2', 'b') : {'s0'},
#                 ('s2', 'c') : {'s3', 's4'},
#                 ('s2', ''): {'s3', 's4'},
#                 ('s3', 'a') : {'s3', 's4'},
#                 ('s3', 'b') : {'s2'},
#                 ('s3', 'c') : {'s4'},
#                 ('s3', ''): {'s0'},
#                 ('s4', 'a') : {'s3'},
#                 ('s4', 'b') : {'s2'},
#                 ('s4', 'c') : {'s2'},
#                 ('s4', ''): {'s4'},
#             },
#             {'s0', 's1', 's4'},
#         )

#         tests = [
#             ('', True),
#             ('a', True),
#             ('aaabcabc', True),
#             ('baabbac', True),
#             ('caccabab', True),
#             ('bbaab', True),
#             ('babaabaabbc', True),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)
#         self.__class__.score += 4

#     def test_dfa_13(self):
#         nfa = NFA(
#             {'a', 'b', 'c'},
#             {'s0', 's1', 's2', 's3', 's4'},
#             's0',
#             {
#                 ('s0', 'a') : {'s1', 's4'},
#                 ('s0', 'b') : {'s3', 's4'},
#                 ('s0', ''): {'s0'},
#                 ('s1', 'a') : {'s1', 's3'},
#                 ('s1', 'b') : {'s3', 's4'},
#                 ('s1', 'c') : {'s3'},
#                 ('s2', 'a') : {'s4'},
#                 ('s2', 'b') : {'s0'},
#                 ('s3', 'a') : {'s0', 's2'},
#                 ('s3', 'b') : {'s2', 's3'},
#                 ('s3', 'c') : {'s0', 's1'},
#                 ('s3', ''): {'s1'},
#                 ('s4', 'b') : {'s1', 's4'},
#             },
#             {'s0', 's1', 's2', 's4'},
#         )

#         tests = [
#             ('', True),
#             ('aaabcabc', True),
#             ('baabbac', True),
#             ('caccabab', False),
#             ('bbaab', True),
#             ('babaabaabbc', True),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)
#         self.__class__.score += 4

#     def test_dfa_14(self):
#         nfa = NFA(
#             {'a', 'b', 'c', 'd'},
#             {'s0', 's1', 's2', 's3', 's4', 's5'},
#             's0',
#             {
#                 ('s0', 'a') : {'s0', 's4'},
#                 ('s0', 'b') : {'s4'},
#                 ('s0', 'c') : {'s1'},
#                 ('s1', 'a') : {'s2'},
#                 ('s1', 'c') : {'s4'},
#                 ('s1', ''): {'s2'},
#                 ('s2', 'a') : {'s2', 's3'},
#                 ('s2', 'b') : {'s2'},
#                 ('s2', 'c') : {'s5'},
#                 ('s2', 'd') : {'s2', 's3'},
#                 ('s2', ''): {'s0'},
#                 ('s3', 'b') : {'s5'},
#                 ('s3', 'd') : {'s0', 's3'},
#                 ('s3', ''): {'s2'},
#                 ('s4', 'a') : {'s4', 's5'},
#                 ('s4', 'b') : {'s5'},
#                 ('s4', 'c') : {'s0', 's1'},
#                 ('s4', 'd') : {'s1', 's3'},
#                 ('s4', ''): {'s5'},
#                 ('s5', 'a') : {'s5'},
#                 ('s5', 'd') : {'s5'},
#                 ('s5', ''): {'s4'},
#             },
#             {'s0', 's2', 's3'},
#         )

#         tests = [
#             ('', True),
#             ('abcdbdb', True),
#             ('baabbac', True),
#             ('caccabab', True),
#             ('dabbab', False),
#             ('babaabaabbc', True),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)
#         self.__class__.score += 4

#     def test_dfa_15(self):
#         nfa = NFA(
#             {'a', 'b', 'c', 'd'},
#             {'s0', 's1', 's2', 's3', 's4', 's5'},
#             's0',
#             {
#                 ('s0', 'a') : {'s1'},
#                 ('s0', 'c') : {'s4'},
#                 ('s0', 'd') : {'s0', 's5'},
#                 ('s0', ''): {'s1'},
#                 ('s1', 'c') : {'s2'},
#                 ('s1', 'd') : {'s4', 's5'},
#                 ('s2', 'b') : {'s1', 's3'},
#                 ('s2', 'c') : {'s3'},
#                 ('s2', 'd') : {'s4'},
#                 ('s3', 'a') : {'s2', 's3'},
#                 ('s3', 'b') : {'s1', 's2'},
#                 ('s3', 'c') : {'s4', 's5'},
#                 ('s3', ''): {'s2'},
#                 ('s4', 'a') : {'s1'},
#                 ('s4', 'b') : {'s2', 's5'},
#                 ('s5', 'a') : {'s3', 's5'},
#                 ('s5', 'b') : {'s0', 's1'},
#                 ('s5', 'c') : {'s0'},
#                 ('s5', ''): {'s1'},
#             },
#             {'s2', 's3', 's5'},
#         )

#         tests = [
#             ('', False),
#             ('abcdbdb', False),
#             ('baabbac', False),
#             ('caccabab', True),
#             ('dabbab', True),
#             ('babaabaabbc', False),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)
#         self.__class__.score += 4

#     def test_dfa_16(self):
#         nfa = NFA(
#             {'a', 'b', 'c', 'd'},
#             {'s0', 's1', 's2', 's3', 's4', 's5'},
#             's0',
#             {
#                 ('s0', 'c') : {'s2', 's3'},
#                 ('s0', 'd') : {'s2'},
#                 ('s1', 'a') : {'s3', 's5'},
#                 ('s1', 'b') : {'s4', 's5'},
#                 ('s1', 'd') : {'s3', 's5'},
#                 ('s1', ''): {'s3'},
#                 ('s2', 'd') : {'s3', 's4'},
#                 ('s2', ''): {'s1', 's4'},
#                 ('s3', 'b') : {'s4', 's5'},
#                 ('s3', ''): {'s3', 's5'},
#                 ('s4', 'a') : {'s4'},
#                 ('s4', 'b') : {'s1'},
#                 ('s4', ''): {'s5'},
#                 ('s5', 'a') : {'s3', 's5'},
#                 ('s5', 'b') : {'s2'},
#                 ('s5', 'c') : {'s4', 's5'},
#                 ('s5', 'd') : {'s4', 's5'},
#                 ('s5', ''): {'s1'},
#             },
#             {'s0', 's4'},
#         )

#         tests = [
#             ('', True),
#             ('abc', False),
#             ('babab', False),
#             ('caccabab', True),
#             ('dabbab', True),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)
#         self.__class__.score += 4

#     def test_dfa_17(self):
#         nfa = NFA(
#             {'a', 'b', 'c', 'd'},
#             {'s0', 's1', 's2', 's3', 's4', 's5', 's6'},
#             's0',
#             {
#                 ('s0', 'a') : {'s1'},
#                 ('s0', 'b') : {'s5'},
#                 ('s0', 'd') : {'s4', 's5'},
#                 ('s1', 'b') : {'s0'},
#                 ('s1', 'c') : {'s3', 's5'},
#                 ('s1', 'd') : {'s3', 's4'},
#                 ('s2', 'a') : {'s4', 's5'},
#                 ('s2', 'b') : {'s4'},
#                 ('s2', 'c') : {'s0'},
#                 ('s2', 'd') : {'s1', 's6'},
#                 ('s3', 'a') : {'s6'},
#                 ('s3', 'b') : {'s1', 's2'},
#                 ('s3', 'c') : {'s4'},
#                 ('s3', 'd') : {'s5', 's6'},
#                 ('s3', ''): {'s0', 's3'},
#                 ('s4', 'a') : {'s1'},
#                 ('s4', 'b') : {'s1', 's3'},
#                 ('s4', 'd') : {'s1'},
#                 ('s4', ''): {'s3', 's6'},
#                 ('s5', 'a') : {'s1'},
#                 ('s5', 'b') : {'s4', 's5'},
#                 ('s5', 'c') : {'s3', 's5'},
#                 ('s5', 'd') : {'s6'},
#                 ('s6', 'a') : {'s1', 's3'},
#                 ('s6', 'd') : {'s1'},
#                 ('s6', ''): {'s3'},
#             },
#             {'s0', 's1', 's2', 's4', 's5', 's6'},
#         )

#         tests = [
#             ('', True),
#             ('abc', False),
#             ('babab', True),
#             ('caccabab', False),
#             ('dabbab', True),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)
#         self.__class__.score += 4

#     def test_dfa_18(self):
#         nfa = NFA(
#             {'a', 'b', 'c', 'd', 'e'},
#             {'s0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9'},
#             's0',
#             {
#                 ('s0', 'c') : {'s3'},
#                 ('s0', ''): {'s9'},
#                 ('s1', 'b') : {'s8'},
#                 ('s1', 'c') : {'s3'},
#                 ('s1', 'd') : {'s1'},
#                 ('s1', 'e') : {'s5'},
#                 ('s1', ''): {'s7'},
#                 ('s2', 'c') : {'s6'},
#                 ('s2', 'd') : {'s6'},
#                 ('s2', ''): {'s3'},
#                 ('s3', 'a') : {'s4'},
#                 ('s3', 'b') : {'s5'},
#                 ('s3', 'c') : {'s0'},
#                 ('s3', 'd') : {'s6'},
#                 ('s3', 'e') : {'s0'},
#                 ('s3', ''): {'s3'},
#                 ('s4', 'a') : {'s4'},
#                 ('s4', 'b') : {'s2'},
#                 ('s4', ''): {'s5'},
#                 ('s5', 'b') : {'s1'},
#                 ('s5', 'c') : {'s2'},
#                 ('s5', 'd') : {'s9'},
#                 ('s5', 'e') : {'s9'},
#                 ('s5', ''): {'s0'},
#                 ('s6', 'b') : {'s5'},
#                 ('s6', ''): {'s2'},
#                 ('s7', 'c') : {'s7'},
#                 ('s7', 'e') : {'s2'},
#                 ('s8', 'b') : {'s8'},
#                 ('s8', 'c') : {'s0'},
#                 ('s8', 'd') : {'s1'},
#                 ('s8', ''): {'s2'},
#                 ('s9', 'b') : {'s5'},
#                 ('s9', 'e') : {'s3'},
#             },
#             {'s2', 's3', 's6'},
#         )

#         tests = [
#             ('', False),
#             ('abc', False),
#             ('cccab', True),
#             ('abcabc', False),
#             ('bdeaabcbc', True),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)
#         self.__class__.score += 4

#     def test_dfa_19(self):
#         nfa = NFA(
#             {'a', 'b', 'c', 'd', 'e'},
#             {'s0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11'},
#             's0',
#             {
#                 ('s0', 'b') : {'s1'},
#                 ('s0', 'c') : {'s7'},
#                 ('s0', 'e') : {'s1'},
#                 ('s0', ''): {'s1'},
#                 ('s1', 'a') : {'s9'},
#                 ('s1', 'c') : {'s7'},
#                 ('s3', 'c') : {'s10'},
#                 ('s3', 'd') : {'s11'},
#                 ('s4', 'b') : {'s11'},
#                 ('s4', 'd') : {'s9'},
#                 ('s5', 'a') : {'s5'},
#                 ('s5', 'b') : {'s5'},
#                 ('s5', 'c') : {'s7'},
#                 ('s5', 'e') : {'s6'},
#                 ('s6', 'b') : {'s2'},
#                 ('s6', 'c') : {'s3'},
#                 ('s6', 'd') : {'s3'},
#                 ('s6', 'e') : {'s4'},
#                 ('s6', ''): {'s10'},
#                 ('s7', 'b') : {'s9'},
#                 ('s7', 'c') : {'s7'},
#                 ('s7', 'e') : {'s2'},
#                 ('s8', 'a') : {'s0'},
#                 ('s8', 'b') : {'s9'},
#                 ('s8', 'd') : {'s11'},
#                 ('s8', 'e') : {'s5'},
#                 ('s9', 'a') : {'s10'},
#                 ('s9', 'b') : {'s7'},
#                 ('s9', 'c') : {'s1'},
#                 ('s9', ''): {'s1'},
#                 ('s10', 'a') : {'s11'},
#                 ('s10', 'd') : {'s5'},
#                 ('s10', 'e') : {'s10'},
#                 ('s11', 'b') : {'s8'},
#                 ('s11', ''): {'s9'},
#             },
#             {'s4', 's5', 's6', 's7', 's8'},
#         )

#         tests = [
#             ('', False),
#             ('abc', True),
#             ('caccabab', False),
#             ('debabc', False),
#             ('d', False),
#             ('bccbaeed', True),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)
#         self.__class__.score += 4

#     def test_dfa_20(self):
#         nfa = NFA(
#             {'a', 'b', 'c', 'd', 'e'},
#             {'s0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14', 's15'},
#             's0',
#             {
#                 ('s0', 'a') : {'s5'},
#                 ('s0', 'c') : {'s15'},
#                 ('s0', 'd') : {'s10'},
#                 ('s0', 'e') : {'s2'},
#                 ('s0', ''): {'s11'},
#                 ('s1', 'a') : {'s6'},
#                 ('s1', 'e') : {'s2'},
#                 ('s1', ''): {'s11'},
#                 ('s2', 'a') : {'s7'},
#                 ('s2', 'd') : {'s12'},
#                 ('s2', 'e') : {'s3'},
#                 ('s3', 'a') : {'s3'},
#                 ('s3', 'c') : {'s8'},
#                 ('s3', 'd') : {'s1'},
#                 ('s3', ''): {'s2'},
#                 ('s4', 'a') : {'s13'},
#                 ('s4', 'c') : {'s5'},
#                 ('s4', 'e') : {'s4'},
#                 ('s5', 'a') : {'s7'},
#                 ('s5', 'e') : {'s12'},
#                 ('s6', 'a') : {'s12'},
#                 ('s6', 'd') : {'s14'},
#                 ('s6', ''): {'s3'},
#                 ('s7', 'a') : {'s14'},
#                 ('s7', 'd') : {'s9'},
#                 ('s7', 'e') : {'s4'},
#                 ('s7', ''): {'s12'},
#                 ('s8', 'b') : {'s7'},
#                 ('s8', 'c') : {'s11'},
#                 ('s8', 'e') : {'s11'},
#                 ('s9', 'b') : {'s1'},
#                 ('s9', 'd') : {'s10'},
#                 ('s9', 'e') : {'s11'},
#                 ('s10', 'b') : {'s15'},
#                 ('s10', ''): {'s12'},
#                 ('s11', 'b') : {'s11'},
#                 ('s11', 'd') : {'s1'},
#                 ('s11', 'e') : {'s7'},
#                 ('s12', 'd') : {'s15'},
#                 ('s12', 'e') : {'s10'},
#                 ('s13', 'a') : {'s12'},
#                 ('s13', 'd') : {'s3'},
#                 ('s14', 'b') : {'s8'},
#                 ('s14', 'd') : {'s6'},
#                 ('s14', 'e') : {'s13'},
#                 ('s14', ''): {'s11'},
#                 ('s15', 'e') : {'s8'},
#                 ('s15', ''): {'s6'},
#             },
#             {'s3', 's4', 's6', 's7', 's8', 's9', 's10', 's11'},
#         )

#         tests = [
#             ('', True),
#             ('aeebae', True),
#             ('dbdedaa', True),
#             ('abc', False),
#             ('babab', False),
#             ('caccabab', False),
#             ('dabbab', False),
#         ]

#         dfa = nfa.subset_construction()
#         self.structural_check(dfa)
#         self.behaviour_check(dfa, tests)
#         self.__class__.score += 4

