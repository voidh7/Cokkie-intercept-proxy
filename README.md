# Cokkie Intercept Proxy

Cokkie Intercept Proxy is a CLI tool that creates an HTTP proxy capable of intercepting traffic.

It supports both passive and active interception modes.

## Installation

1-Clone the repository:
```bash
git clone https://github.com/voidh7/Cokkie-intercept-proxy.git && cd Cokkie-intercept-proxy
```

2-Install the dependencies:
```bash
pip install -r requirements.txt
```
## Usage

### Passive interception

Captures HTTP packets and displays requests and responses without modification.
```bash
  python3 proxy.py
```
### Active interception

Allows modifying and forging HTTP packets and responses before forwarding them.
```bash
  python3 proxy.py --intercept
```
## Interception Modes

- Passive interception: only captures packets and displays responses.
- Active interception: allows modifying and forging packets and responses.
