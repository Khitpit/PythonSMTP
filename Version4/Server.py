# UNC Honor Pledge: I certify that no unauthorized assistance has been received or given in the completion of this work
# Aayush Singh

import sys
import os
import socket

# Special characters not allowed as a 'character' in the parse_char function
special_chars = ['<', '>', '(', ')', '[', ']', '\\',
                 '.', ',', ';', ':', '@', '"']


def send_message(message, conn):
    # print(message)  # for debugging
    # return True
    conn.send(message.encode())
    return True


def get_message(conn):
    # return sys.stdin.readline()  # for debugging
    response = False
    while (not response):
        response = conn.recv(1024).decode()
    return response


def get_socket_next_line(conn):
    # return sys.stdin.readline()  # for debugging
    line = ''
    while (not line.endswith('\n')):
        line += conn.recv(1).decode()
    return line


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
    if (string_left_to_parse[:len(parse_string)] != parse_string):
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


def parse_quit_cmd(string_left_to_parse):
    if (string_left_to_parse[:len('QUIT')] != 'QUIT'):
        return -1

    if string_left_to_parse == 'QUIT\n':
        return 0

    return 1


def parse_data_body(string_left_to_parse):
    return '250 OK'


def read_emails(conn):
    current_state = 'waiting for mail cmd'
    fromTextBuffer = ''
    toTextBuffer = ''
    bodyTextBuffer = ''
    while (True):
        line = get_socket_next_line(conn)
        if (line != None):
            if (parse_quit_cmd(line) != -1):
                break
            mail = parse_mail_from_cmd(line)
            rcpt = parse_rcpt_to_cmd(line)
            data = parse_data_cmd(line)
            match current_state:
                case 'waiting for mail cmd':
                    if (mail != -1):  # We are reading a mail cmd
                        if (mail == 1):  # if it's args are wrong
                            try:
                                send_message('501 Syntax error in parameters or arguments', conn)
                            except:
                                pass
                            return 'waiting for quit'
                        elif (mail == 0):  # if it's a valid mail cmd
                            try:
                                send_message('250 OK', conn)
                            except:
                                return 'conn closed'
                            fromTextBuffer = 'From: ' + line[line.index('<'):line.index('>')+1] + '\n'
                            current_state = 'waiting for first rcpt'
                    elif (rcpt != -1 or data != -1):  # We are reading another cmd
                        try:
                            send_message('503 Bad sequence of commands', conn)
                        except:
                            pass
                        return 'waiting for quit'
                    else:  # We are reading none of those three cmds
                        try:
                            send_message('500 Syntax error: command unrecognized', conn)
                        except:
                            pass
                        return 'waiting for quit'

                case 'waiting for first rcpt':
                    if (mail != -1 or data != -1):  # We are reading a mail or data cmd
                        try:
                            send_message('503 Bad sequence of commands', conn)
                        except:
                            pass
                        return 'waiting for quit'
                    elif (rcpt != -1):  # We are reading a rcpt cmd
                        if (rcpt == 1):  # if it's args are wrong
                            try:
                                send_message('501 Syntax error in parameters or arguments', conn)
                            except:
                                pass
                            return 'waiting for quit'
                        elif (rcpt == 0):  # if it's a valid rcpt cmd
                            try:
                                send_message('250 OK', conn)
                            except:
                                return 'conn closed'
                            toTextBuffer = 'To: ' + \
                                line[line.index('<'):line.index('>')+1] + '\n'
                            current_state = 'waiting for rcpt or data'
                    else:  # We are reading none of those three cmds
                        try:
                            send_message('500 Syntax error: command unrecognized', conn)
                        except:
                            pass
                        return 'waiting for quit'

                case 'waiting for rcpt or data':
                    if (mail != -1):  # We are reading a mail cmd
                        try:
                            send_message('503 Bad sequence of commands', conn)
                        except:
                            pass
                        return 'waiting for quit'
                    elif (rcpt != -1):  # We are reading a rcpt cmd
                        if (rcpt == 1):  # if it's args are wrong
                            try:
                                send_message('501 Syntax error in parameters or arguments', conn)
                            except:
                                pass
                            return 'waiting for quit'
                        elif (rcpt == 0):  # if it's a valid rcpt cmd
                            try:
                                send_message('250 OK', conn)
                            except:
                                return 'conn closed'
                            toTextBuffer += 'To: ' + line[line.index('<'):line.index('>')+1] + '\n'
                            current_state = 'waiting for rcpt or data'
                    elif (data != -1):  # We are reading a data cmd
                        if (data == 1):  # if it's args are wrong
                            try:
                                send_message('501 Syntax error in parameters or arguments', conn)
                            except:
                                pass
                            return 'waiting for quit'
                        elif (data == 0):  # if it's a valid data cmd
                            try:
                                send_message('354 Start mail input; end with <CRLF>.<CRLF>', conn)
                            except:
                                return 'conn closed'
                            current_state = 'reading data body'
                    else:  # We are reading none of those three cmds
                        try:
                            send_message('500 Syntax error: command unrecognized', conn)
                        except:
                            pass
                        return 'waiting for quit'

                case 'reading data body':
                    if (line == ".\n"):
                        try:
                            send_message("250 OK", conn)
                        except:
                            return 'conn closed'
                        printToDirectory(fromTextBuffer, toTextBuffer, bodyTextBuffer)
                        return 'waiting for quit'
                    else:
                        bodyTextBuffer += line


def printToDirectory(fromTextBuffer, toTextBuffer, bodyTextBuffer):
    if (not os.getcwd().endswith('forward')):
        try:
            os.chdir(os.path.abspath(os.path.dirname(__file__)) + '/forward')
        except Exception as e:
            pass

    recipientPaths = toTextBuffer.splitlines()
    unique_domains = []
    for str in recipientPaths:
        domain = str.split('@')[1][:-1]
        if (not domain in unique_domains):
            unique_domains.append(domain)

    for unique_domain in unique_domains:
        try:
            file = open(unique_domain, "a")
            file.write(bodyTextBuffer)
            file.close()
        except Exception as e:
            pass

try:
    portNum = int(sys.argv[1])
except:
    print('Invalid port number')
    exit()

try:
    welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    welcome_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    welcome_socket.bind(('', portNum))
    welcome_socket.listen(1)
except:
    print('Welcome socket error')
    exit()


while (True):  # while welcome port is working
    conn, addr = welcome_socket.accept()
    # conn = None  # for debugging
    while (True):  # while connection with a client is established
        try:
            send_message('220 comp431sp23.cs.unc.edu', conn)
        except:
            try:
                conn.close()
            finally:
                break

        try:
            response = get_message(conn)
        except:
            print('Failed to receive after sending 220')
            try:
                conn.close()
            finally:
                break

        if (response == False or response[:len('HELO')] != 'HELO'):
            print('Improper greeting message')
            try:
                conn.close()
            finally:
                break

        try:
            send_message('250 Hello comp431sp23b.cs.unc.edu pleased to meet you', conn)
        except:
            print('Failed to send 250 Hello')
            try:
                conn.close()
            finally:
                break

        result = read_emails(conn)
        if (result == 'waiting for quit' or result == 'conn closed'):
            try:
                response = get_message(conn)
            except:
                break

        try:
            send_message('221 comp432sp23.cs.unc.edu closing connection', conn)
            conn.close()
        finally:
            break
