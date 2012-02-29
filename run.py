#!/usr/bin/env python

from dabot import start
from twisted.python import log
import sys

if __name__ == "__main__":
	log.startLogging(sys.stdout)
	start("etc/default.yaml")
