from __future__ import division		#Python 3 has nice things...
import sys
import string
import random
import time
import re

#Used as a weighting list to attempt to form 50% to 66% G/C content
NUCLEOTIDES = [("C", 33), ("G", 33), ("A", 25), ("T", 25)]
ENZYMES = {'HhaI':'GCGC', 'HindIII':'AAGCTT', 'NotI':'GCGGCCGC', 'EcoRI':'GATTC', 'FokI':'GGATG', 'FokIReverse':'CATCC', 'AlwI':'GGATC', 'AlwIReverse':'GATCC'}

#Function to ensure that the G/C content of the DNA will be between 50% and 66%
def GCchecker(dna):
	time.sleep(0.5)
	nucleotideCount = {'A':0, 'T':0, 'G':0, 'C':0}
	for nucleotide in dna: nucleotideCount[nucleotide] += 1
	GCcontent = (nucleotideCount['G'] + nucleotideCount['C'])/len(dna)
	if (GCcontent >= 0.50 and GCcontent <= 0.66): return dna
	else:
		#Recursively cycles through to generate more sequences
		print "50%-66% GC content not detected... Regenerating"
		return GCchecker(DNASequenceGenerator(len(dna)))

def enzymeChecker(dna):
	time.sleep(0.5)
	for enzyme in ENZYMES:
		if ENZYMES[enzyme] not in dna: return dna
		else:
			print "Matched Library Enzyme \"{0}\"... Regenerating".format(enzyme)
			return enzymeChecker(GCchecker(DNASequenceGenerator(len(dna))))

def DNASequenceGenerator(length): 
	return ''.join(random.choice("".join(nucleotide * weighting for nucleotide, weighting in NUCLEOTIDES)) for _ in range(length))

def userSequence(length):
	print "Working..."
	return enzymeChecker(GCchecker(DNASequenceGenerator(length)))

def addUserEnzyme(userEnzyme):
	if userEnzyme not in ENZYMES.values(): ENZYMES['UserEnzyme'] = userEnzyme

def enzymeCheck(userEnzyme):
	if re.search(r'\b[ATGC]+\b', userEnzyme): return True
	else: return False

if __name__ == '__main__':
	print "Hello and Welcome to IRENAEUS Assignment 3"
	print "The objective of this program is to generate a random DNA sequence for you"
	print "that will not contain any restriction enzyme sites (from our specified library)"
	print "as well as any enzyme sites that you may want to specify"
	print "==============================================================================="
	print ""
	while True:
		#Ensures that user will always enter an integer
		try:
			userLength = int(raw_input("How long do you wish the DNA sequence to be? "))
			break
		except ValueError:
			print "Please enter an INTEGER e.g. 10"
			print ""
	while True:
		print "If you would like to enter your own target site that your restriction enzyme will taget"
		userEnzyme = raw_input("Please do so here (e.g. ACCGGT) or leave blank: ")
		if enzymeCheck(userEnzyme.upper()):
			addUserEnzyme(userEnzyme.upper())
			break
	dna = userSequence(userLength)
	print ""
	print "DNA Sequence has been generated for you:"
	print dna
	print "==============================================================================="