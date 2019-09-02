# F5Cookie

F5 BIG-IP load balancers can be configured to encode the IP address of the actual web server that it is acting on behalf of within a cookie. This script can be used to quickly check if a host provides the client with such a cookie and will decode it to disclose the internal host and port the client is communicating with.

This script also can ingest a cookie as a string and return the decoded IP and port or encode a given IP address into cookie format.


## Usage Examples
```
./F5cookie.py -u https://example.com
IP:     10.73.128.30
PORT:   16024

./F5cookie.py -u https://X.X.X.X --no-ssl
IP:     10.73.128.30
PORT:   16024

./F5cookie.py -c 511723786.38974.0000
IP:     10.73.128.30
PORT:   16024

./F5cookie.py -ip 10.73.128.30
511723786
```
