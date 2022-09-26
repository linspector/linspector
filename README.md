# Linspector Infrastructure and System Monitoring

#### Linspector is not some program expecting computers to obviously run...

The idea is based on a software I developed around 2010 or so. The name of the software is 
[Linspector](http://linspector.org/) but the implementation was just too
complicated. The idea still remains so here is the rebirth of Linspector. First commits 
of this rewrite where done as a new project named 
[monipy](https://git.unixpeople.org/linspector/monipy), but I moved to the name 
Linspector because I believe it is the better and cooler name... Old Linspector code is 
not available in this repository anymore, you can find it under 
[https://git.unixpeople.org/linspector/linspector-old]().

Hope this project will become useful for someone at some day and not only for
me. Just give me some amount of time for the first usable release... ;)

## About

**Linspector** contains a daemon and some tools to monitor your infrastructure. It
collects data for statistics and sends alerts in case of errors. When extending Linspector
with plugins it for example can provide a web interface etc.

This project is at a very early stage of development it is not able for usage.
I design the software actually and try to convert my ideas to software. Code
nearly does not exist.

## Development

### To do

**Everything!** :) Just outlining the idea and creating code and structure skeletons
at the moment!

### Ideas

- Think about adding [APScheduler](https://pypi.org/project/APScheduler/) for 
scheduling execution of the monitors instead of a self constructed thread
structure... It was very nice to get the jobs done in Linspector using APScheduler 
in the past.

### Manifest

- All of this project **must be MIT licensed**. When using 3rd party libraries make
sure the license is compatible but MIT should always be preferred if an
alternative is available.
- The core of Linspector should not use 3rd party libraries. only plugins,
notifications and types may use other libraries. But coping code into the
source tree is ok when respecting the license. Not using 3rd party libraries
should always be preferred though.
- Inline comment should be all lowercase. Descriptions and documentation comments
must be natural language.

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

## License

### MIT License

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
