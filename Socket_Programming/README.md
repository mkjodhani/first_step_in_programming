# Socket
Sockets allow communication between two different processes on the same or different machines. To be more precise, it's a way to talk to other computers using standard Unix file descriptors. In Unix, every I/O action is done by writing or reading a file descriptor. A file descriptor is just an integer associated with an open file and it can be a network connection, a text file, a terminal, or something else.

To a programmer, a socket looks and behaves much like a low-level file descriptor. This is because commands such as read() and write() work with sockets in the same way they do with files and pipes.

Sockets were first introduced in 2.1BSD and subsequently refined into their current form with 4.2BSD. The sockets feature is now available with most current UNIX system releases.
### Socket Types
  - Stream Sockets
  - Datagram Sockets 
  - Raw Sockets
  - Sequenced Packet Sockets
# Socket Concepts

When you create a socket, you must specify the style of communication you want to use and the type of protocol that should implement it. The communication style of a socket defines the user-level semantics of sending and receiving data on the socket. Choosing a communication style specifies the answers to questions such as these:

    What are the units of data transmission? Some communication styles regard the data as a sequence of bytes with no larger structure; others group the bytes into records (which are known in this context as packets).
    Can data be lost during normal operation? Some communication styles guarantee that all the data sent arrives in the order it was sent (barring system or network crashes); other styles occasionally lose data as a normal part of operation, and may sometimes deliver packets more than once or in the wrong order.

    Designing a program to use unreliable communication styles usually involves taking precautions to detect lost or misordered packets and to retransmit data as needed.
    Is communication entirely with one partner? Some communication styles are like a telephone call—you make a connection with one remote socket and then exchange data freely. Other styles are like mailing letters—you specify a destination address for each message you send. 

You must also choose a namespace for naming the socket. A socket name (“address”) is meaningful only in the context of a particular namespace. In fact, even the data type to use for a socket name may depend on the namespace. Namespaces are also called “domains”, but we avoid that word as it can be confused with other usage of the same term. Each namespace has a symbolic name that starts with ‘PF_’. A corresponding symbolic name starting with ‘AF_’ designates the address format for that namespace.

Finally you must choose the protocol to carry out the communication. The protocol determines what low-level mechanism is used to transmit and receive data. Each protocol is valid for a particular namespace and communication style; a namespace is sometimes called a protocol family because of this, which is why the namespace names start with ‘PF_’.

The rules of a protocol apply to the data passing between two programs, perhaps on different computers; most of these rules are handled by the operating system and you need not know about them. What you do need to know about protocols is this:

    In order to have communication between two sockets, they must specify the same protocol.
    Each protocol is meaningful with particular style/namespace combinations and cannot be used with inappropriate combinations. For example, the TCP protocol fits only the byte stream style of communication and the Internet namespace.
    For each combination of style and namespace there is a default protocol, which you can request by specifying 0 as the protocol number. And that’s what you should normally do—use the default. 
