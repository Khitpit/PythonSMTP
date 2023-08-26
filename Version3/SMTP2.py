import sys

def readResponse(expected_response_code):
    input = sys.stdin.readline()
    sys.stderr.write(input)
    if(input[:3] != expected_response_code):
        print('QUIT')
        exit()

try:
    filepath = sys.argv[1]
    fp = open(filepath, 'r')
    content = fp.readlines()
    fp.close()
except Exception as e:
    exit()

# current_state can be parseFrom, firstParseTo, secondParseTo, parseBody
current_state = 'parseFrom'
for line in content:
    if(current_state == 'parseFrom'):
        if(line[:5] == 'From:'):
            output = line.replace('From:', 'MAIL FROM:')
            print(output, end = '')
            readResponse('250')
            current_state = 'firstParseTo'
    elif(current_state == 'firstParseTo'):
        if(line[:3] == 'To:'):
            output = line.replace('To:', 'RCPT TO:')
            print(output, end = '')
            readResponse('250')
            current_state = 'secondParseTo'
    elif(current_state == 'secondParseTo'):
        if(line[:3] == 'To:'):
            output = line.replace('To:', 'RCPT TO:')
            print(output, end = '')
            readResponse('250')
        else:
            print('DATA')
            readResponse('354')
            current_state = 'parseBody'
    if(current_state == 'parseBody'):
        if(line[:5] == 'From:'):
            print('.\n', end='')
            readResponse('250')
            output = line.replace('From:', 'MAIL FROM:')
            print(output, end = '')
            readResponse('250')
            current_state = 'firstParseTo'
        else:
            print(line, end = '')
print('.\n', end='')
readResponse('250')
print('QUIT')