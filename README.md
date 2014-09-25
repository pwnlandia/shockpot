# ShockPot

Shockpot is a web app honeypot designed to find attackers attempting to exploit the
Bash remote code vulnerability, CVE-2014-6271.

## Installation

```
virtualenv env
. env/bin/activate
pip install -r requirements.txt 
```

## Configuration

Edit shockpot.conf

```
[server]
host = 0.0.0.0
port = 8080

[headers]
server = Apache/2.0.55 (Debian) PHP/5.1.2-1+b1 mod_ssl/2.0.55 OpenSSL/0.9.8b

[hpfeeds]
enabled = True
host = your.mhn.server.com
port = 10000
identity = shockpot
secret = secret
channel = shockpot.events
```

## Running

```
python shockpot.py
```

## LICENSE

Modern Honeypot Network

Copyright (C) 2014 - ThreatStream

This program free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation; either version 2.1 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
