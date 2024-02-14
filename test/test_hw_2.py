# import itertools
# import math
# import time
# import unittest

# from src.DFA import DFA
# from src.NFA import NFA
# from src.Regex import parse_regex

# from typing import Iterable


# class HW2Tests(unittest.TestCase):
#     score: int

#     def __init__(self, methodName: str = "runTest") -> None:
#         super().__init__(methodName)
#         self.__class__.score = 10 

#     @classmethod
#     def tearDownClass(cls):
#         print('\nHomework 2 - Total score:', cls.score, '/ 100\n')

#     def behaviour_check(self, regex: str, tests: Iterable[tuple[str, bool]]) -> None:
#         dfa = parse_regex(regex).thompson().subset_construction()
#         for s, ref in tests:
#             self.assertEqual(
#                 dfa.accept(s), ref,
#                 f'regex has unexpected behaviour on "{s}".'
#                 f' expected: {"accept" if ref else "reject"}'
#             )

#     def test_character(self):
#         regex = 'a'

#         tests = [
#             ('', False),
#             ('a', True),
#             ('aa', False),
#             ('aaaaaaaaa', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_concat_1(self):
#         regex = 'aa!'

#         tests = [
#             ('', False),
#             ('a', False),
#             ('aa', True),
#             ('aaaaaaaaa', False),
#             ('aaaaaaaaaa', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_concat_2(self):
#         regex = 'ab!'

#         tests = [
#             ('', False),
#             ('a', False),
#             ('aa', False),
#             ('ab', True),
#             ('b', False),
#             ('ba', False),
#             ('bb', False),
#             ('abab', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_union(self):
#         regex = 'a | b'

#         tests = [
#             ('', False),
#             ('a', True),
#             ('b', True),
#             ('aa', False),
#             ('ab', False),
#             ('bb', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_concat_union_1(self):
#         regex = 'ca | cb'

#         tests = [
#             ('', False),
#             ('c', False),
#             ('ca', True),
#             ('cb', True),
#             ('ccb', False),
#             ('cab', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_concat_union_2(self):
#         regex = 'c(a | b)'

#         tests = [
#             ('', False),
#             ('c', False),
#             ('ca', True),
#             ('cb', True),
#             ('ccb', False),
#             ('cab', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_kleene_star(self):
#         regex = 'a*'

#         tests = [
#             ('', True),
#             ('a', True),
#             ('aa', True),
#             ('aaaaaaaaa', True),
#             ('b', False),
#             ('ab', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_concat_kleene_star(self):
#         regex = '(ab)*'

#         tests = [
#             ('', True),
#             ('a', False),
#             ('aa', False),
#             ('aaaaaaaaa', False),
#             ('b', False),
#             ('ab', True),
#             ('abab', True),
#             ('ababababab', True),
#             ('abababababab', True),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_union_kleene_star(self):
#         regex = '(a | b)*'

#         tests = [
#             ('', True),
#             ('a', True),
#             ('b', True),
#             ('aa', True),
#             ('ab', True),
#             ('bb', True),
#             ('abab', True),
#             ('ababababab', True),
#             ('c', False),
#             ('ababc', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_concat_union_kleene_star_1(self):
#         regex = 'c(a | b)*'
        
#         tests = [
#             ('', False),
#             ('c', True),
#             ('ca', True),
#             ('cb', True),
#             ('cababa', True),
#             ('cabababcabab', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_concat_union_kleene_star_2(self):
#         regex = '(ab | cd)*'

#         tests = [
#             ('', True),
#             ('a', False),
#             ('aa', False),
#             ('ab', True),
#             ('cd', True),
#             ('abab', True),
#             ('cdcd', True),
#             ('abcdab', True),
#             ('abcbcd', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_optional(self):
#         regex = 'a?'

#         tests = [
#             ('', True),
#             ('a', True),
#             ('aa', False),
#             ('aaaaaaaaa', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_complex_optional(self):
#         regex = 'c(a | b)?'

#         tests = [
#             ('', False),
#             ('ca', True),
#             ('cb', True),
#             ('cababa', False),
#             ('c', True),
#             ('cabababcabab', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_plus(self):
#         regex = 'a+'

#         tests = [
#             ('', False),
#             ('a', True),
#             ('aa', True),
#             ('aaaaaaaaa', True),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_complex_plus(self):
#         regex = 'c(a | b)+'

#         tests = [
#             ('', False),
#             ('ca', True),
#             ('cb', True),
#             ('cababa', True),
#             ('c', False),
#             ('cabababcabab', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_digit(self):
#         regex = "[0-9]"

#         tests = [
#             ('', False),
#             ('0', True),
#             ('1', True),
#             ('9', True),
#             ('10', False),
#             ('a', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_digits(self):
#         regex = "[0-9]+"

#         tests = [
#             ('', False),
#             ('0', True),
#             ('1', True),
#             ('9', True),
#             ('10', True),
#             ('a', False),
#             ('123456789', True),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_small_letter(self):
#         regex = "[a-z]"

#         tests = [
#             ('', False),
#             ('a', True),
#             ('b', True),
#             ('z', True),
#             ('A', False),
#             ('0', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_small_letters(self):
#         regex = "[a-z]+"

#         tests = [
#             ('', False),
#             ('a', True),
#             ('b', True),
#             ('z', True),
#             ('A', False),
#             ('0', False),
#             ('abc', True),
#             ('abcABC', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_big_letter(self):
#         regex = "[A-Z]"

#         tests = [
#             ('', False),
#             ('A', True),
#             ('B', True),
#             ('Z', True),
#             ('a', False),
#             ('0', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_big_letters(self):
#         regex = "[A-Z]+"

