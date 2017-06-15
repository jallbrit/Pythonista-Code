from console import clear, set_color, set_font
import linguistictagger as lt
import random, speech, time, sys, csv

#------------assignment-------------

#if tester is true, it prints all phrases and reactions.
tester = False

#if skip_intro is true, it (obviously) skips the intro.
skip_intro = False

#if talk is true, it speaks the words
talk = True

#these variables determine the way the computer will spit out the response: the dialect of the voice, and the font and font size the characters are printed as.
dialect = 'en-GB'
font = 'Futura'
set_color(0,0,0)
font_size = 20

phrase_list = []
reaction_list = []
stop_phrases = ["stop","quit","exit","leave"]

noun = []
verb = []
adjective = []
adverb = []
prounoun = []
determiner = []
particle = []
preposition = []
interjection = []
conjunction = []
punctuation = []
number = []
dash = []
sentenceterminator = []
otherword = []
whitespace = []

phrase_file_content = csv.reader(open("phrase_file.csv"))
reaction_file_content = csv.reader(open("reaction_file.csv"))

#-------------functions--------------

for row in phrase_file_content:
	phrase_list.append(row)
	
for row in reaction_file_content:
	reaction_list.append(row)

def search_pos(pos,search_list):
	result_list = []
	for item in search_list:
		tag = lt.tag_string(item,lt.SCHEME_LEXICAL_CLASS)
		for x in range(0,len(tag)):
			if tag[x][0] == pos and tag[x][1].lower() not in result_list:
				result_list.append(tag[x][1].lower())
	return result_list

def extract_characters(list):
	for x in range(0,len(list)):
		item = str((list[x]))
		item1 = item.replace("[","")
		item2 = item1.replace("]","")
		item4 = item2.replace(item2[0],"")
		while "~" in item4:
			item4 = item4.replace("~","")
		while "|" in item4:
			item4 = item4.replace("|",",")
		while "  " in item4:
			item4 = item4.replace("  ","")
		list[x] = item4
	return list

def replace_commas(list):
	for x in range(0,len(list)):
		item = list[x]
		if "," in list[x]:
			list[x] = list[x].replace(",","|")
	return list
	
def getwords(phrase):
	phrase = phrase.split()
	for x in range(0,len(phrase)):
		if "," in phrase[x]:
			phrase[x] = phrase[x].replace(",","")
		if "." in phrase[x]:
			phrase[x] = phrase[x].replace(".","")
		if "!" in phrase[x]:
			phrase[x] = phrase[x].replace("!","")
		if "?" in phrase[x]:
			phrase[x] = phrase[x].replace("?","")
		phrase[x] = phrase[x].lower()
	return phrase
	
def getlexical(string):
	lexical_words = []
	lexical_tag = lt.tag_string(string,lt.SCHEME_LEXICAL_CLASS)
	for item in lexical_tag:
		if item != " " and item != "":
			lexical_words.append(item[0])
	return lexical_words
	
def getlemma(string):
	lemma_words = []
	lemma_tag = lt.tag_string(string,lt.SCHEME_LEMMA)
	for item in lemma_tag:
		if item != " " and item != "":
			lemma_words.append(item[0])
	return lemma_words

#uses lemma to find most similar string matches in sentences
def find_matches(string,list):
	string = string
	string_words = getwords(string)
	lemma_words = getlemma(string)
	all_highest_matches = []
	highest_match = -1
	highest_matches = []
	match_percent = 0
	
	for x in range(0,len(list)):
		item = list[x]
		match = 0
		item_words = getwords(str(item))
		for word in string_words:
			if word in item_words:
				match += 1
			
		if match == highest_match and item not in highest_matches:
			highest_matches.append(item)
		if match > highest_match:
			if len(highest_matches) > 0:
				all_highest_matches.append(highest_matches)
			highest_matches = []
			highest_matches.append(item)
			highest_match = match
	if len(highest_matches) > 0:
		all_highest_matches.append(highest_matches)
	highest_match = float(highest_match)
	string_length = float(len(string_words))
		
	match_percent = highest_match / string_length * 100
	return all_highest_matches

def find_pos_matches(string,list):
	matches = []
	string_pos = getlexical(string)
	
	for x in range(0,len(list)):
		item = list[x]
		item_pos = getlexical(item)
		if item_pos == string_pos:
			matches.append(x)
	return matches
