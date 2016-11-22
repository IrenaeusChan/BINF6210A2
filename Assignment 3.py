from __future__ import division		#Python 3 has nice things...
import sys
import string
import random
import time
import re

#Used as a weighting list to attempt to form 50% to 66% G/C content
NUCLEOTIDES = [("C", 33), ("G", 33), ("A", 25), ("T", 25)]
#A dictionary of our enzyme library
ENZYMES = {'HhaI':'GCGC', 'HindIII':'AAGCTT', 'NotI':'GCGGCCGC', 'EcoRI':'GATTC', 'FokI':'GGATG', 'FokIReverse':'CATCC', 'AlwI':'GGATC', 'AlwIReverse':'GATCC'}

#Function to ensure that the G/C content of the DNA will be between 50% and 66%
def GCchecker(dna):
	time.sleep(0.5)
	nucleotideCount = {'A':0, 'T':0, 'G':0, 'C':0}
	#For every nucleotide in our DNA sequence, record a count
	for nucleotide in dna: nucleotideCount[nucleotide] += 1
	GCcontent = (nucleotideCount['G'] + nucleotideCount['C'])/len(dna)	#GC content
	if (GCcontent >= 0.50 and GCcontent <= 0.66): return dna 	#If within our range, it's good
	else:
		#Recursively cycles through to generate more sequences if it's not within our range
		print "50%-66% GC content not detected... Regenerating"
		return GCchecker(DNASequenceGenerator(len(dna)))

def enzymeChecker(dna, enzymeChoice):
	time.sleep(0.5)
	if enzymeChoice not in dna: return dna
	else:
		print "Matched your selected enzyme: \"{0}\"... Regenerating".format(enzymeChoice)
		return enzymeChecker(GCchecker(DNASequenceGenerator(len(dna))), enzymeChoice)

#Function to generate our random DNA by joining ATGC together based on their weighting and user length
def DNASequenceGenerator(length): 
	return ''.join(random.choice("".join(nucleotide * weighting for nucleotide, weighting in NUCLEOTIDES)) for _ in range(length))

def userSequence(length, enzymeChoice):
	print "Working..."
	return enzymeChecker(GCchecker(DNASequenceGenerator(length)), enzymeChoice)

#Used to check if the enzyme the user enters is a valid enzyme using ATGC
def enzymeValidator(userEnzyme):
	if re.search(r'\b[ATGC]+\b', userEnzyme): return True
	else: return False

def listOfEnzyme():
	print "\nHere is our list of precompiled restriction enzymes you can choose from."
	print "Or leave this part blank if you don't want to use any of our restrction enzymes"
	#Prints the libary of enzymes for the user
	for num, enzymes in enumerate(ENZYMES.keys()): print str(num+1) + ". " + enzymes
	enzymeChoice = raw_input("Which enzyme would you like to use? ")
	#Make sure that the user has selected an enzyme (Case Insensitive) that exists in our library
	if enzymeChoice.lower() in list(k.lower() for k in ENZYMES.keys()): 
		#Generate a temporary dictionary with case insensitive key values of the ENZYME dictionary
		# and look for the value that corresponds to the users selection of enzyme
		return dict((key.lower(), value) for key, value in ENZYMES.iteritems())[enzymeChoice.lower()]
	#The user might also see the list of enzymes and choose a number, so we want to make sure we can
	# read in their number and return to them the corresponding enzyme for that number
	elif enzymeChoice in list(str(n+1) for n in range(6)): return ENZYMES.values()[int(enzymeChoice)-1]
	#If the user enters blank, then we assume they don't want to use our enzyme library
	elif enzymeChoice is "": return enzymeChoice
	#If the user hasn't selected a viable enzyme from our libary, then prompt them again
	else: listOfEnzyme()

def userRestrictionEnzyme():
	print "\nIf you would like to enter your own target site that your restriction enzyme will target"
	userEnzyme = raw_input("Please do so here (e.g. ACCGGT) or leave blank: ")
	while True:
		#Check to see if the user enzyme is actually a correct sequence
		if enzymeValidator(userEnzyme.upper()) and len(userEnzyme) > 0: return userEnzyme
		#If they enter blank, they don't want to use a restriction enzyme
		elif userEnzyme == "": return userEnzyme
		else: userEnzyme = raw_input("Your restriction enzyme is not valid, please enter it again: ")
		
if __name__ == '__main__':
	print "Hello and Welcome to IRENAEUS Assignment 3"
	print "The objective of this program is to generate random DNA sequences for you"
	print "that will not contain any restriction enzyme sites (from our specified library)"
	print "as well as any enzyme sites that you may want to specify"
	print "===============================================================================\n"
	while True: #Ensures that user will always enter an integer
		try:
			userLength = int(raw_input("How long do you wish the DNA sequence to be? "))			
			break
		except ValueError: print "Please enter an INTEGER e.g. 10\n"
	while True: #Same...
		try:
			userAmount = int(raw_input("How many sequences do you wish to generate? "))
			break
		except ValueError: print "Please enter an INTEGER e.g. 10\n"
	print "\nThanks..."
	time.sleep(0.5)
	#Prompt user for which restriction enzyme they would like to account for
	enzymeChoice = listOfEnzyme()
	#If they don't want to use our enzyme lbiraries then they can use their own
	if enzymeChoice == "": enzymeChoice = userRestrictionEnzyme()
	if enzymeChoice == "": enzymeChoice = "nothing"
	print "We will be checking for " + enzymeChoice + " in the DNA sequence."
	for i in range(userAmount):
		print ""
		dna = userSequence(userLength, enzymeChoice)
		print "\nDNA Sequence has been generated for you:"
		print str(i+1) + ". " + dna
	print "==============================================================================="