#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This script converts the ing <www.ing.nl> csv files into more generic csv files which can be imported by FireflyIII <https://github.com/JC5/firefly-iii>
# Copyright (C) 2016 Bonno Nachtegaal-Karels
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; If not, see <http://www.gnu.org/licenses/>.

import re
import csv
import argparse
import datetime
import os

SavingIBAN = 'NL12RBOS0606327219' # random generated IBAN

def CategoryTransaction(desc):
	if (re.search(r"(Autocentr|MCS)", desc, re.I)):
		return ["Auto:Onderhoud", "Auto"]
	if (re.search(r"(TAMOIL|SHELL|TINQ|TANGO|BP|Esso)", desc, re.I)):
		return ["Auto:Benzine", "Auto"]
	if (re.search(r"(KINDERBIJSLAG|SALARIS)", desc, re.I)):
		return ["Inkomen", "Inkomen"]
	if (re.search(r"(KINDEX|Norlandia)", desc, re.I)):
		return ["Kinderen:Kinderopvang", "Kinderen"]
	if (re.search(r"(jumbo|kruidvat|ALBERT HEIJN|AH to go|Gall & Gall|Sligro|Etos|Primera|PLUS |C1000|EMTE|LIDL|ALDI|SPAR|V.O.F. J. en S. Smit|Kaaskoerier|Kaashand|Hoogvliet|DIRK VDBROEK|Verhoog|HWBiofoods)", desc, re.I)):
		return ["Boodschappen", "Boodschappen"]
	if (re.search(r"(belastingdienst|Belastingsamenwerking)", desc, re.I)):
		return ["Belastingen","Belastingen"]
	if (re.search(r"(Simyo)", desc, re.I)):
		return ["Telefoon","GWE"]
	if (re.search(r"(DUNEA DUIN WATER|Energie)", desc, re.I)):
		return ["Energie/Water","GWE"]
	if (re.search(r"(Ziggo)", desc, re.I)):
		return ["Televisie","GWE"]
	if (re.search(r"(SCHADEVERZEKERIN|INSHARED|FBTO|ZORGVERZEKERINGEN|Delta Lloyd|NATIONALE NEDERLANDEN|Allianz|ZORGVERZEKER|TAF|ASSURANTIE|Polis)", desc, re.I)):
		return ["Verzekeringen","Verzekeringen"]
	if (re.search(r"(Hypotheek|Hypotrust)", desc, re.I)):
		return ["Huis:Hypotheek", "Hypotheek"]
	if (re.search(r"(Gamma|Praxis|Karwei|Warmteservice|HEYMANS)", desc, re.I)):
		return ["Huis:Verbouwing","Huis"]
	if (re.search(r"(H-Cleaning)", desc, re.I)):
		return ["Huis:Schoonmaak","Huis"]
	if (re.search(r"(Ikea|Eigen Huis)", desc, re.I)):
		return ["Huis:Overig","Huis"]
	if (re.search(r"(INTRATUIN|Bosrand)", desc, re.I)):
		return ["Huis:Tuin","Huis"]
	if (re.search(r"(GEA)", desc, re.I)):
		return ["Contanten","Contanten"]
	if (re.search(r"(Esprit|Hunkemoller|ECCO|MS MODE|Bon ?Prix|Etam|Chique Dress|Schoenenreus|HarenSchoenen|VAN DAL (B.V.|Mannenmode)|C\&A |ZEEMAN|Wibra|Bijou Brigitte|Primark)", desc, re.I)):
		return ["Kleding","Kleding"]
	if (re.search(r"([0-9]{4} Action|Hema|BLOKKER|Xenos|Boerenbond|Douglas|Rituals|Trekpleister|V\&D )", desc, re.I)):
		return ["Diversen:Overig","Diversen"]
	if (re.search(r"(Intertoys|Bart Smit)", desc, re.I)):
		return ["Diversen:Speelgoed","Diversen"]
	if (re.search(r"(Silver Ocean|scheerenfoppen|4Launch|MMS Online|MediaMarkt|DIXONS)", desc, re.I)):
		return ["Diversen:Computers","Diversen"]
	if (re.search(r"(E Friends|DOMINO.?S|La Place|Mc Donald|Cafetaria|Copper Food|Smullers|PIZZA EXPRESS|Badmeester WASSENAAR|Boerderij Meijendel|IJskiosk Was-slag)", desc, re.I)):
		return ["Uitjes:Uiteten","Uitjes"]
	if (re.search(r"(Creditcard|PayPal)", desc, re.I)):
		return "Creditcard"		
	if (re.search(r"(edutel|kpn|XS4ALL|Transip B.V.)", desc, re.I)):
		return ["Internet", "GWE"]
	if (re.search(r"(Apotheken)", desc, re.I)):
		return "Zorg:Apotheek"
	if (re.search(r"(Famed)", desc, re.I)):
		return "Zorg:Tandarts"
	if (re.search(r"(Pathe|bios)", desc, re.I)):
		return ["Uitjes:Bioscoop","Uitjes"]
	if (re.search(r"(xxx|yyy)", desc, re.I)):
		return ["Uitjes:Diverse","Uitjes"]
	if (re.search(r"(center ?par[ck])", desc, re.I)):
		return "Vakantie:CenterParcs"
	return ""

