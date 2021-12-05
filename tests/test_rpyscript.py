import rscript

def test_get_lst_lexemes():
    r_script = rscript.RScript('nothing')
    lexemes_expected = ['a', '::', 'b'] # list type
    lexemes_actual = r_script.get_lst_lexemes("test")
    assert lexemes_actual == lexemes_expected

    #lexemes_expected = ('a", "::", "b", ":::", "ba", "$", "c", "@", "d", "^", "e", ":", "ea", "\%\%", "f", "%/%", "g", "\%\*\%", "h", "%o%", "i", "\%x%", "j", "%in%", "k", "/", "l", "*", "m", "+", "n", "-", "o", "<", "p", ">", "q", "<=", "r", ">=", "s", "==", "t", "!=", "u", "!", "v", "&", "wx", "&&", "y", "|", "z", "||", "a2", "~", "2b", "->", "c0a", "->>", "d0123456789a", "<-", "1234567890", "<<-", "e0a1b2", "=", "345f6789")
    #lexemes_actual = r_script.get_lst_lexemes('a::b:::ba$c@d^e:ea%%f%/%g%*%h%o%i%x%j%in%k/l*m+n-o<p>q<=r>=s==t!=u!v&wx&&y|z||a2~2b->c0a->>d012345678' + '9a<-1234567890<<-e0a1b2=345f6789')
