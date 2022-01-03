from typing import List
import rlexeme
import rtoken
import rscript

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

def get_tokens_as_string(tokens: List[rtoken.RToken]) -> str:
    if not tokens:
        return "" 

    tokens_str : str = ""

    for token in tokens:
        tokens_str += token.text + '('
        match token.token_type:
            case rtoken.TokenType.SYNTACTIC_NAME:
                tokens_str += 'RSyntacticName'
            case rtoken.TokenType.FUNCTION_NAME:
                tokens_str += 'RFunctionName'
            case rtoken.TokenType.KEY_WORD:
                tokens_str += 'RKeyWord'
            case rtoken.TokenType.CONSTANT_STRING:
                tokens_str += 'RStringLiteral'
            case rtoken.TokenType.COMMENT:
                tokens_str += 'RComment'
            case rtoken.TokenType.SPACE:
                tokens_str += 'RSpace'
            case rtoken.TokenType.BRACKET:
                tokens_str += 'RBracket'
            case rtoken.TokenType.SEPARATOR:
                tokens_str += 'RSeparator'
            case rtoken.TokenType.NEW_LINE:
                tokens_str += 'RNewLine'
            case rtoken.TokenType.END_STATEMENT:
                tokens_str += 'REndStatement'
            case rtoken.TokenType.END_SCRIPT:
                tokens_str += 'REndScript'
            case rtoken.TokenType.OPERATOR_UNARY_LEFT:
                tokens_str += 'ROperatorUnaryLeft'
            case rtoken.TokenType.OPERATOR_UNARY_RIGHT:
                tokens_str += 'ROperatorUnaryRight'
            case rtoken.TokenType.OPERATOR_BINARY:
                tokens_str += 'ROperatorBinary'
            case rtoken.TokenType.OPERATOR_BRACKET:
                tokens_str += 'ROperatorBracket'
        tokens_str += '), '

    return tokens_str

