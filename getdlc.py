#!/usr/bin/python3
# Created by yosh778

PKG2ZIP='./pkg2zip'

import os, sys
import subprocess
from urllib.request import urlopen

DBURL='https://docs.google.com/spreadsheets/d/18PTwQP7mlwZH1smpycHsxbEwpJnT8IwFP7YZWQT7ZSs/export?format=tsv&id=18PTwQP7mlwZH1smpycHsxbEwpJnT8IwFP7YZWQT7ZSs&gid=743196745'


if len(sys.argv) < 2:
	print('Usage : ' + sys.argv[0] + ' <GAMEID>')
	exit()

curID = sys.argv[1]


print( 'Parsing Database' )


allDLCs = {}

data = urlopen( DBURL ).read().decode('utf8')

for line in data.splitlines():

	items = line.split('\t')

	idGame = items[0]
	name   = items[2]
	pkgURL = items[3]
	zRIF   = items[4]
	idDLC  = items[5]

	DLCs = {}

	if idGame in allDLCs:
		DLCs = allDLCs[ idGame ]

	DLC = {}
	DLC['pkgURL'] = pkgURL
	DLC['zRIF']   = zRIF
	DLC['name']   = name

	DLCs[ idDLC ] = DLC
	allDLCs[ idGame ] = DLCs


print()
print( 'Fetching all DLCs for ' + curID )
print()


for idDLC, dlc in allDLCs[ curID ].items():

	zRIF = dlc[ 'zRIF' ]

	if zRIF == 'MISSING':
		continue

	print( 'Getting "' + dlc['name'] + '"' )

	print( 'Downloading DLC', end="\r" )
	subprocess.check_call( [ "wget", dlc[ 'pkgURL' ], "-O", "tmp.pkg", "-q" ] )

	print( 'Extracting DLC ', end="\r" )
	subprocess.check_call( [ PKG2ZIP, "-x", "tmp.pkg", zRIF ], stdout=open(os.devnull, 'wb') )
	os.unlink( "tmp.pkg" )


print( '               ' )
print( 'Finished' )