#--------------------------------
		
phrase_list = extract_characters(phrase_list)
reaction_list = extract_characters(reaction_list)

#this block of code prints all parts of speech present in its database.
'''
all_pos = []
for item in phrase_list:
	tag = lt.tag_string(item,lt.SCHEME_LEXICAL_CLASS)
	for x in range(0,len(tag)):
		if tag[x][0] not in all_pos:
			all_pos.append(tag[x][0])
print(all_pos)
'''

if skip_intro == False:
	set_font('Menlo',14)
	clear()
	print("Chatbot v.3.0\nThis program will attempt to have a conversation with the user. \nFor the best results:\n 1: Use correct grammar, spelling, and punctuation\n 2: Give logical answers\n 3: Treat it like a real person!\n\nLoading... ")
	#set_font(font,font_size)

#this creates the list of all examples of parts of speech (lowercase, no repeats) so it can insert them later if needed.
nouns = search_pos("Noun",phrase_list)
verbs = search_pos("Verb",phrase_list)
adjectives = search_pos("Adjective",phrase_list)
adverbs = search_pos("Adverb",phrase_list)
prounouns = search_pos("Pronoun",phrase_list)
determiners = search_pos("Determiner",phrase_list)
particles = search_pos("Particle",phrase_list)
prepositions = search_pos("Preposition",phrase_list)
interjections = search_pos("Interjection",phrase_list)
conjunctions = search_pos("Conjunction",phrase_list)
punctuations = search_pos("Punctuation",phrase_list)
numbers = search_pos("Number",phrase_list)
dashes = search_pos("Dash",phrase_list)
sentenceterminators = search_pos("SentenceTerminator",phrase_list)
otherwords = search_pos("OtherWord",phrase_list)

print("Go!")

#------------testing------------

'''
current_matches = find_matches(str(raw_input()),phrase_list)
print(current_matches)
print()
for x in range(len(current_matches[1])-1,-1,-1):
	print(current_matches[1][x])
'''

#-----------main loop------------

#this while loop is the real conversation. It only ends when you say one of the "stop" phrases.

conversation = 1
checkpoint2 = 0
checkpoint1 = 1

