# PythonSMTP

PythonSMTP is my personal python implementation of the SMTP protocol as outlined in [RFC 821](https://www.rfc-editor.org/rfc/rfc821). There are four versions - each one with incremental features and functionality.

## Version 1

Version 1 is the simple core of the SMTP protocol: parsing commands sent via the client. Version 1 contains a rudimentary parser which expects RFC 821 compliant commands and parses them accordingly, using a state machine implementation.

## Version 2

Version 2 contains the implementation responsible for actually 'forwarding' emails sent to the server. This is essentially the physical mail equivalent of storing it in the mailbox, so that the recipient can come and retrieve the mail later. It is built on top of Version 1, which means that once Version 1 receives and parses the expected sequence of commands, the message will be stored ('forwarded') for future use.

## Version 3

Version 3 contains the code which would be running on a client-side system, receiving response codes issued from the server. It contains the logic required for users to input their messages and define their recipients to send the mail that will be parsed in Versions 1 and 2. This Version also allows the user to send multiple emails all at once, without requiring a program restart.

## Version 4

Version 4 is the final version which completes both the client and server side processes required to completely enact RFC 821. The client module runs as a CLI which takes input from the user to generate the correct RFC 821 codes to send to the mail server (as created in Version 3). Then the email is sent to the mail server which is running the server module which receives and parses the email. If there are any errors or unexpected commands, it returns errors as specified by the protocol, otherwise it forwards the email to the recipient and waits for more input.
