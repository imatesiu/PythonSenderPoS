#!/usr/bin/python

from escpos.printer import *

p = Network("leggionella.ddns.net")

p.text("ciao")

p.block_text("ciao1",font="a" ,columns=None)

p.cut()
