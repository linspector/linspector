# Linspector Infrastructure and System Monitoring

#### Linspector is not some program expecting computers to obviously run...

## About

The idea is based on a software I developed around 2010 or so. The name of the software was 
[Linspector](http://linspector.org/) but the implementation was just too
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
- The core of Linspector should not use 3rd party libraries. only plugins,
notifications and types may use other libraries. But coping code into the
source tree is ok when respecting the license. Not using 3rd party libraries
should always be preferred though. If adding 3rd party libraries to the Linspector 
core all code **must** be included in the Linspector source tree. Not as Git
submodule but as files imported into the Linspector Git repository!
- Inline comment should be all lowercase. Descriptions and documentation comments
must be natural language.

### Included libraries

Currently, the Linspector source tree contains the following 3rd party libraries:

- [APScheduler](https://github.com/agronholm/apscheduler) (3.9.1) - This is the scheduler in Linspector for execution of monitors. I started 
to use this library in very early versions of Linspector in 2011. Since the main task
in Linspector is the execution of jobs in regularly intervals I believe it is the right 
decision to include the code of APScheduler directly into the Linspector project.

### Other used libraries

monitors, notifications, services or plugins sometimes need to make the use of 
3rd party libraries, but they are not required to run Linspector properly. Not installing 
them may only affect parts of Linspector. Currently used libraries are:

- [CherryPy](https://cherrypy.dev/) - CherryPy is a pythonic, object-oriented HTTP framework. Used by the HTTPServer plugin.
- [requests](https://requests.readthedocs.io/en/latest/) - Requests is an elegant and simple HTTP library for Python, built for human beings. Used by the Speedtest service.

These libraries are not being delivered with the Linspector source code and maybe have 
different and incompatible licenses. You need to install them using pip, your OS package
manager or any other possible way.

### Version numbering

According to: [https://wiki.unixpeople.org/linux_kernel_version_numbering](https://wiki.unixpeople.org/linux_kernel_version_numbering)

**MAJOR**.**FEATURE**.**MINOR**.**FIXES**

- **MAJOR** changes _can_ change the API. The lesser, the better.
- **FEATURE** changes can, but _should_ not break the API. New features are placed
  here. It _expects_ a complete documentation.
- **MINOR** changes are "just-in-time" changes or small enhancements which _should_
  not affect the documentation and _must_ not break the API.
- **FIXES** _must_ never affect anything else then stability or security.

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

### MIT license

Copyright (c) 2010 - 2022 Johannes Findeisen &lt;you@hanez.org&gt;

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
