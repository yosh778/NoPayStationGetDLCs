#!/usr/bin/python3
# Created by yosh778

PKG2ZIP='./pkg2zip'

import os, sys
import subprocess
from urllib.request import urlopen

DBURL='https://docs.google.com/spreadsheets/d/18PTwQP7mlwZH1smpycHsxbEwpJnT8IwFP7YZWQT7ZSs/export?format=tsv&id=18PTwQP7mlwZH1smpycHsxbEwpJnT8IwFP7YZWQT7ZSs&gid='
GAMES='1180017671'
DLCS='743196745'


if len(sys.argv) < 2:
	print('Usage : ' + sys.argv[0] + ' <GAMEID> or ' + sys.argv[0] + ' -l for the game list')
	exit()

curID = sys.argv[1]

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


print( 'Parsing Database' )


allDLCs = {}
titles = None

data = urlopen( DBURL + DLCS ).read().decode('utf8')

for line in data.splitlines():

	items = line.split('\t')

	if titles is None:
		titles = items
		continue

	idGame = items[0]
	region = items[1]
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
	DLC['region']   = region

	DLCs[ idDLC ] = DLC
	allDLCs[ idGame ] = DLCs

def nameSort(item):
	item = allDLCs[item]
	elem = next(iter( item.values() ))
	return elem['name']

if curID.strip() == '-l':

	for game in sorted(allDLCs, key=nameSort):

		dlcs = allDLCs[game]
		dlc = next(iter( dlcs.values() ))

		print( game + ' ' + dlc['region'][:2] + ' ' + dlc['name'] )

	exit()


print()
print( 'Fetching all DLCs for ' + curID )
print()

if not curID in allDLCs:
	print( 'No result' )
	exit()

for idDLC, dlc in allDLCs[ curID ].items():

	zRIF = dlc[ 'zRIF' ]
	pkgURL = dlc[ 'pkgURL' ]

	if zRIF == 'MISSING' or pkgURL == 'MISSING':
		continue

	print( 'Getting "' + dlc['name'] + '"' )

	print( 'Downloading DLC', end="\r" )
	subprocess.check_call( [ "wget", pkgURL, "-O", "tmp.pkg", '-q' ] )

	print( 'Extracting DLC ', end="\r" )
	subprocess.check_call( [ get_script_path() + '/' + PKG2ZIP, "-x", "tmp.pkg", zRIF ], stdout=open(os.devnull, 'wb') )
	os.unlink( "tmp.pkg" )


print( '               ' )
print( 'Finished' )

