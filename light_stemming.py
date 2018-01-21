
# LIGHT STEMMING APPROACH

from __future__ import division
from string import punctuation
import editdistance
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
    

# Return the Levenshtein distance between two words
def computeLevenshteinDistance(student_ans_word, correct_ans_word):
	return editdistance.eval(student_ans_word, correct_ans_word)


# Return the similarity score between two words
def computeSimilarityScore(lev_distance, student_ans_word, correct_ans_word):
	# Formula: S(s1, s2) = 1 - (D(s1, s2) / (max(L(s1), L(s2))))
	# where L is the length of a given string
	return 1 - (lev_distance / (max(len(student_ans_word), len(correct_ans_word))))


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

# Split each one of the two anwers into an array of words, processing one word at a time

list_of_student_ans_words = student_ans_no_nums.translate(None, punctuation).lower().split()
list_of_correct_ans_words = correct_ans_no_nums.translate(None, punctuation).lower().split()

# [1] Removal of stopwords

list_of_student_ans_words_no_stops = removeStopwords(list_of_student_ans_words)
list_of_correct_ans_words_no_stops = removeStopwords(list_of_correct_ans_words)

# [4] Remove prefix if word length is greater than 3, else skip this step

list_of_student_ans_words_no_stops_suf = []
list_of_correct_ans_words_no_stops_suf = []

for student_ans_word in list_of_student_ans_words_no_stops:
	new_word = student_ans_word

	if len(student_ans_word) > 3:
		new_word = removeSuffix(student_ans_word)

	list_of_student_ans_words_no_stops_suf.append(new_word)

for correct_ans_word in list_of_correct_ans_words_no_stops:
	new_word = correct_ans_word

	if len(correct_ans_word) > 3:
		new_word = removeSuffix(correct_ans_word)

	list_of_correct_ans_words_no_stops_suf.append(new_word)


# Find the similarities by giving a weight to each word in both answers
# Formula: Word(i) weight = 1 / (total words in correct answer)

wordWeight = 1 / len(list_of_correct_ans_words_no_stops_suf)

print '\n'
print 'Word weight: {0}'.format(wordWeight)

# For each word in student answer, calculate the similarity with words in correct answer

# [1] Calculate the Levenshtein distance between every word in student answer and words in correct answer

list_of_lev_distances = []

for student_ans_word_idx in range(len(list_of_student_ans_words_no_stops_suf)):
	for correct_ans_word_idx in range(len(list_of_correct_ans_words_no_stops_suf)):
		student_ans_word = list_of_student_ans_words_no_stops_suf[student_ans_word_idx]
		correct_ans_word = list_of_correct_ans_words_no_stops_suf[correct_ans_word_idx]

		# Compute the Levenshtein distance between student answer word and correct answer word
		levenshtein_distance = computeLevenshteinDistance(student_ans_word, correct_ans_word)
		
		# Create a tuple specifying the index for the student and correct answer word as well as the Levenshtein distance
		lev_distance_tuple = (student_ans_word_idx, correct_ans_word_idx, levenshtein_distance)

		# Insert the tuple into a list
		list_of_lev_distances.append(lev_distance_tuple)

print '\n'
print 'List of Levenshtein distance:'
print list_of_lev_distances

# [2] Calculate the similarity score between every word in student answer and words in correct answer

list_of_sim_score = []

for student_ans_word_idx in range(len(list_of_student_ans_words_no_stops_suf)):
	for correct_ans_word_idx in range(len(list_of_correct_ans_words_no_stops_suf)):
		
		for lev_distance in list_of_lev_distances:
			if lev_distance[0] == student_ans_word_idx and lev_distance[1] == correct_ans_word_idx:

				student_ans_word = list_of_student_ans_words_no_stops_suf[student_ans_word_idx]
				correct_ans_word = list_of_correct_ans_words_no_stops_suf[correct_ans_word_idx]

				# Compute the similarity score between student answer word and correct answer word
				similarity_score = computeSimilarityScore(lev_distance[2], student_ans_word, correct_ans_word)

				# Create a tuple specifying the index for student and correct answer word as well as the similarity score
				sim_score_tuple = (student_ans_word_idx, correct_ans_word_idx, similarity_score)

				# Insert the tuple into a list
				list_of_sim_score.append(sim_score_tuple)

				break

print '\n'
print 'List of Similarity score:'
print list_of_sim_score

# For each word in student answer, calculate the similarity with words in correct answer

finalMark = 0

# [1] If the similarity between StudentWord(i) and CorrectWord(i) = 1 then add weight to the final mark
# [2] Elseif the similarity between StudentWord(i) and CorrectWord(i) < 1 and >= 0.96, add weight to the final mark
# [3] Elseif the similarity between StudentWord(i) and CorrectWord(i) >= 0.8 and < 0.96, add half the weight to the final mark
# [4] Elseif the similarity between StudentWord(i) and CorrectWord(i) < 0.8 then no weight is added to the final mark

for student_ans_word_idx in range(len(list_of_student_ans_words_no_stops_suf)):
	for correct_ans_word_idx in range(len(list_of_correct_ans_words_no_stops_suf)):

		for sim_score in list_of_sim_score:
			if sim_score[0] == student_ans_word_idx and sim_score[1] == correct_ans_word_idx:

				if sim_score[2] == 1:
					finalMark = finalMark + wordWeight
				elif sim_score[2] >= 0.96 and sim_score[2] < 1:
					finalMark = finalMark + wordWeight
				elif sim_score[2] >= 0.8 and sim_score[2] < 0.96:
					finalMark = finalMark + (wordWeight * 0.5)
				else:
					finalMark = finalMark

				break

print '\n'
print 'LIGHT STEMMING APPROACH'
print '-----------------------'
print 'Final Mark (%): {0} ({1} %)'.format(finalMark, finalMark * 100)
