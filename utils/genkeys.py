#!/usr/bin/env python3

import sys, os
import base64
import secrets

def usage():
	print("genkeys.py <key_length> <out_file>")
	sys.exit()

if len(sys.argv) != 3:
	usage()

KEY_LENGTH = int(sys.argv[1])
OUT_PATH = sys.argv[2]

def genkey(length, out_file):
	out_dir = os.path.dirname(out_file)
	if not os.path.exists(out_dir) and out_dir:
		os.makedirs(out_dir)

	with open(out_file, "wb") as f:
		f.write(secrets.token_bytes(length))

genkey(KEY_LENGTH, OUT_PATH)
