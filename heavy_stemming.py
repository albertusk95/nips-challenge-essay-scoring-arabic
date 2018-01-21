
# HEAVY STEMMING APPROACH

from string import punctuation
import unidecode

DATASET = 'docs'


# Return list of words without stopwords
def removeStopwords(list_of_words):
	with open('stopwords') as f:
		stopwords = f.readlines()

	stopwords = [x.strip() for x in stopwords]

	return [ x for x in list_of_words if x not in stopwords ]


# Return new string without prefix if the string is started with a certain prefix
def removePrefix(text):
	with open('prefixes') as f:
		prefixes = f.readlines()

	prefixes = [x.strip() for x in prefixes]

	for prefix in prefixes:
		if text.startswith(prefix):
			return text[len(prefix):]
    
	return text


# Return new string without suffix if the string is ended with a certain suffix
def removeSuffix(text):
	with open('suffixes') as f:
		suffixes = f.readlines()

	suffixes = [x.strip() for x in suffixes]

	for suffix in suffixes:
		if text.endswith(suffix):
			return text[:len(text)-len(suffix)]

	return text
    

# Get both question and correct answer from the database
with open(DATASET + '/questions') as f:
	questions_text = f.read().replace('\n', ' ')

with open(DATASET + '/correct_ans') as f:
	correct_ans_text = f.read().replace('\n', ' ')

# Get the student's answers
with open(DATASET + '/student_ans') as f:
	student_ans_text = f.read().replace('\n', ' ')

# Begin Heavy Stemming on both student and correct answers

# [1] Removal of numbers from both answers

student_ans_no_nums = ''.join([i for i in student_ans_text if not i.isdigit()])
correct_ans_no_nums = ''.join([i for i in correct_ans_text if not i.isdigit()])

# [2] Removal of diacritics from both answers

# Convert each answer to unicode
student_ans_no_nums_unicode = student_ans_no_nums_unicode.decode('utf-8')
correct_ans_no_nums_unicode = correct_ans_no_nums_unicode.decode('utf-8')

# Remove diacritics from both answers
student_ans_no_nums_diacritics = unidecode.unidecode(student_ans_no_nums_unicode)
correct_ans_no_nums_diacritics = unidecode.unidecode(correct_ans_no_nums_unicode)


# Split each one of the two anwers into an array of words, processing one word at a time

list_of_student_ans_words = student_ans_no_nums_diacritics.translate(None, punctuation).lower().split()
list_of_correct_ans_words = correct_ans_no_nums_diacritics.translate(None, punctuation).lower().split()

# [1] Removal of stopwords

list_of_student_ans_words_no_stops = removeStopwords(list_of_student_ans_words)
list_of_correct_ans_words_no_stops = removeStopwords(list_of_correct_ans_words)

# [4] Remove prefix if word length is greater than 3, else skip this step

list_of_student_ans_words_no_stops_pref = []
list_of_correct_ans_words_no_stops_pref = []

for student_ans_word in list_of_student_ans_words_no_stops:
	new_word = student_ans_word

	if len(student_ans_word) > 3:
		new_word = removePrefix(student_ans_word)

	list_of_student_ans_words_no_stops_pref.append(new_word)

for correct_ans_word in list_of_correct_ans_words_no_stops:
	new_word = correct_ans_word

	if len(correct_ans_word) > 3:
		new_word = removePrefix(correct_ans_word)

	list_of_correct_ans_words_no_stops_pref.append(new_word)

# [5] Remove suffix if word length is greater than 3, else skip this step

list_of_student_ans_words_no_stops_pref_suf = []
list_of_correct_ans_words_no_stops_pref_suf = []

for student_ans_word in list_of_student_ans_words_no_stops_pref:
	new_word = student_ans_word

	if len(student_ans_word) > 3:
		new_word = removeSuffix(student_ans_word)

	list_of_student_ans_words_no_stops_pref_suf.append(new_word)

for correct_ans_word in list_of_correct_ans_words_no_stops_pref:
	new_word = correct_ans_word

	if len(correct_ans_word) > 3:
		new_word = removeSuffix(correct_ans_word)

	list_of_correct_ans_words_no_stops_pref_suf.append(new_word)


