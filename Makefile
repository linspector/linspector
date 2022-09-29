all:
	PYTHONPATH=$(shell pwd) ./bin/linspector -s ./etc

daemon:
	PYTHONPATH=$(shell pwd) ./bin/linspector -d ./etc