while conversation == 1:
	
	if tester:
		for x in range(0,len(phrase_list)):
			print(str(x) + ": " + str(phrase_list[x]) + " : " + str(reaction_list[x]))
	
	#-----------input------------
	
	if checkpoint1 == 1:
		user_input = raw_input()
	clear()
	
	#if you said a stop phrase, end the conversation immediately
	if user_input.lower() in stop_phrases:
		conversation = 0
	
	if conversation == 0:
		break
		
	checkpoint1 = 1
	
	#if you react to it in a new way, it learns how to react to what it just said.
	if checkpoint2 == 1:
		if reaction not in phrase_list and reaction != "":
			phrase_list.append(reaction)
			reaction_list.append(user_input)
		
	checkpoint2 = 1
	
	#------formation of response------
	
	#this part uses the input's parts of speech to determine which parts of speech it should use (and in which order) in its response.
	reaction_pos_matches = []
	
	pos_matches_index = find_pos_matches(user_input,phrase_list)
	if len(pos_matches_index) == 0:
		#print("New sentence structure!")
		pos_matches_index.append(random.randint(0,len(phrase_list)))
		
	for num in pos_matches_index:
		reaction_pos_matches.append(reaction_list[int(num)])
		#reaction_pos_matches is all the possible reaction part of speech structures, which it then chooses from randomly.
		
	reaction_pos = getlexical(random.choice(reaction_pos_matches))
	#print("Planned reaction sentence structure: " + str(reaction_pos) + "\n")
	
	#now, it has a black slate of parts of speech to fill in (e.g., noun, verb, adjective). The next part fills these in with the most common pos in the responses to the most vocabularatively similar phrases.
	pos_vocab_matches = []
	for x in pos_matches_index:
		pos_vocab_matches.append(phrase_list[x])
	
	best_phrase_matches_unmod = find_matches(user_input,pos_vocab_matches)
	#print("pos_vocab_matches: "+str(pos_vocab_matches)) + "\n"
	
	#print("best phrase matches, unmod: "+str(best_phrase_matches_unmod)+ "\n")
	
	#best_phrase_matches_unmod isn't formatted correctly, so it creates a new list the right way so that it can compare:
	best_phrase_matches = []
	for phrase in best_phrase_matches_unmod[0]: #that 0 can change depending on if it contains many levels of matching and not just the hightest matching, so it needs to be fixed
		best_phrase_matches.append(phrase)
	
	best_reaction_matches = []
	for x in range(0,len(phrase_list)):
		if phrase_list[x] in best_phrase_matches:
			best_reaction_matches.append(reaction_list[x])
	#at this point, it has a list of responses (from the most similar in vocab from the most similar in structure phrases) from which it pulls its parts of speech
	#print("gold: " + str(best_reaction_matches))
	#best_reaction_matches is the real gold.
	reaction = best_reaction_matches
	
	#------------output-------------
	
	#next, when showing the user the response, it color-codes words to verb, noun, adjective, etc.
	Adjective_ltr = []
	Pronoun_ltr = []
	Verb_ltr = []
	Adverb_ltr = []
	Determiner_ltr = []
	Conjunction_ltr = []
	Preposition_ltr = []
	
	tag = lt.tag_string(reaction,lt.SCHEME_LEXICAL_CLASS)
	for word in range(0,len(tag)):
		
		#it then sets the color depending on which part of speech the word is that it is currently printing
		if tag[word][0] == "Pronoun":
			for number in range(tag[word][2][0],tag[word][2][1]):
				Pronoun_ltr.append(number)
		if tag[word][0] == "Verb":
			for number in range(tag[word][2][0],tag[word][2][1]):
				Verb_ltr.append(number)
		if tag[word][0] == "Adjective":
			for number in range(tag[word][2][0],tag[word][2][1]):
				Adjective_ltr.append(number)
		if tag[word][0] == "Adverb":
			for number in range(tag[word][2][0],tag[word][2][1]):
				Adverb_ltr.append(number)
		if tag[word][0] == "Determiner":
			for number in range(tag[word][2][0],tag[word][2][1]):
				Determiner_ltr.append(number)
		if tag[word][0] == "Conjunction":
			for number in range(tag[word][2][0],tag[word][2][1]):
				Conjunction_ltr.append(number)
		if tag[word][0] == "Preposition":
			for number in range(tag[word][2][0],tag[word][2][1]):
				Preposition_ltr.append(number)
				
	#if talk is true, it says the response in line with the speed at which it prints the characters, so as to look more realistic
	if talk:
		speech.say(reaction,dialect,.53)
		
	for x in range(0,len(reaction)):
		set_color(.0, .0, .0)
		if x in Pronoun_ltr:
			set_color(.16, .16, 1.0)
		if x in Verb_ltr:
			set_color(1.0, .26, .26)
		if x in Adjective_ltr:
			set_color(.16, .72, 1.0)
		if x in Adverb_ltr:
			set_color(1.0, .21, 1.0)
		if x in Determiner_ltr:
			set_color(.0, .66, .0)
		if x in Conjunction_ltr:
			set_color(1.0, .68, .05)
		if x in Preposition_ltr:
			set_color(.0, .86, .86)
		
		#here is where it actually prints the characters, letter by letter
		sys.stdout.write(reaction[x])
		sys.stdout.flush()
		time.sleep(.03)
	
	#then, all of it repeats.
	
#-------------saving-------------

#after the conversation is over, it replaces all the commas to | in the phrases so that it stores the information properly
phrase_list = replace_commas(phrase_list)
reaction_list = replace_commas(reaction_list)

#then, the data is "saved" to 2 files: phase_file and reaction_file, using "~" between each character (becuase it has to). The "~"s are removed when retrieving the data in the beginning

outphrase = open("phrase_file.csv","wb")
outreaction = open("reaction_file.csv","wb")

output = csv.writer(outphrase,delimiter = "~",dialect = csv.QUOTE_NONE)
for x in range(0,len(phrase_list)):
	output.writerow(phrase_list[x])
outphrase.close()

output2 = csv.writer(outreaction,delimiter = "~",dialect = csv.QUOTE_NONE)
for x in range(0,len(reaction_list)):
	output2.writerow(reaction_list[x])
outreaction.close()

#lastly, it tells you how many phrases it knows
print("Number of phrases: " + str(len(phrases)))
#-----------------------------------
