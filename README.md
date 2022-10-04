# Linspector System Monitoring

#### Linspector is not some program expecting computers to obviously run...

## About

The idea is based on a software I developed around 2010 or so. The name of the software was 
[Linspector](https://linspector.org/) but the implementation was just too
complicated. The idea still remains so here is the rebirth of Linspector. First commits 
of this rewrite where done as a new project named 
[monipy](https://git.unixpeople.org/linspector/monipy), but I moved to the name 
Linspector because I believe it is the better and cooler name... Old Linspector code is 
not available in this repository anymore, you can find it under 
[https://git.unixpeople.org/linspector/linspector-old](https://git.unixpeople.org/linspector/linspector-old).

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
sure the license is compatible but MIT should always be preferred if an
alternative is available.
- The core of Linspector should not use 3rd party libraries. Only plugins,
notifications and types may use other libraries. But coping code into the
source tree is ok when respecting the license. Not using 3rd party libraries
should always be preferred though. 
- Inline comments should be all lowercase. Descriptions and documentation comments
must be natural language.

### Required libraries

Currently, the Linspector core requires the following 3rd party libraries:

- [APScheduler](https://github.com/agronholm/apscheduler) - This is the scheduler in 
Linspector for execution of monitors. I started 
to use this library in very early versions of Linspector in 2011. Since the main task
in Linspector is the execution of jobs in regularly intervals I believe it is the right 
decision to make use of APScheduler directly in the core of the Linspector project.

### Other used libraries

monitors, notifications, services or plugins sometimes need to make the use of 
3rd party libraries, but they are not required to run Linspector properly. Not installing 
them may only affect parts of Linspector. Currently used libraries are:

- [CherryPy](https://cherrypy.dev/) - CherryPy is a pythonic, object-oriented HTTP framework. 
Used by the HTTPServer plugin.
- [requests](https://requests.readthedocs.io/en/latest/) - Requests is an elegant and simple 
HTTP library for Python, built for human beings. Used by the Speedtest service.

These libraries are not being delivered with the Linspector source code and maybe have 
different and incompatible licenses. You need to install them using pip, your OS package
manager or any other possible way.

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

 - No inline comments so every available character can be used in values
 - Values can be overridden in each monitor
 - File names in etc/* are not important but section names and key names.
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

Copyright (c) 2013 - 2022 Johannes Findeisen

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
