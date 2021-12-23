import rlexeme
import rtoken

def test_get_lexemes():

    # identifiers and standard operators
    expected = ['a', '::', 'b', ':::', 'ba', '$', 'c', '@', 'd', '^', 'e', ':', 'ea', 
            '%%%%', 'f', '%%/%%', 'g', '%%*%%', 'h', '%%o%%', 'i', '%%x%%', 'j', '%%in%%', 'k', 
            '/', 'l', '*', 'm', '+', 'n', '-', 'o', '<', 'p', '>', 'q', '<=', 'r', '>=', 's', 
            '==', 't', '!=', 'u', '!', 'v', '&', 'wx', '&&', 'y', '|', 'z', '||', 'a2', '~', 
            '2b', '->', 'c0a', '->>', 'd0123456789a', '<-', '1234567890', '<<-', 'e0a1b2', 
            '=', '345f6789']
    actual = rlexeme.get_lexemes(
            'a::b:::ba$c@d^e:ea%%%%f%%/%%g%%*%%h%%o%%i%%x%%j%%in%%k/l*m+n-o<p>q<=r>=s==t!=u!v&wx' +
            '&&y|z||a2~2b->c0a->>d012345678' + '9a<-1234567890<<-e0a1b2=345f6789')
    assert actual == expected

    # separators, brackets, line feeds, user-defined operators and variable names with '.' and '_'
    expected = [',', 'ae', ';', 'af', '\r', 'ag', '\n', '(', 'ah', ')', '\r\n', 'ai', 
            '{', 'aj', '}', 'ak', '[', 'al', ']', 'al', '[[', 'am', ']]', '_ao', '%%>%%', '.ap', 
            '%%aq%%', '.ar_2', '%%asat%%', 'au_av.awax']
    actual = rlexeme.get_lexemes(
            ',ae;af\rag\n(ah)\r\nai{aj}ak[al]al[[am]]_ao%%>%%.ap%%aq%%.ar_2%%asat%%au_av.awax')
    assert actual == expected

    # spaces
    expected = [
            ' ', '+', 'ay', '-', ' ', 'az', '  ', '::', 'ba', '   ', '%%*%%', '   ', 'bb', '   ',
            '<<-', '    ', 'bc', ' ', '\r', '  ', 'bd', '   ', '\n', '    ', 'be', '   ',
            '\r\n', '  ', 'bf', ' ']
    actual = rlexeme.get_lexemes(
            ' +ay- az  ::ba   %%*%%   bb   <<-    bc \r  bd   \n    be   \r\n  bf ')
    assert actual == expected

    # string literals
    expected = [
            '"a"', '+', '"bf"', '%%%%', '"bga"', '%%/%%', '"bgba"', '%%in%%', '"bgbaa"', '>=', 
            '"~!@#$%%^&*()_[] {} \\|;:\',./<>? "', ',', '" bgbaaa"', '\r', '"bh"', '\n', '"bi"', 
            '\r\n', '"bj"', '{', '"bk"', '[[', '"bl"', '%%>%%', '"bm"', '%%aq%%', '"bn"', ' ', '+',
            '"bn"', '-', ' ', '"bo"', '  ', '::', '"bq"', '   ',  '<<-', '    ', '"br"', ' ', '\r', 
            '  ', '"bs"', '   ', '\n', '    ', '"bt"', '   ', '\r\n', '  ', '"bu"', ' ']
    actual = rlexeme.get_lexemes(
            '"a"+"bf"%%%%"bga"%%/%%"bgba"%%in%%"bgbaa">="~!@#$%%^&*()_[] {} \\|;:\',./<>? ",' +
            '" bgbaaa"\r"bh"\n"bi"\r\n"bj"{"bk"[["bl"%%>%%"bm"%%aq%%"bn" +"bn"- "bo"  ::"bq"   ' +
            '<<-    "br" \r  "bs"   \n    "bt"   \r\n  "bu" ')
    assert actual == expected

    # comments
    expected = [
            '#', '\n', 'c', '#', '\n', 'ca', '#', '\n', '+', '#', '\n', '%%/%%', '#', '\n',
            '%%in%%', '#', '\n', '>=', '#~!@#$%%^&*()_[]{}\\|;:\',./<>?#', '\n', ' ', '#', '\n',
            '  ', '#~!@#$%%^&*()_[] {} \\|;:\',./<>?', '\n', '#cb', '\n', '#cba', '\n',
            '# "," cbaa ', '\n', '#', '\r', '#cc', '\r', '#cca', '\r\n', '# ccaa ', '\r\n']
    actual = rlexeme.get_lexemes(
            '#\nc#\nca#\n+#\n%%/%%#\n%%in%%#\n>=#~!@#$%%^&*()_[]{}\\|;:\',./<>?#\n #\n  ' +
            '#~!@#$%%^&*()_[] {} \\|;:\',./<>?\n#cb\n#cba\n# "," cbaa \n#\r#cc\r#cca\r\n# ccaa \r\n')
    assert actual == expected 

