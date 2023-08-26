# UNC Honor Pledge: I certify that no unauthorized assistance has been received or given in the completion of this work
# Aayush Singh

import sys
import os

# Special characters not allowed as a 'character' in the parse_char function
special_chars = ['<', '>', '(', ')', '[', ']', '\\', '.', ',', ';', ':', '@', '"']

def parse_mail_from_cmd(string_left_to_parse):

    string_left_to_parse = parse_literal_string(string_left_to_parse, 'MAIL')
    if string_left_to_parse == -1:
        return -1

    string_left_to_parse = parse_whitespace(string_left_to_parse)
    if string_left_to_parse == -1:
        return -1

    string_left_to_parse = parse_literal_string(string_left_to_parse, 'FROM:')
    if string_left_to_parse == -1:
        return -1

    string_left_to_parse = parse_nullspace(string_left_to_parse)

    string_left_to_parse = parse_reverse_path(string_left_to_parse)
    if string_left_to_parse == -1:
        return 1

    string_left_to_parse = parse_nullspace(string_left_to_parse)

    string_left_to_parse = parse_CRLF(string_left_to_parse)
    if string_left_to_parse == -1:
        return 1

    if string_left_to_parse == None:
        return 0

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
        return -1

    string_left_to_parse = parse_mailbox(string_left_to_parse)
    if string_left_to_parse == -1:
        return -1

    string_left_to_parse = parse_literal_string(string_left_to_parse, '>')
    if string_left_to_parse == -1:
        return -1
    
    return string_left_to_parse

def parse_mailbox(string_left_to_parse):
    string_left_to_parse = parse_local_part(string_left_to_parse)
    if string_left_to_parse == -1:
        return -1

    string_left_to_parse = parse_literal_string(string_left_to_parse, '@')
    if string_left_to_parse == -1:
        return -1

    string_left_to_parse = parse_domain(string_left_to_parse)
    if string_left_to_parse == -1:
        return -1

    return string_left_to_parse

def parse_local_part(string_left_to_parse):
    return parse_string(string_left_to_parse)

def parse_string(string_left_to_parse):
    if parse_char(string_left_to_parse) == -1:
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
        return -1

def parse_rcpt_to_cmd(string_left_to_parse):
    string_left_to_parse = parse_literal_string(string_left_to_parse, 'RCPT')
    if string_left_to_parse == -1:
        return -1

    string_left_to_parse = parse_whitespace(string_left_to_parse)
    if string_left_to_parse == -1:
        return -1

    string_left_to_parse = parse_literal_string(string_left_to_parse, 'TO:')
    if string_left_to_parse == -1:
        return -1

    string_left_to_parse = parse_nullspace(string_left_to_parse)

    string_left_to_parse = parse_forward_path(string_left_to_parse)
    if string_left_to_parse == -1:
        return 1

    string_left_to_parse = parse_nullspace(string_left_to_parse)

    string_left_to_parse = parse_CRLF(string_left_to_parse)
    if string_left_to_parse == -1:
        return 1

    if string_left_to_parse == None:
        return 0

def parse_forward_path(string_left_to_parse):
    return parse_path(string_left_to_parse)

def parse_data_cmd(string_left_to_parse):
    string_left_to_parse = parse_literal_string(string_left_to_parse, 'DATA')
    if string_left_to_parse == -1:
        return -1

    string_left_to_parse = parse_nullspace(string_left_to_parse)

    string_left_to_parse = parse_CRLF(string_left_to_parse)
    if string_left_to_parse == -1:
        return 1

    if string_left_to_parse == None:
        return 0

def parse_data_body(string_left_to_parse):
    return '250 OK'

