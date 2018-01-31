# An Automated System for Essay Scoring of Online Exams in Arabic based on Stemming Techniques and Levenshtein Edit Operations

## Global NIPS Paper Implementation Challenge

I implemented the paper based on the research methodology

## Original Paper

https://arxiv.org/pdf/1611.02815.pdf

## Main Goal

Develop an automated system is proposed for essay scoring in Arabic language for online exams based on stemming techniques and  Levenshtein edit operations

## Programming Tool

<ul>
  <li>Python 2.7</li>
</ul>

## Files

Some important files / directories:

<ul>
  <li><b>heavy_stemming.py</b>
    <p>
      The whole source code for heavy stemming approach
    </p>
  </li>
  <li><b>light_stemming.py</b>
    <p>
      The whole source code for light stemming approach
    </p>
  </li>
  <li><b>docs</b>
    <p>
      Several text files, such as <i>questions</i>, <i>correct_ans</i>, and <i>student_ans</i>
    </p>
  </li>
  <li><b>prefixes</b>
    <p>
      Stores the list of prefixes
    </p>
  </li>
  <li><b>suffixes</b>
    <p>
      Stores the list of suffixes
    </p>
  </li> 
  <li><b>stopwords</b>
    <p>
      Stores the list of stopwords
    </p>
  </li>
</ul>

## To Run

To run the program, execute the following command:
<ul>
  <li>Heavy stemming approach: <i>python heavy_stemming.py</i></li>
  <li>Light stemming approach: <i>python light_stemming.py</i></li>
</ul>

## Methodology

Both approaches (heavy and light stemming) uses the following steps. The difference is only in the removal of prefixes and suffixes.

<ul>
  <li><b>Begin Heavy Stemming on both student and correct answers</b>
    <p>
      This initial step consists of two sub-steps, such as removal of numbers from both answers and removal of diacritics from both answers. For the latter task, each answer is converted to unicode then the diacritics can be removed from both answers.
    </p>
    <p>
      <img src="https://github.com/albertusk95/nips-challenge-essay-scoring-arabic/blob/master/assets/img/step_1_AES.png?raw=true"/>
    </p>
  </li>
  <li><b>Split each one of the two anwers into an array of words, processing one word at a time</b>
    <p>
      It includes several steps, such as removal of stopwords, removal of prefix if word length is greater than 3, and removal of suffix if word length is greater than 3.
    </p>
    <p>
      <img src="https://github.com/albertusk95/nips-challenge-essay-scoring-arabic/blob/master/assets/img/step_2_AES.png?raw=true"/>
    </p>
  </li>
  <li><b>Find the similarities by giving a weight to each word in both answers</b>
    <p>
      The weight formula for each word:
      <i>Word(i) weight = 1 / (total words in correct answer)</i>
    </p>
    <p>
      <img src="https://github.com/albertusk95/nips-challenge-essay-scoring-arabic/blob/master/assets/img/step_4_AES.png?raw=true"/>
    </p>
  </li>
  <li><b>For each word in student answer, calculate the similarity with words in correct answer</b>
    <p>
      Several steps were included, such as calculating the Levenshtein distance between every word in student answer and words in correct answer AND calculating the similarity score between every word in student answer and words in correct answer.
    </p>
    <p>
      <img src="https://github.com/albertusk95/nips-challenge-essay-scoring-arabic/blob/master/assets/img/step_8_AES.png?raw=true"/>
    </p>
    <p>
      <img src="https://github.com/albertusk95/nips-challenge-essay-scoring-arabic/blob/master/assets/img/step_5_AES.png?raw=true"/>
    </p>
    <p>
      <img src="https://github.com/albertusk95/nips-challenge-essay-scoring-arabic/blob/master/assets/img/step_6_AES.png?raw=true"/>
    </p>
  </li>
  <li><b>For each word in student answer, calculate the similarity with words in correct answer</b>
    <p>
      These are the rules for calculating the final mark:
      <ul>
        <li>If the similarity between StudentWord(i) and CorrectWord(i) = 1 then add weight to the final mark</li>
        <li>Elseif the similarity between StudentWord(i) and CorrectWord(i) < 1 and >= 0.96, add weight to the final mark</li>
        <li>Elseif the similarity between StudentWord(i) and CorrectWord(i) >= 0.8 and < 0.96, add half the weight to the final mark</li>
        <li>Elseif the similarity between StudentWord(i) and CorrectWord(i) < 0.8 then no weight is added to the final mark</li>
      </ul>
    </p>
    <p>
      <img src="https://github.com/albertusk95/nips-challenge-essay-scoring-arabic/blob/master/assets/img/step_7_AES.png?raw=true"/>
    </p>
  </li>
</ul>

---

**Albertus Kelvin**<br/>
**Bandung Institute of Technology**<br/><br/>
**Code was developed on January 21st, 2018**<br/>
**Code was made publicly available on January 31st, 2018**