def test_get_lst_tokens():
    # RSyntacticName
    input_string = '._+.1+.a+a+ba+baa+a_b+c12+1234567890+2.3+1e6+' + \
            'abcdefghijklmnopqrstuvwxyz+`a`+`a b`+`[[`+`d,ae;af`+`(ah)`+`ai{aj}`+' + \
            "`~!@#$%%^&*()_[] {} \\|;:',./<>?`+`%%%%a_2ab%%`+`%%ac%%`+" + '`[["b"]]n[[[o][p]]]`+' + \
            '`if`+`else`+`while`+`repeat`+`for`+`in`+`function`+`return`+`else`+`next`+`break`'
    expected = '._(RSyntacticName), +(ROperatorBinary), .1(RSyntacticName), ' + \
            '+(ROperatorBinary), .a(RSyntacticName), +(ROperatorBinary), a(RSyntacticName), ' + \
            '+(ROperatorBinary), ba(RSyntacticName), +(ROperatorBinary), baa(RSyntacticName), ' + \
            '+(ROperatorBinary), a_b(RSyntacticName), +(ROperatorBinary), c12(RSyntacticName), ' + \
            '+(ROperatorBinary), 1234567890(RSyntacticName), +(ROperatorBinary), ' + \
            '2.3(RSyntacticName), +(ROperatorBinary), 1e6(RSyntacticName), +(ROperatorBinary), ' + \
            'abcdefghijklmnopqrstuvwxyz(RSyntacticName), +(ROperatorBinary), `a`(RSyntacticName), ' + \
            '+(ROperatorUnaryRight), `a b`(RSyntacticName), +(ROperatorUnaryRight), `[[`(RSyntacticName), ' + \
            '+(ROperatorUnaryRight), `d,ae;af`(RSyntacticName), +(ROperatorUnaryRight), ' + \
            '`(ah)`(RSyntacticName), +(ROperatorUnaryRight), `ai{aj}`(RSyntacticName), +(ROperatorUnaryRight), ' + \
            "`~!@#$%%^&*()_[] {} \\|;:',./<>?`(RSyntacticName), +(ROperatorUnaryRight), " + \
            '`%%%%a_2ab%%`(RSyntacticName), +(ROperatorUnaryRight), `%%ac%%`(RSyntacticName), ' + \
            '+(ROperatorUnaryRight), `[["b"]]n[[[o][p]]]`(RSyntacticName), +(ROperatorUnaryRight), ' + \
            '`if`(RSyntacticName), +(ROperatorUnaryRight), `else`(RSyntacticName), +(ROperatorUnaryRight), ' + \
            '`while`(RSyntacticName), +(ROperatorUnaryRight), `repeat`(RSyntacticName), ' + \
            '+(ROperatorUnaryRight), `for`(RSyntacticName), +(ROperatorUnaryRight), `in`(RSyntacticName), ' + \
            '+(ROperatorUnaryRight), `function`(RSyntacticName), +(ROperatorUnaryRight), ' + \
            '`return`(RSyntacticName), +(ROperatorUnaryRight), `else`(RSyntacticName), ' + \
            '+(ROperatorUnaryRight), `next`(RSyntacticName), +(ROperatorUnaryRight), ' + \
            '`break`(RSyntacticName), '
    actual = get_tokens_as_string(rtoken.get_tokens(rlexeme.get_lexemes(input_string)))
    assert actual == expected

    # RBracket, RSeparator
    input_string = 'd,ae;af\rag\n(ah)\r\nai{aj}'
    expected = 'd(RSyntacticName), ,(RSeparator), ae(RSyntacticName), ;(REndStatement), ' + \
                'af(RSyntacticName), \r(REndStatement), ag(RSyntacticName), ' + \
                '\n(REndStatement), ((RBracket), ah(RSyntacticName), )(RBracket), ' + \
                '\r\n(REndStatement), ai(RSyntacticName), {(RBracket), aj(RSyntacticName), }(REndScript), '
    actual = get_tokens_as_string(rtoken.get_tokens(rlexeme.get_lexemes(input_string)))
    assert actual == expected

    # RSpace
    input_string = ' + ay + az + ba   +   bb   +    bc \r  bd   \n' + \
                '    be   \r\n  bf '
    expected = ' (RSpace), +(ROperatorUnaryRight),  (RSpace), ay(RSyntacticName), ' + \
                ' (RSpace), +(ROperatorBinary),  (RSpace), az(RSyntacticName),  (RSpace), ' + \
                '+(ROperatorBinary),  (RSpace), ba(RSyntacticName),    (RSpace), ' + \
                '+(ROperatorBinary),    (RSpace), bb(RSyntacticName),    (RSpace), ' + \
                '+(ROperatorBinary),     (RSpace), bc(RSyntacticName),  (RSpace), ' + \
                '\r(REndStatement),   (RSpace), bd(RSyntacticName),    (RSpace), ' + \
                '\n(REndStatement),     (RSpace), be(RSyntacticName),    (RSpace), ' + \
                '\r\n(REndStatement),   (RSpace), bf(RSyntacticName),  (RSpace), '
    actual = get_tokens_as_string(rtoken.get_tokens(rlexeme.get_lexemes(input_string)))
    assert actual == expected

    # RStringLiteral
    input_string = "'a'" + \
                ',"bf",' + \
                "'bga'" + \
                ',"bgba",' + \
                "'bgbaa'" + \
                ',"~!@#$%^&*()_[] {} \\|;:' + \
                "'" + \
                ',./<>? "," bgbaaa"\r' + \
                "'bh'" + \
                '\n"bi"\r\n' + \
                "'bj'" + \
                '{"bk",' + \
                "'bl'" + \
                ',"bm",' + \
                "'bn'" + \
                ' ,"bn", ' + \
                "'bo'" + \
                '  ,"bq"   ,    ' + \
                "'br'" + \
                ' \r  "bs"   \n    ' + \
                "'bt'" + \
                '   \r\n  "bu" ' + \
                "'" + \
                '~!@#$%^&*()_[] {} \\|;:",./<>? ' + \
                "'"
    expected = "'a'" + \
                '(RStringLiteral), ,(RSeparator), "bf"(RStringLiteral), ,(RSeparator), ' + \
                "'bga'" + \
                '(RStringLiteral), ,(RSeparator), "bgba"(RStringLiteral), ,(RSeparator), ' + \
                "'bgbaa'" + \
                '(RStringLiteral), ,(RSeparator), "~!@#$%^&*()_[] {} \\|;:' + \
                "'" + \
                ',./<>? "(RStringLiteral), ,(RSeparator), " bgbaaa"(RStringLiteral), \r(REndStatement), ' + \
                "'bh'" + \
                '(RStringLiteral), \n(REndStatement), "bi"(RStringLiteral), \r\n(REndStatement), ' + \
                "'bj'" + \
                '(RStringLiteral), {(RBracket), "bk"(RStringLiteral), ,(RSeparator), ' + \
                "'bl'" + \
                '(RStringLiteral), ,(RSeparator), "bm"(RStringLiteral), ,(RSeparator), ' + \
                "'bn'" + \
                '(RStringLiteral),  (RSpace), ,(RSeparator), "bn"(RStringLiteral), ,(RSeparator),  (RSpace), ' + \
                "'bo'" + \
                '(RStringLiteral),   (RSpace), ,(RSeparator), "bq"(RStringLiteral),    (RSpace), ,(RSeparator),     (RSpace), ' + \
                "'br'" + \
                '(RStringLiteral),  (RSpace), \r(REndStatement),   (RSpace), "bs"(RStringLiteral),    (RSpace), \n(REndStatement),     (RSpace), ' + \
                "'bt'" + \
                '(RStringLiteral),    (RSpace), \r\n(REndStatement),   (RSpace), "bu"(RStringLiteral),  (RSpace), ' + \
                "'" + \
                '~!@#$%^&*()_[] {} \\|;:",./<>? ' + \
                "'" + \
                '(RStringLiteral), '
    actual = get_tokens_as_string(rtoken.get_tokens(rlexeme.get_lexemes(input_string)))
    assert actual == expected

    # RComment 
    input_string = '#\nc#\nca#\nd~#\n #\n  #~!@#$%^&*()_[] {} \\|;:' + \
                    "'" + \
                    ',./<>?\n#cb\n#cba\n# "," cbaa \n#\r#cc\r#cca\r\n# ccaa \r\n#\ne+f#\n #ignored comment'
    expected = '#(RComment), ' + \
                '\n(RNewLine), c(RSyntacticName), #(RComment), ' + \
                '\n(REndStatement), ca(RSyntacticName), #(RComment), ' + \
                '\n(REndStatement), d(RSyntacticName), ~(ROperatorUnaryLeft), #(RComment), ' + \
                '\n(REndStatement),  (RSpace), #(RComment), ' + \
                '\n(RNewLine),   (RSpace), #~!@#$%^&*()_[] {} \\|;:' + \
                "'" + \
                ',./<>?(RComment), ' + \
                '\n(RNewLine), #cb(RComment), ' + \
                '\n(RNewLine), #cba(RComment), ' + \
                '\n(RNewLine), # "," cbaa (RComment), ' + \
                '\n(RNewLine), #(RComment), ' + \
                '\r(RNewLine), #cc(RComment), ' + \
                '\r(RNewLine), #cca(RComment), ' + \
                '\r\n(RNewLine), # ccaa (RComment), ' + \
                '\r\n(RNewLine), #(RComment), ' + \
                '\n(RNewLine), e(RSyntacticName), +(ROperatorBinary), f(RSyntacticName), #(RComment), ' + \
                '\n(REndScript), '

    actual = get_tokens_as_string(rtoken.get_tokens(rlexeme.get_lexemes(input_string)))
    assert actual == expected

    # standard operators ROperatorUnaryLeft, ROperatorUnaryRight, ROperatorBinary
    input_string = 'a::b:::ba$c@d^e:ea%%%%f%%/%%g%%*%%h%%o%%i%%x%%j%%in%%k/l*m+n-o<p>q<=r>=s==t!=u!v&wx&&y|z' + \
                '||a2~2b->c0a->>d0123456789a<-1234567890<<-e0a1b2=345f6789+a/(b)*((c))+(d-e)/f*g' + \
                '+(((d-e)/f)*g)+f1(a,b~,c,~d,e~(f+g),h~!i)'
    expected = 'a(RSyntacticName), ::(ROperatorBinary), b(RSyntacticName), ' + \
                ':::(ROperatorBinary), ba(RSyntacticName), $(ROperatorBinary), ' + \
                'c(RSyntacticName), @(ROperatorBinary), d(RSyntacticName), ^(ROperatorBinary), ' + \
                'e(RSyntacticName), :(ROperatorBinary), ea(RSyntacticName), %%%%(ROperatorBinary), ' + \
                'f(RSyntacticName), %%/%%(ROperatorBinary), g(RSyntacticName), %%*%%(ROperatorBinary), ' + \
                'h(RSyntacticName), %%o%%(ROperatorBinary), i(RSyntacticName), %%x%%(ROperatorBinary), ' + \
                'j(RSyntacticName), %%in%%(ROperatorBinary), k(RSyntacticName), /(ROperatorBinary), ' + \
                'l(RSyntacticName), *(ROperatorBinary), m(RSyntacticName), +(ROperatorBinary), ' + \
                'n(RSyntacticName), -(ROperatorBinary), o(RSyntacticName), <(ROperatorBinary), ' + \
                'p(RSyntacticName), >(ROperatorBinary), q(RSyntacticName), <=(ROperatorBinary), ' + \
                'r(RSyntacticName), >=(ROperatorBinary), s(RSyntacticName), ==(ROperatorBinary), ' + \
                't(RSyntacticName), !=(ROperatorBinary), u(RSyntacticName), !(ROperatorBinary), ' + \
                'v(RSyntacticName), &(ROperatorBinary), wx(RSyntacticName), &&(ROperatorBinary), ' + \
                'y(RSyntacticName), |(ROperatorBinary), z(RSyntacticName), ||(ROperatorBinary), ' + \
                'a2(RSyntacticName), ~(ROperatorBinary), 2b(RSyntacticName), ->(ROperatorBinary), ' + \
                'c0a(RSyntacticName), ->>(ROperatorBinary), d0123456789a(RSyntacticName), ' + \
                '<-(ROperatorBinary), 1234567890(RSyntacticName), <<-(ROperatorBinary), ' + \
                'e0a1b2(RSyntacticName), =(ROperatorBinary), 345f6789(RSyntacticName), ' + \
                '+(ROperatorBinary), a(RSyntacticName), /(ROperatorBinary), ((RBracket), ' + \
                'b(RSyntacticName), )(RBracket), *(ROperatorBinary), ((RBracket), ((RBracket), ' + \
                'c(RSyntacticName), )(RBracket), )(RBracket), +(ROperatorBinary), ((RBracket), ' + \
                'd(RSyntacticName), -(ROperatorBinary), e(RSyntacticName), )(RBracket), ' + \
                '/(ROperatorBinary), f(RSyntacticName), *(ROperatorBinary), g(RSyntacticName), ' + \
                '+(ROperatorBinary), ((RBracket), ((RBracket), ((RBracket), d(RSyntacticName), ' + \
                '-(ROperatorBinary), e(RSyntacticName), )(RBracket), /(ROperatorBinary), ' + \
                'f(RSyntacticName), )(RBracket), *(ROperatorBinary), g(RSyntacticName), ' + \
                ')(RBracket), +(ROperatorBinary), f1(RFunctionName), ((RBracket), ' + \
                'a(RSyntacticName), ,(RSeparator), b(RSyntacticName), ~(ROperatorUnaryLeft), ' + \
                ',(RSeparator), c(RSyntacticName), ,(RSeparator), ~(ROperatorUnaryRight), ' + \
                'd(RSyntacticName), ,(RSeparator), e(RSyntacticName), ~(ROperatorBinary), ' + \
                '((RBracket), f(RSyntacticName), +(ROperatorBinary), g(RSyntacticName), ' + \
                ')(RBracket), ,(RSeparator), h(RSyntacticName), ~(ROperatorBinary), ' + \
                '!(ROperatorUnaryRight), i(RSyntacticName), )(RBracket), '
    actual = get_tokens_as_string(rtoken.get_tokens(rlexeme.get_lexemes(input_string)))
    assert actual == expected

    # user-defined operators
    input_string = '.a%%%%a_2ab%%/%%ac%%*%%aba%%o%%aba2%%x%%abaa%%in%%abaaa%%>%%abcdefg%%mydefinedoperator%%hijklmnopqrstuvwxyz'
    expected = '.a(RSyntacticName), %%%%(ROperatorBinary), ' + \
                'a_2ab(RSyntacticName), %%/%%(ROperatorBinary), ' + \
                'ac(RSyntacticName), %%*%%(ROperatorBinary), ' + \
                'aba(RSyntacticName), %%o%%(ROperatorBinary), ' + \
                'aba2(RSyntacticName), %%x%%(ROperatorBinary), ' + \
                'abaa(RSyntacticName), %%in%%(ROperatorBinary), ' + \
                'abaaa(RSyntacticName), %%>%%(ROperatorBinary), ' + \
                'abcdefg(RSyntacticName), %%mydefinedoperator%%(ROperatorBinary), ' + \
                'hijklmnopqrstuvwxyz(RSyntacticName), '
    actual = get_tokens_as_string(rtoken.get_tokens(rlexeme.get_lexemes(input_string)))
    assert actual == expected

    # ROperatorBracket
    input_string = 'a[1]-b[c(d)+e]/f(g[2],h[3],i[4]*j[5])-k[l[m[6]]];df[["a"]];lst[["a"]]' + \
                '[["b"]]n[[[o][p]]]'
    expected = 'a(RSyntacticName), [(ROperatorBracket), 1(RSyntacticName), ' + \
                '](ROperatorBracket), -(ROperatorBinary), b(RSyntacticName), [(ROperatorBracket), ' + \
                'c(RFunctionName), ((RBracket), d(RSyntacticName), )(RBracket), +(ROperatorBinary), ' + \
                'e(RSyntacticName), ](ROperatorBracket), /(ROperatorBinary), f(RFunctionName), ' + \
                '((RBracket), g(RSyntacticName), [(ROperatorBracket), 2(RSyntacticName), ' + \
                '](ROperatorBracket), ,(RSeparator), h(RSyntacticName), [(ROperatorBracket), ' + \
                '3(RSyntacticName), ](ROperatorBracket), ,(RSeparator), i(RSyntacticName), ' + \
                '[(ROperatorBracket), 4(RSyntacticName), ](ROperatorBracket), *(ROperatorBinary), ' + \
                'j(RSyntacticName), [(ROperatorBracket), 5(RSyntacticName), ](ROperatorBracket), ' + \
                ')(RBracket), -(ROperatorBinary), k(RSyntacticName), [(ROperatorBracket), ' + \
                'l(RSyntacticName), [(ROperatorBracket), m(RSyntacticName), [(ROperatorBracket), ' + \
                '6(RSyntacticName), ](ROperatorBracket), ](ROperatorBracket), ](ROperatorBracket), ' + \
                ';(REndStatement), df(RSyntacticName), [[(ROperatorBracket), "a"(RStringLiteral), ' + \
                ']](ROperatorBracket), ;(REndStatement), lst(RSyntacticName), [[(ROperatorBracket), ' + \
                '"a"(RStringLiteral), ]](ROperatorBracket), [[(ROperatorBracket), ' + \
                '"b"(RStringLiteral), ]](ROperatorBracket), n(RSyntacticName), [[(ROperatorBracket), ' + \
                '[(ROperatorBracket), o(RSyntacticName), ](ROperatorBracket), [(ROperatorBracket), ' + \
                'p(RSyntacticName), ](ROperatorBracket), ]](ROperatorBracket), '
    actual = get_tokens_as_string(rtoken.get_tokens(rlexeme.get_lexemes(input_string)))
    assert actual == expected

    # end statement excluding key words
    input_string = 'complete' + \
                '\ncomplete()' + \
                '\ncomplete(a[b],c[[d]])' + \
                '\ncomplete #' + \
                '\ncomplete ' + \
                '\ncomplete + !e' + \
                '\ncomplete() -f' + \
                '\ncomplete() * g~' + \
                '\nincomplete::\n' + \
                '\nincomplete::h i::: \nia' + \
                '\nincomplete %%>%% #comment\nib' + \
                '\nincomplete(\nic)' + \
                '\nincomplete()[id \n]' + \
                '\nincomplete([[j[k]]]  \n)' + \
                '\nincomplete >= \n  #comment \n\nl\n'
    expected = 'complete(RSyntacticName), ' + \
                '\n(REndStatement), complete(RFunctionName), ((RBracket), )(RBracket), ' + \
                '\n(REndStatement), complete(RFunctionName), ((RBracket), a(RSyntacticName), ' + \
                '[(ROperatorBracket), b(RSyntacticName), ](ROperatorBracket), ,(RSeparator), ' + \
                'c(RSyntacticName), [[(ROperatorBracket), d(RSyntacticName), ]](ROperatorBracket), )(RBracket), ' + \
                '\n(REndStatement), complete(RSyntacticName),  (RSpace), #(RComment), ' + \
                '\n(REndStatement), complete(RSyntacticName),  (RSpace), ' + \
                '\n(REndStatement), complete(RSyntacticName),  (RSpace), +(ROperatorBinary), ' + \
                ' (RSpace), !(ROperatorUnaryRight), e(RSyntacticName), ' + \
                '\n(REndStatement), complete(RFunctionName), ((RBracket), )(RBracket), ' + \
                ' (RSpace), -(ROperatorBinary), f(RSyntacticName), ' + \
                '\n(REndStatement), complete(RFunctionName), ((RBracket), )(RBracket), ' + \
                ' (RSpace), *(ROperatorBinary),  (RSpace), g(RSyntacticName), ~(ROperatorUnaryLeft), ' + \
                '\n(REndStatement), incomplete(RSyntacticName), ::(ROperatorBinary), ' + \
                '\n(RNewLine), ' + \
                '\n(RNewLine), incomplete(RSyntacticName), ::(ROperatorBinary), ' + \
                'h(RSyntacticName),  (RSpace), i(RSyntacticName), :::(ROperatorBinary),  (RSpace), ' + \
                '\n(RNewLine), ia(RSyntacticName), ' + \
                '\n(REndStatement), incomplete(RSyntacticName),  (RSpace), %%>%%(ROperatorBinary), ' + \
                ' (RSpace), #comment(RComment), ' + \
                '\n(RNewLine), ib(RSyntacticName), ' + \
                '\n(REndStatement), incomplete(RFunctionName), ((RBracket), ' + \
                '\n(RNewLine), ic(RSyntacticName), )(RBracket), ' + \
                '\n(REndStatement), incomplete(RFunctionName), ((RBracket), )(RBracket), ' + \
                '[(ROperatorBracket), id(RSyntacticName),  (RSpace), ' + \
                '\n(RNewLine), ](ROperatorBracket), ' + \
                '\n(REndStatement), incomplete(RFunctionName), ((RBracket), [[(ROperatorBracket), ' + \
                'j(RSyntacticName), [(ROperatorBracket), k(RSyntacticName), ](ROperatorBracket), ' + \
                ']](ROperatorBracket),   (RSpace), ' + \
                '\n(RNewLine), )(RBracket), ' + \
                '\n(REndStatement), incomplete(RSyntacticName),  (RSpace), >=(ROperatorBinary),  (RSpace), ' + \
                '\n(RNewLine),   (RSpace), #comment (RComment), ' + \
                '\n(RNewLine), ' + \
                '\n(RNewLine), l(RSyntacticName), \n(REndScript), '
    actual = get_tokens_as_string(rtoken.get_tokens(rlexeme.get_lexemes(input_string)))
    assert actual == expected

def test_get_as_executable_script():
    # RSyntacticName
    input_string = 'a+b\n'
    actual = rscript.RScript(input_string).get_as_executable_script()
    assert actual == input_string

