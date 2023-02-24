# Linspector System Monitoring

#### Linspector is not some program expecting computers to obviously run...

## About

The idea is based on a software I developed around 2010 or so. The name of the software was
[Linspector](https://linspector.org/) but the implementation was just too
complicated. The idea still remains so here is the rebirth of Linspector. First commits
of this rewrite where done as a new project named
[monipy](https://github.com/linspector/monipy), but I moved to the name
Linspector because I believe it is the better and cooler name... Old Linspector code is
not available in this repository anymore, you can find it under
[https://github.com/linspector/linspector-old](https://github.com/linspector/linspector-old).

Hope this project will become useful for someone at some day and not only for
me. Just give me some amount of time for the first usable release... ;)

**Linspector** contains a daemon and some tools to monitor your infrastructure. It
collects data for statistics and sends alerts in case of errors. When extending Linspector
with plugins it for example can provide a web interface etc.

Since this project is at a very early stage of development it is not ready for usage.
I design the software actually and try to convert my ideas to software.

## Development

### Environment

My development environment is running using a virtual Python environment. I am using
all packages defined in requirements.txt.

Linspector includes a Makefile for executing bin/linspector without writing the full
command with pretended PYTHONPATH. This makes my work a little easier.

The IDE I am using is [IntelliJ IDEA Community Edition](https://www.jetbrains.com/idea/)
with Python plugin and / or  [PyCharm Community](https://www.jetbrains.com/pycharm/) from
[JetBrains](https://www.jetbrains.com/). I mention the IDE here because I am very thankful
to JetBrains for providing such a nice piece of software. I have never seen such a perfect
development environment.

### To do

- **Everything!** But the progress is fast and after some few days I am not far
away to get a first working codebase. If the core is running I believe adding features
will happen from day to day... ;)

See TODO for internal tasks.

### Ideas

- **Thousands!** For now the goal is to implement most features from the old version
of Linspector. :)

### Manifest

- All of this project **must be MIT licensed**. When using 3rd party libraries make
sure the license is compatible.
- The core of Linspector should not use 3rd party libraries if possible. Only notifications, 
plugins, services and tasks may use other libraries. Copying code into the
source tree is ok when respecting the license. Not using 3rd party libraries
should always be preferred though.
- Inline comments can all be lowercase. Descriptions and documentation comments
must be natural language.
- Arguments to functions must always be in alphabetical order.
- Class member variables must always be in alphabetical order in "\__init__()" or any
function / method.
- Functions must always be in alphabetical order in classes.
- Every commit must be working code without errors even if not being a working version of Linspector.

### Required libraries

Currently, the Linspector core requires the following 3rd party libraries:

- [APScheduler](https://pypi.org/project/APScheduler/) - APScheduler is a Python library that lets you 
schedule your Python code to be executed later, either just once or periodically. This is the heart of Linspector for
executing scheduled jobs in intervals.
- [fastAPI](https://pypi.org/project/fastapi/) - FastAPI is a modern, fast (high-performance), web framework for 
building APIs with Python 3.7+ based on standard Python type hints. It is used in the API plugin but this 
plugin really is core stuff.
- [Loguru](https://pypi.org/project/loguru/) - Loguru is a library which aims to bring enjoyable logging in Python. 
Linspector uses Loguru for all logging stuff. 
- [urwid](https://pypi.org/project/urwid/) - Urwid is a console user interface library for Python. urwid will 
become the UI library used for the management TUI of Linspector.

### Other used libraries

monitors, notifications, services or plugins sometimes need to make the use of
3rd party libraries, but they are not required to run Linspector properly. Not installing
them may only affect parts of Linspector. Currently used libraries are:

- [CherryPy](https://cherrypy.dev/) - CherryPy is a pythonic, object-oriented HTTP framework.
Used by the HTTPServer plugin.
- [fritzconnection](https://github.com/kbr/fritzconnection) - A Python-Tool to communicate with
the AVM Fritz!Box. Uses the TR-064 protocol over UPnP. Used by the FritzboxPhoneStatus and
FritzBoxUplink service.
- [Paramiko](https://www.paramiko.org/) - Paramiko is a pure-Python (2.7, 3.4+) implementation
of the SSHv2 protocol, providing both client and server functionality. Used by the SSH service.
- [python-gammu](https://wammu.eu/python-gammu/) - Python bindings for the Gammu library. Used by the
SMS notification.
- [PySNMP](https://pysnmp.readthedocs.io/en/latest/) - PySNMP is a cross-platform, pure-Python
SNMP engine implementation. It features fully-functional SNMP engine capable to act in
Agent/Manager/Proxy roles, talking SNMP v1/v2c/v3 protocol versions over IPv4/IPv6 and other
network transports. Used by the SNMP services (get).
- [requests](https://requests.readthedocs.io/en/latest/) - Requests is an elegant and simple
HTTP library for Python, built for human beings. Used by the Speedtest service.
- [xmpp2](https://pypi.org/project/xmpp2/) - A XMPP client for Python. Used by the XMPP notification.

These libraries are not being delivered with the Linspector source code and maybe have
different and incompatible licenses. You need to install them using pip, your OS package
manager or by just install everything in requirements.txt (recommended).

### Version numbering

To be compliant to Python packaging guidelines Linspector uses the following versioning
scheme (See: [https://semver.org/](https://semver.org/)):

#### MAJOR.MINOR.MAINTENANCE

- **MAJOR** changes _can_ change the API. The lesser, the better. It _expects_ a
  complete documentation.
- **MINOR** changes _must_ not break the API. New features are placed here.
- **MAINTENANCE** changes are "just-in-time" changes or small enhancements which _should_
  not affect the documentation and _must_ not break the API.

#### Examples:

- 1.2.0.dev1 - Development release
- 1.2.0a1 - Alpha Release
- 1.2.0b1 - Beta Release
- 1.2.0rc1 - Release Candidate
- 1.2.0 - Final Release
- 1.2.0.post1 - Post Release
- 15.10 - Date based release
- 23 - Serial release

(More information: [https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#choosing-a-versioning-scheme](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#choosing-a-versioning-scheme) &
[https://peps.python.org/pep-0440/#public-version-identifiers](https://peps.python.org/pep-0440/#public-version-identifiers))

### Configuration file rules

- All configuration options must be documented
- No unused options should be added to the default configuration
- No inline comments so every available character can be used in values
- Values can be overridden in each monitor
- File name case in etc/* is not important but section names and key names
- Comments can be inserted using ';' or '#'

## FAQ

### Is Linspector usable already?

No! Linspector is at a very early stage of development, but I believe it will become
stable until the end of 2022. The old version of Linspector was usable and I ran it for
monitoring a small amount of services for some years.

### Should I try the old version of Linspector?

I recommend not to use the old version of Linspector because the new version will
in no way become backward compatible. Features of the old version will nearly all be
implemented in the new version so if you can wait a little then I recommend to wait
until I release the new version of Linspector.

### Can I use an old configuration of Linspector in the new version?

No! The new configuration does not use JSON files anymore but an INI file syntax based on
a directory tree.

### Why should I use Linspecter even there are other mature and stable tools available already?

Linpector aims to be very small and simple and even should work in home or small
environments. But Linspector also is useful in very large infrastructures for monitoring
thousands of devices and services.

### Can I run multiple instances of the Linspector daemon?

Yes, of course. Since you add a configuration path when running Linspector you can
just pass a different path to a configuration tree to each instance. And since you
can configure the PID file in each configuration you can even can start, stop or
restart each instance in a native way.

## License

Linspector is open-source and completely free and will always be.

### MIT license

Copyright (c) 2013 - 2023 Johannes Findeisen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice (including the next
paragraph) shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
