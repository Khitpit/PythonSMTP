import sys

# Special characters not allowed as a 'character' in the parse_char function
special_chars = ['<', '>', '(', ')', '[', ']', '\\', '.', ',', ';', ':', '@', '"']

def parse_mail_from_cmd(string_left_to_parse):

    string_left_to_parse = parse_literal_string(string_left_to_parse, 'MAIL')
    if string_left_to_parse == -1:
        print("ERROR -- mail-from-cmd")
        return -1

    string_left_to_parse = parse_whitespace(string_left_to_parse)
    if string_left_to_parse == -1:
        print("ERROR -- whitespace")
        return -1

    string_left_to_parse = parse_literal_string(string_left_to_parse, 'FROM:')
    if string_left_to_parse == -1:
        print("ERROR -- mail-from-cmd")
        return -1

    string_left_to_parse = parse_nullspace(string_left_to_parse)

    string_left_to_parse = parse_reverse_path(string_left_to_parse)
    if string_left_to_parse == -1:
        return -1

    string_left_to_parse = parse_nullspace(string_left_to_parse)

    string_left_to_parse = parse_CRLF(string_left_to_parse)
    if string_left_to_parse == -1:
        return -1

    if string_left_to_parse == None:
        print('Sender ok')

def parse_literal_string(string_left_to_parse, parse_string):
    if(string_left_to_parse[:len(parse_string)] != parse_string):
        return -1
    else:
        string_left_to_parse = string_left_to_parse[len(parse_string):]
        return string_left_to_parse
        
def parse_whitespace(string_left_to_parse):
    if parse_SP(string_left_to_parse) == -1:
        return -1
    else:
        string_left_to_parse = parse_SP(string_left_to_parse)
        while parse_SP(string_left_to_parse) != -1:
            string_left_to_parse = parse_SP(string_left_to_parse)
        return string_left_to_parse

def parse_SP(string_left_to_parse):
    if parse_literal_string(string_left_to_parse, '\t') == -1:
        if parse_literal_string(string_left_to_parse, ' ') == -1:
            return -1
        else:
            return parse_literal_string(string_left_to_parse, ' ')
    else:
        return parse_literal_string(string_left_to_parse, '\t')

def parse_nullspace(string_left_to_parse):
    if parse_whitespace(string_left_to_parse) == -1:
        return string_left_to_parse
    else:
        return parse_whitespace(string_left_to_parse)

def parse_reverse_path(string_left_to_parse):
    return parse_path(string_left_to_parse)

def parse_path(string_left_to_parse):
    string_left_to_parse = parse_literal_string(string_left_to_parse, '<')
    if string_left_to_parse == -1:
        print('ERROR -- path')
        return -1

    string_left_to_parse = parse_mailbox(string_left_to_parse)
    if string_left_to_parse == -1:
        return -1

    string_left_to_parse = parse_literal_string(string_left_to_parse, '>')
    if string_left_to_parse == -1:
        print('ERROR -- path')
        return -1
    
    return string_left_to_parse

def parse_mailbox(string_left_to_parse):
    string_left_to_parse = parse_local_part(string_left_to_parse)
    if string_left_to_parse == -1:
        return -1

    string_left_to_parse = parse_literal_string(string_left_to_parse, '@')
    if string_left_to_parse == -1:
        print('ERROR -- mailbox')
        return -1

    string_left_to_parse = parse_domain(string_left_to_parse)
    if string_left_to_parse == -1:
        return -1

    return string_left_to_parse

def parse_local_part(string_left_to_parse):
    return parse_string(string_left_to_parse)

def parse_string(string_left_to_parse):
    if parse_char(string_left_to_parse) == -1:
        print("ERROR -- string")
        return -1
    else:
        string_left_to_parse = parse_char(string_left_to_parse)
        while parse_char(string_left_to_parse) != -1:
            string_left_to_parse = parse_char(string_left_to_parse)
        return string_left_to_parse

def parse_char(string_left_to_parse):
    ascii_value = ord(string_left_to_parse[0])
    if ascii_value < 33 or ascii_value > 126 or special_chars.count(string_left_to_parse[0]) > 0:
        return -1
    else:
        return string_left_to_parse[1:]

def parse_domain(string_left_to_parse):
    if parse_element(string_left_to_parse) == -1:
        return -1
    else:
        string_left_to_parse = parse_element(string_left_to_parse)
        if parse_literal_string(string_left_to_parse, '.') != -1:
            string_left_to_parse = parse_literal_string(string_left_to_parse, '.')
            return parse_domain(string_left_to_parse)
        else:
            return string_left_to_parse            

def parse_element(string_left_to_parse):
    if parse_name(string_left_to_parse) == -1:
        if parse_letter(string_left_to_parse) == -1:
            print("ERROR -- element")
            return -1
        else:
            return parse_letter(string_left_to_parse)
    else:
        string_left_to_parse = parse_name(string_left_to_parse)
        return string_left_to_parse

def parse_name(string_left_to_parse):
    string_left_to_parse = parse_letter(string_left_to_parse)
    if string_left_to_parse == -1:
        return -1

    string_left_to_parse = parse_let_dig_str(string_left_to_parse)
    if string_left_to_parse == -1:
        return -1

    return string_left_to_parse

def parse_letter(string_left_to_parse):
    ascii_value = ord(string_left_to_parse[0])
    if (ascii_value >= 65 and ascii_value <= 90) or (ascii_value >= 97 and ascii_value <= 122):
        return string_left_to_parse[1:]
    else:
        return -1

def parse_let_dig_str(string_left_to_parse):
    if parse_let_dig(string_left_to_parse) == -1:
        return -1
    else:
        string_left_to_parse = parse_let_dig(string_left_to_parse)
        while parse_let_dig_str(string_left_to_parse) != -1:
            string_left_to_parse = parse_let_dig_str(string_left_to_parse)
        return string_left_to_parse

def parse_let_dig(string_left_to_parse):
    if parse_letter(string_left_to_parse) == -1:
        if parse_digit(string_left_to_parse) == -1:
            return -1
        else:
            return parse_digit(string_left_to_parse)
    else:
        return parse_letter(string_left_to_parse)

def parse_digit(string_left_to_parse):
    ascii_value = ord(string_left_to_parse[0])
    if ascii_value >= 48 and ascii_value <= 57:
        return string_left_to_parse[1:]
    else:
        return -1

def parse_CRLF(string_left_to_parse):
    string_left_to_parse = parse_literal_string(string_left_to_parse, '\n')
    if string_left_to_parse == -1:
        print("ERROR -- CRLF")
        return -1

for line in sys.stdin:
    print(line, end="")
    parse_mail_from_cmd(line)