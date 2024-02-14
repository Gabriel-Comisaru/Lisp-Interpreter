import unittest
from src.Lexer import Lexer


def verify(lexer: Lexer, tests):
	results = []
	for word, ref in tests:
		results.append(lexer.lex(word) == ref)
	return results


class HW3Tests(unittest.TestCase):
	def __init__(self, methodName: str = "runTest") -> None:
		super().__init__(methodName)
		self.__class__.score = 0

	@classmethod
	def tearDownClass(cls):
		print("\nHomework 3 - Total score:", cls.score, "/ 150\n")

	def test_1_basic(self):
		spec = [("one", "1"), ("zero", "0")]

		lexer = Lexer(spec)

		tests = [
			(
				"1011011",
				[
					("one", "1"),
					("zero", "0"),
					("one", "1"),
					("one", "1"),
					("zero", "0"),
					("one", "1"),
					("one", "1"),
				],
			),
			(
				"10101",
				[
					("one", "1"),
					("zero", "0"),
					("one", "1"),
					("zero", "0"),
					("one", "1"),
				],
			)
		]

		results = verify(lexer, tests)

		print(f"test01: {results}")
		assert all(results)
		self.__class__.score += 10

	def test_2_max_munch(self):
		spec = [("ones", "11+"), ("pair", "01|10"), ("other", "0|1")]

		lexer = Lexer(spec)

		tests = [
			(
				"1011011",
				[("pair", "10"), ("ones", "11"), ("pair", "01"), ("other", "1")],
			),
			("10101", [("pair", "10"), ("pair", "10"), ("other", "1")]),
			("1001", [("pair", "10"), ("pair", "01")]),
		]

		results = verify(lexer, tests)

		print(f"test02: {results}")
		assert all(results)
		self.__class__.score += 10

	def test_3_big(self):
		spec = [("SPACE", "\\ "), ("ZEROS", "0+")]

		lexer = Lexer(spec)

		tests = [
			("0000 0", [("ZEROS", "0000"), ("SPACE", " "), ("ZEROS", "0")]),
			(" 0000 ", [("SPACE", " "), ("ZEROS", "0000"), ("SPACE", " ")]),
			(
				"00000000000000000000000000000000000000",
				[("ZEROS", "00000000000000000000000000000000000000")],
			),
			(
				"0 00 000 0000 000 000 00 0 ",
				[
					("ZEROS", "0"),
					("SPACE", " "),
					("ZEROS", "00"),
					("SPACE", " "),
					("ZEROS", "000"),
					("SPACE", " "),
					("ZEROS", "0000"),
					("SPACE", " "),
					("ZEROS", "000"),
					("SPACE", " "),
					("ZEROS", "000"),
					("SPACE", " "),
					("ZEROS", "00"),
					("SPACE", " "),
					("ZEROS", "0"),
					("SPACE", " "),
				],
			),
		]

		results = verify(lexer, tests)

		print(f"test03: {results}")
		assert all(results)
		self.__class__.score += 10

	def test_4_big(self):
		spec = [("TWO", "2"), ("PATTERN", "11*(00)*101(0|1)(0|1)*")]

		lexer = Lexer(spec)

		tests = [
			("1001010", [("PATTERN", "1001010")]),
			("1101010101", [("PATTERN", "1101010101")]),
			("2110000101112", [("TWO", "2"), ("PATTERN", "11000010111"), ("TWO", "2")]),
			(
				"111100001010211011",
				[("PATTERN", "111100001010"), ("TWO", "2"), ("PATTERN", "11011")],
			),
			(
				"100101001011211010101012",
				[
					("PATTERN", "100101001011"),
					("TWO", "2"),
					("PATTERN", "1101010101"),
					("TWO", "2"),
				],
			),
			(
				"2100001010021001011",
				[
					("TWO", "2"),
					("PATTERN", "1000010100"),
					("TWO", "2"),
					("PATTERN", "1001011"),
				],
			),
			(
				"21101121101021000010112",
				[
					("TWO", "2"),
					("PATTERN", "11011"),
					("TWO", "2"),
					("PATTERN", "11010"),
					("TWO", "2"),
					("PATTERN", "100001011"),
					("TWO", "2"),
				],
			),
			(
				"100101112110111112100101002",
				[
					("PATTERN", "10010111"),
					("TWO", "2"),
					("PATTERN", "11011111"),
					("TWO", "2"),
					("PATTERN", "10010100"),
					("TWO", "2"),
				],
			),
			(
				"2211100000010111011000110110010022",
				[
					("TWO", "2"),
					("TWO", "2"),
					("PATTERN", "111000000101110110001101100100"),
					("TWO", "2"),
					("TWO", "2"),
				],
			),
			(
				"2100101121101112110101012100001011211011110111101",
				[
					("TWO", "2"),
					("PATTERN", "1001011"),
					("TWO", "2"),
					("PATTERN", "110111"),
					("TWO", "2"),
					("PATTERN", "11010101"),
					("TWO", "2"),
					("PATTERN", "100001011"),
					("TWO", "2"),
					("PATTERN", "11011110111101"),
				],
			),
		]

		results = verify(lexer, tests)

		print(f"test04: {results}")
		assert all(results)
		self.__class__.score += 10

	def test_5_big(self):
		spec = [("C", "c"), ("ABS", "(ab)+"), ("BS", "b*")]

		lexer = Lexer(spec)

		tests = [
			("ab", [("ABS", "ab")]),
			("bbbbb", [("BS", "bbbbb")]),
			("abababcb", [("ABS", "ababab"), ("C", "c"), ("BS", "b")]),
			("bbab", [("BS", "bb"), ("ABS", "ab")]),
			(
				"bbbcbbabbc",
				[
					("BS", "bbb"),
					("C", "c"),
					("BS", "bb"),
					("ABS", "ab"),
					("BS", "b"),
					("C", "c"),
				],
			),
			(
				"cbababbc",
				[("C", "c"), ("BS", "b"), ("ABS", "abab"), ("BS", "b"), ("C", "c")],
			),
			(
				"ababcbbbcbabbcabbab",
				[
					("ABS", "abab"),
					("C", "c"),
					("BS", "bbb"),
					("C", "c"),
					("BS", "b"),
					("ABS", "ab"),
					("BS", "b"),
					("C", "c"),
					("ABS", "ab"),
					("BS", "b"),
					("ABS", "ab"),
				],
			),
			(
				"cbbbbcbbabcabbbabb",
				[
					("C", "c"),
					("BS", "bbbb"),
					("C", "c"),
					("BS", "bb"),
					("ABS", "ab"),
					("C", "c"),
					("ABS", "ab"),
					("BS", "bb"),
					("ABS", "ab"),
					("BS", "b"),
				],
			),
			(
				"ababbbbabcabbababcb",
				[
					("ABS", "abab"),
					("BS", "bbb"),
					("ABS", "ab"),
					("C", "c"),
					("ABS", "ab"),
					("BS", "b"),
					("ABS", "abab"),
					("C", "c"),
					("BS", "b"),
				],
			),
			(
				"cbbbabcabbabcbbcababab",
				[
					("C", "c"),
					("BS", "bbb"),
					("ABS", "ab"),
					("C", "c"),
					("ABS", "ab"),
					("BS", "b"),
					("ABS", "ab"),
					("C", "c"),
					("BS", "bb"),
					("C", "c"),
					("ABS", "ababab"),
				],
			),
		]

		results = verify(lexer, tests)

		print(f"test05: {results}")
		assert all(results)
		self.__class__.score += 10

	def test_6_big(self):
		spec = [
			("SPACE", "\\ "),
			("NEWLINE", "\n"),
			("PATTERN1", "1\\ 0"),
			("PATTERN2", "(10)*\\ "),
			("PATTERN3", "\\ 001\\ "),
			("PATTERN4", "(101\\ )+"),
			("PATTERN5", "1*01"),
		]

		lexer = Lexer(spec)

		tests = [
			("1 0", [("PATTERN1", "1 0")]),
			("101010 ", [("PATTERN2", "101010 ")]),
			(
				"101010 1 0 1 0",
				[
					("PATTERN2", "101010 "),
					("PATTERN1", "1 0"),
					("SPACE", " "),
					("PATTERN1", "1 0"),
				],
			),
			(
				"1 0 001 1 010 ",
				[
					("PATTERN1", "1 0"),
					("PATTERN3", " 001 "),
					("PATTERN1", "1 0"),
					("PATTERN2", "10 "),
				],
			),
			(
				"1 0 \n  001 1 0",
				[
					("PATTERN1", "1 0"),
					("SPACE", " "),
					("NEWLINE", "\n"),
					("SPACE", " "),
					("PATTERN3", " 001 "),
					("PATTERN1", "1 0"),
				],
			),
			(
				"101 101 1 01010  ",
				[
					("PATTERN4", "101 101 "),
					("PATTERN1", "1 0"),
					("PATTERN2", "1010 "),
					("SPACE", " "),
				],
			),
			(
				"101 101\n  001   001  101010 ",
				[
					("PATTERN4", "101 "),
					("PATTERN5", "101"),
					("NEWLINE", "\n"),
					("SPACE", " "),
					("PATTERN3", " 001 "),
					("SPACE", " "),
					("PATTERN3", " 001 "),
					("SPACE", " "),
					("PATTERN2", "101010 "),
				],
			),
			(
				"11101\n1 0  001 101  ",
				[
					("PATTERN5", "11101"),
					("NEWLINE", "\n"),
					("PATTERN1", "1 0"),
					("SPACE", " "),
					("PATTERN3", " 001 "),
					("PATTERN4", "101 "),
					("SPACE", " "),
				],
			),
			(
				"101\n1 01111101\n 1010 101 101    001 ",
				[
					("PATTERN5", "101"),
					("NEWLINE", "\n"),
					("PATTERN1", "1 0"),
					("PATTERN5", "1111101"),
					("NEWLINE", "\n"),
					("SPACE", " "),
					("PATTERN2", "1010 "),
					("PATTERN4", "101 101 "),
					("SPACE", " "),
					("SPACE", " "),
					("PATTERN3", " 001 "),
				],
			),
		]

		results = verify(lexer, tests)

		print(f"test06: {results}")
		assert all(results)
		self.__class__.score += 10

	def test_7_big(self):
		spec = [
			("SPACE", "\\ "),
			("DS", "d+"),
			("ABS", "(ab)*"),
			("ABCORC", "(abc)|c"),
			("APLUSCD", "(a+)cd"),
			("ABD", "abd"),
		]

		lexer = Lexer(spec)

		tests = [
			(
				" acdaacdabd",
				[
					("SPACE", " "),
					("APLUSCD", "acd"),
					("APLUSCD", "aacd"),
					("ABD", "abd"),
				],
			),
			(
				"abdabc abd ababab ",
				[
					("ABD", "abd"),
					("ABCORC", "abc"),
					("SPACE", " "),
					("ABD", "abd"),
					("SPACE", " "),
					("ABS", "ababab"),
					("SPACE", " "),
				],
			),
			(
				"abababababab ababab c aaacd abd ",
				[
					("ABS", "abababababab"),
					("SPACE", " "),
					("ABS", "ababab"),
					("SPACE", " "),
					("ABCORC", "c"),
					("SPACE", " "),
					("APLUSCD", "aaacd"),
					("SPACE", " "),
					("ABD", "abd"),
					("SPACE", " "),
				],
			),
			(
				"abd c abababab",
				[
					("ABD", "abd"),
					("SPACE", " "),
					("ABCORC", "c"),
					("SPACE", " "),
					("ABS", "abababab"),
				],
			),
			(
				"abababcababdd",
				[("ABS", "ababab"), ("ABCORC", "c"), ("ABS", "abab"), ("DS", "dd")],
			),
			(
				"ddddd acd abccdddddd ",
				[
					("DS", "ddddd"),
					("SPACE", " "),
					("APLUSCD", "acd"),
					("SPACE", " "),
					("ABCORC", "abc"),
					("ABCORC", "c"),
					("DS", "dddddd"),
					("SPACE", " "),
				],
			),
			(
				" d abab ddabcabcc",
				[
					("SPACE", " "),
					("DS", "d"),
					("SPACE", " "),
					("ABS", "abab"),
					("SPACE", " "),
					("DS", "dd"),
					("ABCORC", "abc"),
					("ABCORC", "abc"),
					("ABCORC", "c"),
				],
			),
			(
				"acdabd aacdc dddd abababc",
				[
					("APLUSCD", "acd"),
					("ABD", "abd"),
					("SPACE", " "),
					("APLUSCD", "aacd"),
					("ABCORC", "c"),
					("SPACE", " "),
					("DS", "dddd"),
					("SPACE", " "),
					("ABS", "ababab"),
					("ABCORC", "c"),
				],
			),
			(
				"caaacdabcaacdcddababd ab abd",
				[
					("ABCORC", "c"),
					("APLUSCD", "aaacd"),
					("ABCORC", "abc"),
					("APLUSCD", "aacd"),
					("ABCORC", "c"),
					("DS", "dd"),
					("ABS", "abab"),
					("DS", "d"),
					("SPACE", " "),
					("ABS", "ab"),
					("SPACE", " "),
					("ABD", "abd"),
				],
			),
			(
				"aacd aacd c abcacddddaacd abccab c",
				[
					("APLUSCD", "aacd"),
					("SPACE", " "),
					("APLUSCD", "aacd"),
					("SPACE", " "),
					("ABCORC", "c"),
					("SPACE", " "),
					("ABCORC", "abc"),
					("APLUSCD", "acd"),
					("DS", "ddd"),
					("APLUSCD", "aacd"),
					("SPACE", " "),
					("ABCORC", "abc"),
					("ABCORC", "c"),
					("ABS", "ab"),
					("SPACE", " "),
					("ABCORC", "c"),
				],
			),
		]

		results = verify(lexer, tests)

		print(f"test07: {results}")
		assert all(results)
		self.__class__.score += 10

	def test_8_big(self):
		spec = [
			("SPACE", "\\ "),
			("DS", "d+"),
			("ABS", "(ab)*"),
			("ABC", "abc"),
			("APLUSBCD", "(a+)bcd"),
			("BORCS", "(b|c)*"),
			("BCSD", "(bc)*d"),
			("DSTARACS", "d*(ac)+"),
		]

		lexer = Lexer(spec)

		tests = [
			(
				"dacacacaaabcd abc ",
				[
					("DSTARACS", "dacacac"),
					("APLUSBCD", "aaabcd"),
					("SPACE", " "),
					("ABC", "abc"),
					("SPACE", " "),
				],
			),
			(
				"aaabcdabcbcbcbcddddacac",
				[
					("APLUSBCD", "aaabcd"),
					("ABC", "abc"),
					("BCSD", "bcbcbcd"),
					("DSTARACS", "dddacac"),
				],
			),
			(
				"bccbbdddd bbb ccc bcd",
				[
					("BORCS", "bccbb"),
					("DS", "dddd"),
					("SPACE", " "),
					("BORCS", "bbb"),
					("SPACE", " "),
					("BORCS", "ccc"),
					("SPACE", " "),
					("BCSD", "bcd"),
				],
			),
			(
				"bcbc bcbcdddacacabd",
				[
					("BORCS", "bcbc"),
					("SPACE", " "),
					("BCSD", "bcbcd"),
					("DSTARACS", "ddacac"),
					("ABS", "ab"),
					("DS", "d"),
				],
			),
			(
				" abcdbcd abcabab bbccd",
				[
					("SPACE", " "),
					("APLUSBCD", "abcd"),
					("BCSD", "bcd"),
					("SPACE", " "),
					("ABC", "abc"),
					("ABS", "abab"),
					("SPACE", " "),
					("BORCS", "bbcc"),
					("DS", "d"),
				],
			),
			(
				"ddacddabc abcdbcdbccbd",
				[
					("DSTARACS", "ddac"),
					("DS", "dd"),
					("ABC", "abc"),
					("SPACE", " "),
					("APLUSBCD", "abcd"),
					("BCSD", "bcd"),
					("BORCS", "bccb"),
					("DS", "d"),
				],
			),
			(
				"acacbcbbc ababcabcd bcddacdd",
				[
					("DSTARACS", "acac"),
					("BORCS", "bcbbc"),
					("SPACE", " "),
					("ABS", "abab"),
					("BORCS", "c"),
					("APLUSBCD", "abcd"),
					("SPACE", " "),
					("BCSD", "bcd"),
					("DSTARACS", "dac"),
					("DS", "dd"),
				],
			),
			(
				"abcdbcbcd bcdbbbcbbcbcccbbbcdbbccbcd ",
				[
					("APLUSBCD", "abcd"),
					("BCSD", "bcbcd"),
					("SPACE", " "),
					("BCSD", "bcd"),
					("BORCS", "bbbcbbcbcccbbbc"),
					("DS", "d"),
					("BORCS", "bbccbc"),
					("DS", "d"),
					("SPACE", " "),
				],
			),
			(
				"abcdbbcdcdacacdababcabc",
				[
					("APLUSBCD", "abcd"),
					("BORCS", "bbc"),
					("DS", "d"),
					("BORCS", "c"),
					("DSTARACS", "dacac"),
					("DS", "d"),
					("ABS", "abab"),
					("BORCS", "c"),
					("ABC", "abc"),
				],
			),
			(
				" d dacacaaabcdbcdbbbdddac",
				[
					("SPACE", " "),
					("DS", "d"),
					("SPACE", " "),
					("DSTARACS", "dacac"),
					("APLUSBCD", "aaabcd"),
					("BCSD", "bcd"),
					("BORCS", "bbb"),
					("DSTARACS", "dddac"),
				],
			),
		]

		results = verify(lexer, tests)

		print(f"test08: {results}")
		assert all(results)
		self.__class__.score += 10

	def test_9_big(self):
		spec = [
			("SPACE", "\\ "),
			("TOKEN1", "(a|b)+(c|d)e"),
			("TOKEN2", "(ab)*((cd*)|e)"),
			("TOKEN3", "b+d*(e|a)*"),
			("TOKEN4", "((ed)|(bc))+"),
			("TOKEN5", "(b|c)*((da)|(ae))+"),
		]

		lexer = Lexer(spec)

		tests = [
			(
				"abcdeabcdddd ed",
				[
					("TOKEN2", "abcd"),
					("TOKEN2", "e"),
					("TOKEN2", "abcdddd"),
					("SPACE", " "),
					("TOKEN4", "ed"),
				],
			),
			(
				"cccbeaeeaa edbc bcdaaeaeda",
				[
					("TOKEN2", "c"),
					("TOKEN2", "c"),
					("TOKEN2", "c"),
					("TOKEN3", "beaeeaa"),
					("SPACE", " "),
					("TOKEN4", "edbc"),
					("SPACE", " "),
					("TOKEN5", "bcdaaeaeda"),
				],
			),
			(
				" caaace edbcededbcedbcbc",
				[
					("SPACE", " "),
					("TOKEN2", "c"),
					("TOKEN1", "aaace"),
					("SPACE", " "),
					("TOKEN4", "edbcededbcedbcbc"),
				],
			),
			(
				"caeeaeeecec cddddaeec ade",
				[
					("TOKEN5", "cae"),
					("TOKEN2", "e"),
					("TOKEN5", "ae"),
					("TOKEN2", "e"),
					("TOKEN2", "e"),
					("TOKEN2", "c"),
					("TOKEN2", "e"),
					("TOKEN2", "c"),
					("SPACE", " "),
					("TOKEN2", "cdddd"),
					("TOKEN5", "ae"),
					("TOKEN2", "e"),
					("TOKEN2", "c"),
					("SPACE", " "),
					("TOKEN1", "ade"),
				],
			),
			(
				"edbcbcaeabeabce",
				[
					("TOKEN4", "edbcbc"),
					("TOKEN5", "ae"),
					("TOKEN2", "abe"),
					("TOKEN1", "abce"),
				],
			),
			(
				" bbccdadae eedbcae",
				[
					("SPACE", " "),
					("TOKEN5", "bbccdada"),
					("TOKEN2", "e"),
					("SPACE", " "),
					("TOKEN2", "e"),
					("TOKEN4", "edbc"),
					("TOKEN5", "ae"),
				],
			),
			(
				" abeedededbcbcedbcbcbcededbcbcababe ",
				[
					("SPACE", " "),
					("TOKEN2", "abe"),
					("TOKEN4", "edededbcbcedbcbcbcededbcbc"),
					("TOKEN2", "ababe"),
					("SPACE", " "),
				],
			),
			(
				"beaeea ccbbbaedaae edbcbcbc  bd ",
				[
					("TOKEN3", "beaeea"),
					("SPACE", " "),
					("TOKEN5", "ccbbbaedaae"),
					("SPACE", " "),
					("TOKEN4", "edbcbcbc"),
					("SPACE", " "),
					("SPACE", " "),
					("TOKEN3", "bd"),
					("SPACE", " "),
				],
			),
			(
				"bdaaecbcbcaeced cedace",
				[
					("TOKEN3", "bdaae"),
					("TOKEN5", "cbcbcae"),
					("TOKEN2", "c"),
					("TOKEN4", "ed"),
					("SPACE", " "),
					("TOKEN2", "c"),
					("TOKEN4", "ed"),
					("TOKEN1", "ace"),
				],
			),
			(
				" ebcededbcbecbccedbced aeaeaedadae",
				[
					("SPACE", " "),
					("TOKEN2", "e"),
					("TOKEN4", "bcededbc"),
					("TOKEN3", "be"),
					("TOKEN2", "c"),
					("TOKEN4", "bc"),
					("TOKEN2", "c"),
					("TOKEN4", "edbced"),
					("SPACE", " "),
					("TOKEN5", "aeaeaedada"),
					("TOKEN2", "e"),
				],
			),
		]

		results = verify(lexer, tests)

		print(f"test09: {results}")
		assert all(results)
		self.__class__.score += 10

	def test_10_big(self):
		spec = [
			("SPACE", "\\ "),
			("ABSTAR", "(ab)*"),
			("ABPLUSC", "(ab)+c*"),
			("BCBC", "bcbc"),
			("CBSAR", "(cb)*"),
			("BORCS", "(b|c)*"),
			("ABDORE", "(abd)|e"),
			("ASTARBD", "a*bd"),
			("EFSTAR", "ef*"),
			("C", "c"),
		]

		lexer = Lexer(spec)

		tests = [
			(
				"ccbbccbbbcabdabd  ",
				[
					("BORCS", "ccbbccbbbc"),
					("ABDORE", "abd"),
					("ABDORE", "abd"),
					("SPACE", " "),
					("SPACE", " "),
				],
			),
			(
				" ababbcbceaaaabd ",
				[
					("SPACE", " "),
					("ABSTAR", "abab"),
					("BCBC", "bcbc"),
					("ABDORE", "e"),
					("ASTARBD", "aaaabd"),
					("SPACE", " "),
				],
			),
			(
				"abababc bccbbcbceabd",
				[
					("ABPLUSC", "abababc"),
					("SPACE", " "),
					("BORCS", "bccbbcbc"),
					("ABDORE", "e"),
					("ABDORE", "abd"),
				],
			),
			(
				"effcbbcefffffe abdabdbd",
				[
					("EFSTAR", "eff"),
					("BORCS", "cbbc"),
					("EFSTAR", "efffff"),
					("ABDORE", "e"),
					("SPACE", " "),
					("ABDORE", "abd"),
					("ABDORE", "abd"),
					("ASTARBD", "bd"),
				],
			),
			(
				"bdebdefabdabaabd abccc",
				[
					("ASTARBD", "bd"),
					("ABDORE", "e"),
					("ASTARBD", "bd"),
					("EFSTAR", "ef"),
					("ABDORE", "abd"),
					("ABSTAR", "ab"),
					("ASTARBD", "aabd"),
					("SPACE", " "),
					("ABPLUSC", "abccc"),
				],
			),
			(
				"abbcbccb cbcbcb bcbcbc c",
				[
					("ABSTAR", "ab"),
					("BORCS", "bcbccb"),
					("SPACE", " "),
					("CBSAR", "cbcbcb"),
					("SPACE", " "),
					("BORCS", "bcbcbc"),
					("SPACE", " "),
					("BORCS", "c"),
				],
			),
			(
				"abdababababababc ccbc cbcbcbcbcbcbcb bcbc ",
				[
					("ABDORE", "abd"),
					("ABPLUSC", "ababababababc"),
					("SPACE", " "),
					("BORCS", "ccbc"),
					("SPACE", " "),
					("CBSAR", "cbcbcbcbcbcbcb"),
					("SPACE", " "),
					("BCBC", "bcbc"),
					("SPACE", " "),
				],
			),
			(
				"efeabdefffcb bcbc cb cbbcabc",
				[
					("EFSTAR", "ef"),
					("ABDORE", "e"),
					("ABDORE", "abd"),
					("EFSTAR", "efff"),
					("CBSAR", "cb"),
					("SPACE", " "),
					("BCBC", "bcbc"),
					("SPACE", " "),
					("CBSAR", "cb"),
					("SPACE", " "),
					("BORCS", "cbbc"),
					("ABPLUSC", "abc"),
				],
			),
			(
				" abd cbbbcbbcbbbbceffceffbcccbbbc  ",
				[
					("SPACE", " "),
					("ABDORE", "abd"),
					("SPACE", " "),
					("BORCS", "cbbbcbbcbbbbc"),
					("EFSTAR", "eff"),
					("BORCS", "c"),
					("EFSTAR", "eff"),
					("BORCS", "bcccbbbc"),
					("SPACE", " "),
					("SPACE", " "),
				],
			),
			(
				"bcbcecbbcebcab aabdeabdababcccab efce",
				[
					("BCBC", "bcbc"),
					("ABDORE", "e"),
					("BORCS", "cbbc"),
					("ABDORE", "e"),
					("BORCS", "bc"),
					("ABSTAR", "ab"),
					("SPACE", " "),
					("ASTARBD", "aabd"),
					("ABDORE", "e"),
					("ABDORE", "abd"),
					("ABPLUSC", "ababccc"),
					("ABSTAR", "ab"),
					("SPACE", " "),
					("EFSTAR", "ef"),
					("BORCS", "c"),
					("ABDORE", "e"),
				],
			),
		]

		results = verify(lexer, tests)

		print(f"test10: {results}")
		assert all(results)
		self.__class__.score += 10

	def test_11_big(self):
		spec = [
			("SPACE", "\\ "),
			("TOKEN1", "(a|b*)(c*|(de))"),
			("TOKEN2", "(((ab)*c)|(aade))"),
			("TOKEN3", "((def*)|(c*))+"),
			("TOKEN4", "(ec)*(a|b)+"),
			("TOKEN5", "((a|c)*|(b|(d|e))*)*"),
		]

		lexer = Lexer(spec)

		tests = [
			(
				"ececbbbbba aade ",
				[
					("TOKEN4", "ececbbbbba"),
					("SPACE", " "),
					("TOKEN2", "aade"),
					("SPACE", " "),
				],
			),
			(
				"cdefdedefdeffccdeececaadbddccdae bbabaaabba",
				[
					("TOKEN3", "cdefdedefdeffccde"),
					("TOKEN5", "ececaadbddccdae"),
					("SPACE", " "),
					("TOKEN4", "bbabaaabba"),
				],
			),
			(
				"eccbbaa aabbecc aade bbcc ",
				[
					("TOKEN5", "eccbbaa"),
					("SPACE", " "),
					("TOKEN5", "aabbecc"),
					("SPACE", " "),
					("TOKEN2", "aade"),
					("SPACE", " "),
					("TOKEN1", "bbcc"),
					("SPACE", " "),
				],
			),
			(
				"defccdefffade abbccdd",
				[
					("TOKEN3", "defccdefff"),
					("TOKEN1", "ade"),
					("SPACE", " "),
					("TOKEN5", "abbccdd"),
				],
			),
			(
				"aade accccc eca ecb ecaab",
				[
					("TOKEN2", "aade"),
					("SPACE", " "),
					("TOKEN1", "accccc"),
					("SPACE", " "),
					("TOKEN4", "eca"),
					("SPACE", " "),
					("TOKEN4", "ecb"),
					("SPACE", " "),
					("TOKEN4", "ecaab"),
				],
			),
			(
				"ade bbbbbb ababab c",
				[
					("TOKEN1", "ade"),
					("SPACE", " "),
					("TOKEN1", "bbbbbb"),
					("SPACE", " "),
					("TOKEN4", "ababab"),
					("SPACE", " "),
					("TOKEN1", "c"),
				],
			),
			(
				"accccccca dbcb dcccaab de ",
				[
					("TOKEN5", "accccccca"),
					("SPACE", " "),
					("TOKEN5", "dbcb"),
					("SPACE", " "),
					("TOKEN5", "dcccaab"),
					("SPACE", " "),
					("TOKEN1", "de"),
					("SPACE", " "),
				],
			),
		]

		results = verify(lexer, tests)

		print(f"test11: {results}")
		assert all(results)
		self.__class__.score += 10

	def test_12_big(self):
		spec = [
			("SPACE", "\\ "),
			("NEWLINE", "\n"),
			("PATTERN1", "((b+|e)(a*|b+))+((e+fd)*|(c+a*)*)"),
			("PATTERN2", "(((db)|d+)*(da)*(dc)*)|((dc)+|(a+|b+))*"),
			("PATTERN3", "((e|(db))+|(e+e(e|f*)))+"),
			("PATTERN4", "(((f*a+)|(a*d+))|((a*|e)daf+))+"),
			("PATTERN5", "(((c|d)|f*)*|((f|a)+|(b|c)+))+"),
		]

		lexer = Lexer(spec)

		tests = [
			(
				"babbbaadcabaaabbabdcbdcbdcbbbefdefdefdeeefdeefdeefddabbfcdadbacdcfcdcbcfddba\n",
				[
					("PATTERN2", "babbbaadcabaaabbabdcbdcbdcbbb"),
					("PATTERN1", "e"),
					("PATTERN5", "fd"),
					("PATTERN1", "e"),
					("PATTERN5", "fd"),
					("PATTERN1", "e"),
					("PATTERN5", "fd"),
					("PATTERN1", "eeefdeefdeefd"),
					("PATTERN5", "dabbfcdadbacdcfcdcbcfddba"),
					("NEWLINE", "\n"),
				],
			),
			(
				"edaffffaaedaffedaffaedaff acccdbdbdbadfdbcfddccfdcf\ndbdbdbddbdcdcdcdcdcdcdcdc\nedafdaedafedafedafdaaedaf ddedafedafedafaafaedafedaf",
				[
					("PATTERN4", "edaffffaaedaffedaffaedaff"),
					("SPACE", " "),
					("PATTERN5", "acccdbdbdbadfdbcfddccfdcf"),
					("NEWLINE", "\n"),
					("PATTERN2", "dbdbdbddbdcdcdcdcdcdcdcdc"),
					("NEWLINE", "\n"),
					("PATTERN4", "edafdaedafedafedafdaaedaf"),
					("SPACE", " "),
					("PATTERN4", "ddedafedafedafaafaedafedaf"),
				],
			),
			(
				"eabaacaccaccaaccccccccaac bdcbdcbdcaadcdcbbdcabadcdc eecacaaaccaaacccacacaacca\n",
				[
					("PATTERN1", "eabaacaccaccaaccccccccaac"),
					("SPACE", " "),
					("PATTERN2", "bdcbdcbdcaadcdcbbdcabadcdc"),
					("SPACE", " "),
					("PATTERN1", "eecacaaaccaaacccacacaacca"),
					("NEWLINE", "\n"),
				],
			),
			(
				"faacadaabccbccbfcdfdffcda ",
				[("PATTERN5", "faacadaabccbccbfcdfdffcda"), ("SPACE", " ")],
			),
			("adcaabdcdcdcdcaababbaadca", [("PATTERN2", "adcaabdcdcdcdcaababbaadca")]),
			(
				"eefeefeeffdbedbedbedbdbee eefdefdeeeeeefdeefdefdeefd ",
				[
					("PATTERN3", "eefeefeeffdbedbedbedbdbee"),
					("SPACE", " "),
					("PATTERN1", "eefdefdeeeeeefdeefdefdeefd"),
					("SPACE", " "),
				],
			),
			(
				"afffccdbaaffddfabaacdcdcb\ncbfafafabdaabdfddfcbccdba\naffadaaaffffafffaadedafda ffaedafaaddaedafdedaffaaa ",
				[
					("PATTERN5", "afffccdbaaffddfabaacdcdcb"),
					("NEWLINE", "\n"),
					("PATTERN5", "cbfafafabdaabdfddfcbccdba"),
					("NEWLINE", "\n"),
					("PATTERN4", "affadaaaffffafffaadedafda"),
					("SPACE", " "),
					("PATTERN4", "ffaedafaaddaedafdedaffaaa"),
					("SPACE", " "),
				],
			),
			(
				"dabadffdccaabcbfbfadacfadbaabaadcabdcadcabbdcbbabdc ",
				[
					("PATTERN5", "dabadffdccaabcbfbfadacfadbaabaadcabdcadcabbdcbbabdc"),
					("SPACE", " "),
				],
			),
			(
				"\needbeeeeeedbeefeeefffdbdb\ndbafcacdcfffdfbdcfbfccdad \nebbbacacacaccaaaacccaaaca",
				[
					("NEWLINE", "\n"),
					("PATTERN3", "eedbeeeeeedbeefeeefffdbdb"),
					("NEWLINE", "\n"),
					("PATTERN5", "dbafcacdcfffdfbdcfbfccdad"),
					("SPACE", " "),
					("NEWLINE", "\n"),
					("PATTERN1", "ebbbacacacaccaaaacccaaaca"),
				],
			),
			(
				"edbeedbdbdbeeeffdbeefdbdb aaabaadcadcdcbdcababababdc\nebbeaeeecacacaccacaccaaaa\nbcaaccaaccaaaacaccccaacac\n",
				[
					("PATTERN3", "edbeedbdbdbeeeffdbeefdbdb"),
					("SPACE", " "),
					("PATTERN2", "aaabaadcadcdcbdcababababdc"),
					("NEWLINE", "\n"),
					("PATTERN1", "ebbeaeeecacacaccacaccaaaa"),
					("NEWLINE", "\n"),
					("PATTERN1", "bcaaccaaccaaaacaccccaacac"),
					("NEWLINE", "\n"),
				],
			),
		]

		results = verify(lexer, tests)

		print(f"test12: {results}")
		assert all(results)
		self.__class__.score += 10

	def test_13_error_check(self):
		spec = [
			("SPACE", "\\ "),
			("NEWLINE", "\n"),
			("ABC", "a(b+)c"),
			("AS", "a+"),
			("BCS", "(bc)+"),
			("DORC", "(d|c)+")
		]

		lexer = Lexer(spec)

		tests = [
			("abcbcbcaabaad dccbca", [("", "No viable alternative at character 10, line 0")]),
			("d abdbc ccddabbbc", [("", "No viable alternative at character 4, line 0")]),
			("d a\nbdbc ccddabbbc", [("", "No viable alternative at character 1, line 1")]),
			("e abbbcbcaadc c", [("", "No viable alternative at character 0, line 0")]),  # this has a char not in the spec
			("dccbcbcaaaa abbcf", [("", "No viable alternative at character 16, line 0")]),  # this has a char not in the spec
			("abbcaaabc dcccabcb", [("", "No viable alternative at character EOF, line 0")]),
			("abbc\naaabc dcccabcb", [("", "No viable alternative at character EOF, line 1")]),
			("dcdccaabcabb dcaabc", [("", "No viable alternative at character 11, line 0")]),
			("\naaa\nbabbcbcbc abbbcaabc", [("", "No viable alternative at character 1, line 2")])
		]

		results = verify(lexer, tests)

		print(f"test13: {results}")
		assert all(results)
		self.__class__.score += 30
