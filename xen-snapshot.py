import subprocess as s
import argparse as a
import sys
import os.path

parser = a.ArgumentParser(description='This will parse a Xen config and dd the LV to a directory of your choosing.')

parser.add_argument('path',metavar='config path', help='path to the domU config file')
parser.add_argument('destpath',metavar='destination path',help='destination for the images')

args = parser.parse_args()

path = args.path
destpath = args.destpath

print "Verifying that the config file exists..."

paths = []
pathsVerified = []

if os.path.isfile(path):
	for line in open(path,'r'):
		if line.find("phy:") > -1:
			line = line.strip()
			line = line.replace("'phy:","")
			line = line.split(",")[0]
			paths.append(line)
			print "Found one path at %s" % line
	for path in paths:
		if os.path.isfile(path):
			pathsVerified.append(path)
			print "Found disk image at %s" % path
		else:
			print "Previously found path at %s looks like its invalid, dropping." % path
	if len(pathsVerified) == 0:
		print "There were no valid paths, can't proceed"
	else:
		for verified in pathsVerified:
			try:
				string = "dd if=%s of=%s%s" % (verified, destpath, verified)
				s.check_output(string,shell=True)
			except Exception,e:
				print "Looks like something broke: %s" % e
else:
	print "The config at %s doesn't appear to be valid, exiting." % path 