#         tests = [
#             ('', False),
#             ('A', True),
#             ('B', True),
#             ('Z', True),
#             ('a', False),
#             ('0', False),
#             ('ABC', True),
#             ('abcABC', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 2

#     def test_1(self):
#         regex = '(ab | cd+ | b*)? efg'

#         tests = [
#             ('', False),
#             ('abefg', True),
#             ('abefg', True),
#             ('cefg', False),
#             ('cdddefg', True),
#             ('efg', True),
#             ('bbbbefg', True),
#             ('abcdefg', False),
#             ('efghijkl', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 3

#     def test_2(self):
#         regex = r'[a-z]*\ [a-z]*'

#         tests = [
#             ('hello world', True),
#             ('ana are mere', False),
#             ('come on barbie lets go party', False),
#         ]
        
#         self.behaviour_check(regex, tests)

#         self.__class__.score += 3

#     def test_3(self):
#         regex = '(\n|[a-z])*'

#         tests = [
#             ('hello\nworld', True),
#             ('ana\nare\nare', True),
#             ('come\ton\tbarbie\tlet\tsgo\tparty', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 3

#     def test_4(self):
#         regex = '(a|(bb*a))(a|(bb*a))*'

#         tests = [
#             ('bba', True),
#             ('bbba', True),
#             ('bbbaaaabbaa', True),
#             ('ababababbbbaaab', False),
#             ('bbbbbbb', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 3

#     def test_5(self):
#         regex = '[A-Z]?([a-z]*[0-9])*'
            
#         tests = [
#             ('Test12345', True),
#             ('Class0homework2', True),
#             ('variable', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 3

#     def test_6(self):
#         regex = '(a|b)*c(a|b)*c(a|b)*'

#         tests = [
#             ('abccba', True),
#             ('abcbcbabab', True),
#             ('abcbacbacbacbacb', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 3

#     def test_7(self):
#         regex = 'a(b|c)(d|e)|abb|abc'

#         tests = [
#             ('abd', True),
#             ('abe', True),
#             ('abb', True),
#             ('abc', True),
#             ('acd', True),
#             ('ace', True),
#             ('ade', False),
#             ('ab', False),
#             ('abcd', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 3

#     def test_8(self):
#         regex = r'class\ ([A-Z][a-z]*)+\(([A-Z][a-z]*)*\):'

#         tests = [
#             ('class Apple():', True),
#             ('class Apple(Fruit):', True),
#             ('cls Apple():', False),
#             ('class Apple:', False),
#             ('class apple():', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 3

#     def test_9(self):
#         regex = '(this_needs_to_match_a_really_long_string_or_nothing)?'

#         tests = [
#             ('this_needs_to_match_a_really_long_string_or_nothing', True),
#             ('', True),
#             ('this_is_some_other_string_that_does_not_match', False),
#             ('this_needs_to_match_a_really_long_string_or_nothing_and_some_more', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 3

#     def test_10(self):
#         regex = '([A-Z]|[a-z]|[0-9])+@[a-z]+.[a-z]+'

#         tests = [
#             ('profesor@upb.ro', True),
#             ('student@stud.acs.upb.ro', False),
#             ('this_is_not_a_email_lol', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 3

#     def test_11(self):
#         regex = '((-|.)(-|.)(-|.))|(.(-|.)(--|-.|..))|(-(-.|..|.-)(-|.))'

#         tests = [
#             ('...', True),
#             ('---', True),
#             ('-..', True),
#             ('-.-', True),
#             ('--..', True),
#             ('-...', True),
#             ('..-.', True),
#             ('----', False),
#             ('---.', False),
#             ('.-.-', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 3

#     def test_12(self):
#         regex = r'((((-|.)(-|.)(-|.))|(.(-|.)(--|-.|..))|(-(-.|..|.-)(-|.)))\ )+'

#         tests = [
#             ('... --- ... ', True),
#             ('-.. -.- -.. ', True),
#             ('-.- -.- -.- ', True),
#             ('-.. -.- -.. -.- -.- -.. ', True),
#             ('... ---- ... ', False),
#             ('.-.- ', False),
#             ('-... ---. ...', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 3

#     def test_13(self):
#         # you will understand if you take IOC
#         regex = r'([a-z]+\ )+vrea\ sa(\ [a-z]+)+'

#         tests = [
#             ('vlad vrea sa vada cand vine mancarea pe aplicatie', True),
#             ('ion vrea sa cheltuiasca mai putin', True),
#             ('maria are nevoie de ajutor', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 3

#     def test_14(self):
#         regex = '[a-z]+([A-Z][a-z]+)*'

#         tests = [
#             ('camelCase', True),
#             ('someLongerCamelCase', True),
#             ('PascalCase', False),
#             ('snake_case', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 3

#     def test_15(self):
#         regex = '[0-9]+((\+|-)[0-9]+)*'

#         tests = [
#             ('1+2+3', True),
#             ('3-7', True),
#             ('4+1-7+4+2+1', True),
#             ('11+23-45+67', True),
#             ('100', True),
#             ('-11+33', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 3

#     def test_16(self):
#         regex = '\/\*([A-Z]|[a-z]|[0-9]|\ )*\*\/'

#         tests = [
#             ('/* comments are allowed */', True),
#             ('/* anything between slashes really */', True),
#             ('/* but it has to be comment */ and not after', False),
#             ('or before /* something */', False),
#             ('/* and slashes cannot be missing', False),
#         ]

#         self.behaviour_check(regex, tests)

#         self.__class__.score += 3