def OpposingName(name):
	while name.strip().find("  ") > 0:
		name = name.strip().replace("  ", " ")
	if (re.search(r"Toprekening", name, re.I)):
		return 'ING Gezamelijk Spaarrekening'
	return name
		

""" First parse the command line arguments. """
parser = argparse.ArgumentParser(prog = 'ing2generic', description= """
                                 This program converts ING (www.ing.nl) CSV files to generic csv files. The default output filename is the input filename.
                                 """)
parser.add_argument('csvfile', help='A csvfile to process')
parser.add_argument('-o, --outfile', dest = 'outfile', 
   help = 'outfile filename', default=None)
parser.add_argument('-d, --directory', dest = 'dir', 
   help = 'Directory to store outfile, default is ./converted', default='converted')
parser.add_argument('-c, --convert', dest = 'convert', 
   help = "Convert decimal separator to dots (.), default is false", action='store_true')
args = parser.parse_args()

#create path to ofxfile
if args.outfile:
	filename = args.outfile
else:
	filename = args.csvfile

#if directory does not exists, create it.
if not os.path.exists(os.path.join(os.getcwd(), args.dir)):
	os.makedirs(os.path.join(os.getcwd(), args.dir))

filepath = os.path.join(os.getcwd(), args.dir, filename)

outfile = open(filepath,'w')
outfile.write('"date-transaction", "account-iban", "description", "budget-name", "category-name", "amount", "opposing-iban","opposing-name"\n')

with open(args.csvfile, 'rb') as csvfile:
	 #Open the csvfile as a Dictreader
	 csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
	 for row in csvreader:
		#Map ACCOUNT to "Rekening"
		Account = row['Rekening'].replace(" ", "")
		
		Name = OpposingName(row['Naam / Omschrijving'])
		
		OpposingIban =  row['Tegenrekening']
		#Description maps to "Mededelingen", the while loop removes any double spaces.
		while row['Mededelingen'].strip().find("  ") > 0:
		   row['Mededelingen'] = row['Mededelingen'].strip().replace("  ", " ")
		#Replace & symbol with &amp to make xml compliant
		desc = str(row['Mededelingen'])
		Category = CategoryTransaction(desc + ' ' + Name)
		omschrijvingIndex = desc.find('Omschrijving: ')
		if omschrijvingIndex > 0:
			omschrijvingIndex += 14
			Description = desc[omschrijvingIndex:len(desc)]
		else:
			Description = desc
		
		if row['Naam / Omschrijving'].find('Toprekening') != -1:
			Description = row['Naam / Omschrijving']
			OpposingIban = SavingIBAN
		
		ParsedDesc = {}
		if (Category != None):
			ParsedDesc["CATEGORY"] = Category
			ParsedDesc["BUDGET"] = ""
			if isinstance(ParsedDesc["CATEGORY"],list):
				ParsedDesc["BUDGET"] = ParsedDesc["CATEGORY"][1]
				ParsedDesc["CATEGORY"] =  ParsedDesc["CATEGORY"][0]
		
			if args.convert:
				row['Bedrag (EUR)'] = row['Bedrag (EUR)'].replace(",", ".")
			if row['Af Bij'] == 'Bij':
				Amount = row['Bedrag (EUR)']
			else:
				Amount = "-"+row['Bedrag (EUR)']
			   
			outfile.write("\"" + row['Datum'] + "\",\"" + Account + "\",\"" + Description + "\",\"" + ParsedDesc["BUDGET"] + "\",\"" + ParsedDesc["CATEGORY"] + "\",\"" + Amount  + "\",\"" + OpposingIban + "\",\"" + Name + "\"\n")
#f.close()
outfile.close()

# input("Press Enter to continue...")


