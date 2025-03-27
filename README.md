# PySocketChat

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)

A minimalist Python socket implementation demonstrating real-time chat capabilities between multiple clients through terminal interfaces.

## Features
- **TCP Socket Communication** - Basic server-client architecture using Python's built-in socket library
- **Multi-Client Support** - Handle multiple concurrent connections
- **Educational Focus** - Clean code structure ideal for learning network fundamentals
- **Cross-Platform** - Works on any OS with Python 3.x

## Installation
```
git clone https://github.com/irhdab/pysocketchat.git
cd pysocketchat
```

No external dependencies required beyond Python standard libraries

## Usage
**Start Server:**
```
python server.py
# Default port: 5555 (modify in code if needed)
```

**Connect Clients:**
```
python client.py
# Enter IP: 127.0.0.1 in default
```

## Project Structure
```
pysocketchat/
├── server.py        # Socket server implementation
├── client.py        # Client connection handler
└── README.md        # Documentation
```

## Key Code Snippets
Server initialization:
```
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen()
```

Client message handling:
```
while True:
    message = input("You: ")
    client.send(message.encode('utf-8'))
```

## Dependencies

This project uses only Python's built-in libraries, such as `socket` and `threading`. No additional dependencies are required, as long as you have Python 3 installed.

## Contributing
1. Fork repository
2. Create feature branch (`git checkout -b enhance/feature`)
3. Test changes locally
4. Submit pull request