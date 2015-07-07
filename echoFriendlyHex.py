#!/usr/bin/python
import sys
import os
import signal
import argparse
import binascii

argParser = argparse.ArgumentParser(
  prog='echoFriendlyHex.py',
  description='dump generally usable hex from binary and vice-versa'
)

argParser.add_argument(
  '-f',
  '--file',
  help='filename (otherwise read data from stdin)',
  default=False
)

argParser.add_argument(
  '-r',
  '--reverse',
  help='reverse a previously dumped hex',
  action='store_true'
)

args = argParser.parse_args()
inputFile = args.file
reverse = args.reverse

def binToEchoFriendlyHex(binData):
  hexData = binascii.hexlify(binData)
  for i in range(0, len(hexData)):
    if not i % 2:
      sys.stdout.write('\\x')
    sys.stdout.write(hexData[i])

def echoFriendlyHexToBin(hexData):
  try:
    binData = binascii.unhexlify(hexData.replace('\\x', '').strip())
  except:
    sys.exit('Invalid hex data');
  sys.stdout.write(binData)

def readData(inputFile=False):
  if inputFile:
    if not os.path.isfile(inputFile):
      sys.exit(inputFile, 'does not exist')
    
    with open(inputFile, 'rb') as f:
      data = f.read()
  else:
    data = sys.stdin.read()
  
  return data

def killHandler(signal, frame):
  print '\n'
  sys.exit()

def run(inputFile, reverse):
  data = readData(inputFile)
  if reverse:
    echoFriendlyHexToBin(data)
    return
  
  binToEchoFriendlyHex(data)

signal.signal(signal.SIGINT, killHandler)
run(inputFile, reverse)