def test_get_lst_tokens():
    # RSyntacticName
#     input_string = '._+.1+.a+a+ba+baa+a_b+c12+1234567890+2.3+1e6+' + \
#             'abcdefghijklmnopqrstuvwxyz+`a`+`a b`+`[[`+`d,ae;af`+`(ah)`+`ai{aj}`+' + \
#             '`~!@#$%%^&*()_[] {} \\|;:',./<>?`+`%%%%a_2ab%%`+`%%ac%%`+`[["b"]]n[[[o][p]]]`+' + \
#             '`if`+`else`+`while`+`repeat`+`for`+`in`+`function`+`return`+`else`+`next`+`break`'
#     expected = '._(RSyntacticName), +(ROperatorBinary), .1(RSyntacticName), ' + \
#             '+(ROperatorBinary), .a(RSyntacticName), +(ROperatorBinary), a(RSyntacticName), ' + \
#             '+(ROperatorBinary), ba(RSyntacticName), +(ROperatorBinary), baa(RSyntacticName), ' + \
#             '+(ROperatorBinary), a_b(RSyntacticName), +(ROperatorBinary), c12(RSyntacticName), ' + \
#             '+(ROperatorBinary), 1234567890(RSyntacticName), +(ROperatorBinary), ' + \
#             '2.3(RSyntacticName), +(ROperatorBinary), 1e6(RSyntacticName), +(ROperatorBinary), ' + \
#             'abcdefghijklmnopqrstuvwxyz(RSyntacticName), +(ROperatorBinary), `a`(RSyntacticName), ' + \
#             '+(ROperatorUnaryRight), `a b`(RSyntacticName), +(ROperatorUnaryRight), `[[`(RSyntacticName), ' + \
#             '+(ROperatorUnaryRight), `d,ae;af`(RSyntacticName), +(ROperatorUnaryRight), ' + \
#             '`(ah)`(RSyntacticName), +(ROperatorUnaryRight), `ai{aj}`(RSyntacticName), +(ROperatorUnaryRight), ' + \
#             '`~!@#$%%^&*()_[] {} \\|;:',./<>?`(RSyntacticName), +(ROperatorUnaryRight), ' + \
#             '`%%%%a_2ab%%`(RSyntacticName), +(ROperatorUnaryRight), `%%ac%%`(RSyntacticName), ' + \
#             '+(ROperatorUnaryRight), `[["b"]]n[[[o][p]]]`(RSyntacticName), +(ROperatorUnaryRight), ' + \
#             '`if`(RSyntacticName), +(ROperatorUnaryRight), `else`(RSyntacticName), +(ROperatorUnaryRight), ' + \
#             '`while`(RSyntacticName), +(ROperatorUnaryRight), `repeat`(RSyntacticName), ' + \
#             '+(ROperatorUnaryRight), `for`(RSyntacticName), +(ROperatorUnaryRight), `in`(RSyntacticName), ' + \
#             '+(ROperatorUnaryRight), `function`(RSyntacticName), +(ROperatorUnaryRight), ' + \
#             '`return`(RSyntacticName), +(ROperatorUnaryRight), `else`(RSyntacticName), ' + \
#             '+(ROperatorUnaryRight), `next`(RSyntacticName), +(ROperatorUnaryRight), ' + \
#             '`break`(RSyntacticName), '
    input_string = '._+.1' 
    expected = '._(RSyntacticName), +(ROperatorBinary), .1(RSyntacticName), '
    actual = rtoken.get_tokens_as_string(rtoken.get_tokens(rlexeme.get_lexemes(input_string)))
    assert actual == expected
