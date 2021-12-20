import rscript

def test_get_lst_lexemes():

    # identifiers and standard operators
    lexemes_expected = ['a', '::', 'b', ':::', 'ba', '$', 'c', '@', 'd', '^', 'e', ':', 'ea', 
            '%%%%', 'f', '%%/%%', 'g', '%%*%%', 'h', '%%o%%', 'i', '%%x%%', 'j', '%%in%%', 'k', 
            '/', 'l', '*', 'm', '+', 'n', '-', 'o', '<', 'p', '>', 'q', '<=', 'r', '>=', 's', 
            '==', 't', '!=', 'u', '!', 'v', '&', 'wx', '&&', 'y', '|', 'z', '||', 'a2', '~', 
            '2b', '->', 'c0a', '->>', 'd0123456789a', '<-', '1234567890', '<<-', 'e0a1b2', 
            '=', '345f6789']
    lexemes_actual = rscript.RScript.get_lst_lexemes(
            'a::b:::ba$c@d^e:ea%%%%f%%/%%g%%*%%h%%o%%i%%x%%j%%in%%k/l*m+n-o<p>q<=r>=s==t!=u!v&wx' +
            '&&y|z||a2~2b->c0a->>d012345678' + '9a<-1234567890<<-e0a1b2=345f6789')
    assert lexemes_actual == lexemes_expected

    # separators, brackets, line feeds, user-defined operators and variable names with '.' and '_'
    lexemes_expected = [',', 'ae', ';', 'af', '\r', 'ag', '\n', '(', 'ah', ')', '\r\n', 'ai', 
            '{', 'aj', '}', 'ak', '[', 'al', ']', 'al', '[[', 'am', ']]', '_ao', '%%>%%', '.ap', 
            '%%aq%%', '.ar_2', '%%asat%%', 'au_av.awax']
    lexemes_actual = rscript.RScript.get_lst_lexemes(
            ',ae;af\rag\n(ah)\r\nai{aj}ak[al]al[[am]]_ao%%>%%.ap%%aq%%.ar_2%%asat%%au_av.awax')
    assert lexemes_actual == lexemes_expected

    # spaces
    lexemes_expected = [
            ' ', '+', 'ay', '-', ' ', 'az', '  ', '::', 'ba', '   ', '%%*%%', '   ', 'bb', '   ',
            '<<-', '    ', 'bc', ' ', '\r', '  ', 'bd', '   ', '\n', '    ', 'be', '   ',
            '\r\n', '  ', 'bf', ' ']
    lexemes_actual = rscript.RScript.get_lst_lexemes(
            ' +ay- az  ::ba   %%*%%   bb   <<-    bc \r  bd   \n    be   \r\n  bf ')
    assert lexemes_actual == lexemes_expected

    # string literals
    lexemes_expected = [
            '"a"', '+', '"bf"', '%%%%', '"bga"', '%%/%%', '"bgba"', '%%in%%', '"bgbaa"', '>=', 
            '"~!@#$%%^&*()_[] {} \\|;:\',./<>? "', ',', '" bgbaaa"', '\r', '"bh"', '\n', '"bi"', 
            '\r\n', '"bj"', '{', '"bk"', '[[', '"bl"', '%%>%%', '"bm"', '%%aq%%', '"bn"', ' ', '+',
            '"bn"', '-', ' ', '"bo"', '  ', '::', '"bq"', '   ',  '<<-', '    ', '"br"', ' ', '\r', 
            '  ', '"bs"', '   ', '\n', '    ', '"bt"', '   ', '\r\n', '  ', '"bu"', ' ']
    lexemes_actual = rscript.RScript.get_lst_lexemes(
            '"a"+"bf"%%%%"bga"%%/%%"bgba"%%in%%"bgbaa">="~!@#$%%^&*()_[] {} \\|;:\',./<>? ",' +
            '" bgbaaa"\r"bh"\n"bi"\r\n"bj"{"bk"[["bl"%%>%%"bm"%%aq%%"bn" +"bn"- "bo"  ::"bq"   ' +
            '<<-    "br" \r  "bs"   \n    "bt"   \r\n  "bu" ')
    assert lexemes_actual == lexemes_expected

    # comments
    lexemes_expected = [
            '#', '\n', 'c', '#', '\n', 'ca', '#', '\n', '+', '#', '\n', '%%/%%', '#', '\n',
            '%%in%%', '#', '\n', '>=', '#~!@#$%%^&*()_[]{}\\|;:\',./<>?#', '\n', ' ', '#', '\n',
            '  ', '#~!@#$%%^&*()_[] {} \\|;:\',./<>?', '\n', '#cb', '\n', '#cba', '\n',
            '# "," cbaa ', '\n', '#', '\r', '#cc', '\r', '#cca', '\r\n', '# ccaa ', '\r\n']
    lexemes_actual = rscript.RScript.get_lst_lexemes(
            '#\nc#\nca#\n+#\n%%/%%#\n%%in%%#\n>=#~!@#$%%^&*()_[]{}\\|;:\',./<>?#\n #\n  ' +
            '#~!@#$%%^&*()_[] {} \\|;:\',./<>?\n#cb\n#cba\n# "," cbaa \n#\r#cc\r#cca\r\n# ccaa \r\n')
    assert lexemes_actual == lexemes_expected 
