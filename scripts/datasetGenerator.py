#!/usr/bin/python

# Takes a set of pcap files as input and outputs a csv w/ metadata as data features

import csv, sys, json, os

acName = str(sys.argv[1])
dataDir = str(sys.argv[2])
n = int(sys.argv[3])

#this defines the common nomenclature found for each ac round (ac-n.EXT)
#fullPath = dataDir+'/'+acName+'-'+str(i+1)

def extractFeaturesJSON(joyFile):
	#Load in JSON file
	jsn = json.load(open(joyFile))

	#Data extraction
	denom = float(jsn['num_pkts_in']) + int(jsn['num_pkts_out'])

	pin = jsn['num_pkts_in'] / denom #Percent of packets in
	pin = round(pin, 6)

	pot = jsn['num_pkts_out'] / denom #Percent of packets out
	pot = round(pot, 6)

	etp = jsn['entropy'] #Entropy

	return etp, pin, pot

def extractFeaturesCAPINFO(infoFile):
	#Load in capinfos file
	capinfo = open(infoFile, 'r')

	#Data extraction
	for i in range(5): capinfo.readline()

	npk = float((capinfo.readline().split(" ")[5]).replace(',','')) #Number of packets

	for i in range(7): capinfo.readline()

	aps = float(capinfo.readline().split(" ")[3]) #Average packet size

	apf = float(capinfo.readline().split(" ")[3]) #Average packet frequency

	return aps, apf, npk

def createJSONandCAPINFO(acName):
	print '>> Begin traffic parsing'
	for i in range(n):
		fullPath = dataDir+acName+'-'+str(i+1)
		os.system('/home/labuser/Mininet/class-testing/apps/joy/bin/joy bidir=1 retrans=1 entropy=1 classify=1 ppi=0 output='+fullPath+'.gz '+fullPath+'.pcap')
		os.system('/home/labuser/Mininet/class-testing/apps/joy/sleuth '+fullPath+'.gz > '+fullPath+'.json')
		os.system('rm '+fullPath+'.gz')
		os.system('capinfos '+fullPath+'.pcap > '+fullPath+'.capinfo')

	print '>> Traffic parsing complete'

def createCSV(acName, dataDir):
	featureTitles = "aps,apf,npk,etp,pin,pot,acn\n"
	csv = open('./dataset-' + acName + str(n) + 'Trials' + '.csv', 'w')
	csv.write(featureTitles)
	for i in range(n):
		fullPath = dataDir+acName+'-'+str(i+1)
		print 'Currently on ' + fullPath
		aps, apf, npk = extractFeaturesCAPINFO(fullPath + ".capinfo")
		etp, pin, pot = extractFeaturesJSON(fullPath + ".json")
		line = str(aps)+','+str(apf)+','+str(npk)+','+str(etp)+','+str(pin)+','+str(pot)+','+str(acName)+'\n'
		print line
		csv.write(line)

createJSONandCAPINFO(acName)
createCSV(acName, dataDir)

#FUTURE IMPROVEMENT
# Make createCSV() and createJSONandCAPINFO() only perform actions on 1 file
# and implement for loop in a main() function
