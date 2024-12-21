import re

TOKEN_SPECIFICATIONS = [
    ('Keywords', r'\b(if|else|switch|case|default|while|for|do|break|continue|goto|int|short|long|float|double|void|bool|char|string|signed|unsiged|auto|const|static|new|delete|using|namespace|try|throw|catch|class|struct|union|public|private|protected|friend|this|virtusl|return|true|false)\b'),
    ('Identifiers', r'[a-zA-Z_]\w*'),
    ('Numeric_constants', r'\b\d+(\.\d+)?([eE][+-]?\d+)?\b'),
    ('Operators', r'\+\+|--|\+=|-=|\=|/=|%=|&=|\|=|\^=|<<=|>>=|\+|-|\|/|%|==|!=|<|>|<=|>=|&&|\|\||!|&|\||\^|~|<<|>>|=|\? :|,|->|\.'),
    ('Special_characters', r'[{}();,]'),
    ('Character_constants', r"'.'"),
    ('Comments', r'//.?$|/\.?\/'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.'),
]

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        if self.type == 'Identifiers':
            return f"<Identifiers, \"{self.value}\">"
        elif self.type == 'Numeric_constants':
            return f"<Numeric constants, {self.value}>"
        elif self.type == 'Keywords':
            return f"<Keywords, {self.value}>"
        elif self.type == 'Character_constants':
            return f"<Character constants, {self.value}>"
        elif self.type == 'Operators':
            return f"<Operators, {self.value}>"
        elif self.type == 'Special_characters':
            return f"<Special characters, {self.value}>"
        elif self.type == 'Comments':
            return f"<Comments, {self.value}>"
        else:
            return f"<{self.type}, {self.value}>"

def tokenize(code):
    tokens = []
    line_num = 1
    line_start = 0
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATIONS)
    get_token = re.compile(tok_regex, re.DOTALL | re.MULTILINE).match

    pos = 0
    match = get_token(code)
    while match is not None:
        type = match.lastgroup
        value = match.group(type)
        if type == 'NEWLINE':
            line_start = pos
            line_num += 1
        elif type == 'SKIP':
            pass  # Ignore whitespace
        elif type == 'MISMATCH':
            print(f"Unexpected character {value!r} on line {line_num}")
        else:
            column = pos - line_start
            tokens.append(Token(type, value, line_num, column))
        pos = match.end()
        match = get_token(code, pos)
    return tokens

def main():
    print("Enter your C++ code below (end with an empty line):")
    cpp_code = ""
    while True:
        line = input()
        if line == "":
            break
        cpp_code += line + "\n"
    
    try:
        tokens = tokenize(cpp_code)

        output = ' '.join(str(token) for token in tokens)
        print(output)

    except RuntimeError as e:
        print(f"Runtime error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
