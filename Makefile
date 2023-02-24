PYTHON_VERSION=3.10
#PYTHON_VERSION = $(shell python -V | awk -F ' ' '{print $2}' | awk -F '.' '{print $1 "." $2}')

help:
	# Getting started using this Makefile. 
	# It should help you to go on fast and easy.
	#
	# First edit this Makefile and add your Python version:
	# -----------------------------------------------------
	#  Set PYTHON_VERSION to MAJOR.MINOR version of your 
	#  current installed Python version. E.g.: 3.10 (default).
	#  Get the Python version with: python -V
	#
	# Create virtual environment:
	# ---------------------------
	#  python -m venv ./venv
	#  source ./venv/bin/activate
	#  pip install -r requirements.txt
	#
	# Activate virtual environment when not already done:
	# ---------------------------------------------------
	#  source ./venv/bin/activate
	#
	# Deactivate virtual environment:
	# -------------------------------
	#  deactivate
	#
	# Run Linspector:
	# ---------------
	#  make run
	#
	# Run Linspector in daemon mode:
	# ------------------------------
	#  make daemon

daemon:
	PYTHONPATH=$(shell pwd):$(shell pwd)/venv/lib/python$(PYTHON_VRESION)/site-packages/ bin/linspector -d ./etc

follow:
	tail -F ./log/linspector.log

run:
	PYTHONPATH=$(shell pwd):$(shell pwd)/venv/lib/python$(PYTHON_VERSION)/site-packages/ bin/linspector ./etc

rundev:
	PYTHONPATH=$(shell pwd):$(shell pwd)/venv/lib/python$(PYTHON_VERSION)/site-packages/ bin/linspector ./etc.test.local