def read_emails():
    current_state = 'waiting for mail cmd'
    fromTextBuffer = ''
    toTextBuffer = ''
    bodyTextBuffer = ''
    for line in sys.stdin:
        print(line, end="")
        match current_state:
            case 'waiting for mail cmd':
                mail = parse_mail_from_cmd(line)
                rcpt = parse_rcpt_to_cmd(line)
                data = parse_data_cmd(line)
                if(mail != -1): #We are reading a mail cmd
                    if(mail == 1): #if it's args are wrong
                        print('501 Syntax error in parameters or arguments')
                    elif(mail == 0): #if it's a valid mail cmd
                        print('250 OK')
                        fromTextBuffer = 'From: ' + line[line.index('<'):line.index('>')+1] + '\n'
                        current_state = 'waiting for first rcpt'
                elif(rcpt != -1 or data != -1): #We are reading another cmd
                    print('503 Bad sequence of commands')
                else: #We are reading none of those three cmds
                    print('500 Syntax error: command unrecognized')

            case 'waiting for first rcpt':
                mail = parse_mail_from_cmd(line)
                rcpt = parse_rcpt_to_cmd(line)
                data = parse_data_cmd(line)
                if(mail != -1 or data != -1): #We are reading a mail or data cmd
                    print('503 Bad sequence of commands')
                    current_state = 'waiting for mail cmd'
                elif(rcpt != -1): #We are reading a rcpt cmd
                    if(rcpt == 1): #if it's args are wrong
                        print('501 Syntax error in parameters or arguments')
                        current_state = 'waiting for mail cmd'
                    elif(rcpt == 0): #if it's a valid rcpt cmd
                        print('250 OK')
                        toTextBuffer = 'To: ' + line[line.index('<'):line.index('>')+1] + '\n'
                        current_state = 'waiting for rcpt or data'
                else: #We are reading none of those three cmds
                    print('500 Syntax error: command unrecognized')
                    current_state = 'waiting for mail cmd'

            case 'waiting for rcpt or data':
                mail = parse_mail_from_cmd(line)
                rcpt = parse_rcpt_to_cmd(line)
                data = parse_data_cmd(line)
                if(mail != -1): #We are reading a mail cmd
                    print('503 Bad sequence of commands')
                    current_state = 'waiting for mail cmd'
                elif(rcpt != -1): #We are reading a rcpt cmd
                    if(rcpt == 1): #if it's args are wrong
                        print('501 Syntax error in parameters or arguments')
                        current_state = 'waiting for mail cmd'
                    elif(rcpt == 0): #if it's a valid rcpt cmd
                        print('250 OK')
                        toTextBuffer += 'To: ' + line[line.index('<'):line.index('>')+1] + '\n'
                elif(data != -1): #We are reading a data cmd
                    if(data == 1): #if it's args are wrong
                        print('501 Syntax error in parameters or arguments')
                        current_state = 'waiting for mail cmd'
                    elif(data == 0): #if it's a valid data cmd
                        print('354 Start mail input; end with <CRLF>.<CRLF>')
                        current_state = 'reading data body'
                else: #We are reading none of those three cmds
                    print('500 Syntax error: command unrecognized')
                    current_state = 'waiting for mail cmd'

            case 'reading data body':
                if(line == ".\n"):
                    print("250 OK")
                    printToDirectory(fromTextBuffer, toTextBuffer, bodyTextBuffer)
                    fromTextBuffer = ''
                    toTextBuffer = ''
                    bodyTextBuffer = ''
                    current_state = 'waiting for mail cmd'
                else:
                    bodyTextBuffer += line
    if(current_state == 'reading data body'):
        print('501 Syntax error in parameters or arguments')
    
def printToDirectory(fromTextBuffer, toTextBuffer, bodyTextBuffer):
    if(not os.getcwd().endswith('forward')):
        try:
            os.chdir(os.getcwd() + '/forward')
        except Exception as e:
            ()
            #print(e)
    recipientPaths = toTextBuffer.splitlines()
    for str in recipientPaths:
        pathWithoutBrackets = str[str.index('<')+1:str.index('>')]
        print(pathWithoutBrackets)
        try:
            file = open(pathWithoutBrackets, "a")
            file.write(fromTextBuffer + toTextBuffer + bodyTextBuffer)
            file.close()
        except Exception as e:
            ()
            #print(e)


read_emails()