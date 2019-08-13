import re

class TokenStream(object):
    def __init__(self):
        self.allowed_tokens = []

    def add_token(self, token):
        self.allowed_tokens.append(token)

    def tokenize(self, string):
        while(len(string) > 0):
            for tok in self.allowed_tokens:
                match = tok.regex.match(string)
                if match:
                    string = string[match.end():]
                    yield self._gen_token(tok, match)
    
    @staticmethod
    def _gen_token(token, match):
        value = match.groups() 
        return LexedToken(
            token.name,
            match.span(),
            value
            )

class RegexToken(object):
    def __init__(self, name, regex):
        self.name = name
        self.regex = re.compile(regex)

class LexedToken(object):
    def __init__(self, name, span, value=None):
        self.name = name
        self.span = span
        self.value = value

    def __str__(self):
        if len(self.value) == 0:
            return self.name
        else:
            return self.name+"("+",".join(self.value)+")"

def main():
    stream = TokenStream()

    stream.add_token(RegexToken("WHITESPACE", r'\s+'))
    stream.add_token(RegexToken("R_PAREN", r'\)'))
    stream.add_token(RegexToken("L_PAREN", r'\('))
    stream.add_token(RegexToken("DECIMAL", r'([0-9]+\.[0-9]*)'))
    stream.add_token(RegexToken("LITERAL_INT", r'([0-9]+)'))

    tokens = list(stream.tokenize("10 200 (50.0)"))
    
    macro = Macro("__for", Arg("a"), Arg("b"), Arg("body"), syntax=[
        Keyword("for"),
        Arg("a"),
        Keyword("in"),
        Arg("b"),
        Symbol("COLON"),
        Arg("body")
    ])

    # "for a in b: body" => "__for(a, b, body)"

    print(" ".join(map(str, tokens)))

if __name__ == '__main__':
    main()