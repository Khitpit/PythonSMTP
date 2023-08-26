# UNC Honor Pledge: I certify that no unauthorized assistance has been received or given in the completion of this work
# Aayush Singh

import sys
import os
import socket

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
        return 1

    string_left_to_parse = parse_domain(string_left_to_parse)
    if string_left_to_parse == -1:
        return 1

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
  
def launch_client():
    # parse_mailbox expects a \n character at the end of the string
    # so we append it, and then make sure there are no characters left
    # after parsing and consuming the mailbox
    print('From:')
    try:
        fromResponse = sys.stdin.readline()[:-1]
    except EOFError:
        exit()

    while(parse_mailbox(fromResponse + '\n') != '\n'):
        print('Error recognising mailbox. Please try again. From:')
        try:
            fromResponse = sys.stdin.readline()[:-1]
        except EOFError:
            exit()

    allCorrect = True
    print('To:')
    try:
        toResponse = sys.stdin.readline()[:-1]
    except EOFError:
        exit()
    toResponse = toResponse.split(',')
    if(len(toResponse) == 0): allCorrect = False
    for string in toResponse:
        string = string.strip()
        correct = parse_mailbox(string + '\n') == '\n'
        if(not correct): allCorrect = False
    while(not allCorrect):
        print('Error recognising mailbox. Please try again. To:')
        try:
            toResponse = sys.stdin.readline()[:-1]
        except EOFError:
            exit()
        toResponse = toResponse.split(',')
        allCorrect = True
        if(len(toResponse) == 0): allCorrect = False
        for string in toResponse:
            string = string.strip()
            correct = parse_mailbox(string + '\n') == '\n'
            if(not correct): allCorrect = False

    print('Subject:')
    try:
        subject = sys.stdin.readline()[:-1]
    except EOFError:
        exit()

    message = ''
    print('Message:')
    try:
        inputted_line = sys.stdin.readline()
    except EOFError:
        exit()

    while(inputted_line != '.\n'):
        message += inputted_line
        try:
            inputted_line = sys.stdin.readline()
        except EOFError:
            exit()
    message += '.\n'

    #do some formatting for the "To:" responses
    toResponses = []
    for string in toResponse:
        toResponses.append(string.strip())

    return (fromResponse, toResponses, subject, message)

def send_message(message, conn):
    conn.send(message.encode())

def require_response_code(response_code, conn):
    response = False
    while(not response):
        response = conn.recv(1024).decode()
    if(response_code != None and response[:len(response_code)] != response_code):
        try:
            send_message('QUIT\n', conn)
            require_response_code('221', conn)
        finally:
            conn.close()
            exit()
    else:
        return response

try:
    try:
        serverName = sys.argv[1]
        portNum = int(sys.argv[2])
        domainName = 'cs.unc.edu'
    except:
        exit()

    (fromResponse, toResponses, subject, message) = launch_client()

    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        conn.connect((serverName, portNum))
    except:
        print('Connection to server failed')
        exit()


    # Do the SMTP handshake 
    require_response_code('220', conn)
    send_message(('HELO ' + serverName), conn)
    require_response_code('250', conn)


    send_message('MAIL FROM: <' + fromResponse + '>\n', conn)
    require_response_code('250', conn)

    for rcpt in toResponses:
        send_message('RCPT TO: <' + rcpt + '>\n', conn)
        require_response_code('250', conn)

    send_message('DATA\n', conn)
    require_response_code('354', conn)

    # Sending the RFC 822 compliant data headers below:
    send_message('From: <' + fromResponse + '>\n', conn)

    to_line = 'To: '
    for rcpt in toResponses:
        to_line += ('<' + rcpt + '>, ')
    to_line = to_line[:-2] + '\n'
    send_message(to_line, conn)

    send_message('Subject: ' + subject + '\n', conn)

    # Blank line to separate RFC822 headers from actual message body
    send_message('\n', conn) 

    # Sending actual message body
    send_message(message, conn)
    require_response_code('250', conn)

    send_message('QUIT\n', conn)
    require_response_code('221', conn)
except Exception as e:
    print("Error")
    try:
        conn.close()
    finally:
        exit()