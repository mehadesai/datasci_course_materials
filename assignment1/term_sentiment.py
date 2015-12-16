import json
import sys
import re

def main():
    dictionary_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    scores = {}
    # parsing AFINN-111.txt to fetch sentiment from dictionary
    for line in dictionary_file:  
      term, score = line.split("\t")
      scores[term] = int(score)

    new_word_score = {}
    word_freq = {}
    for line in tweet_file:
      data = json.loads(line)
      if 'text' in data.keys():
        tweet_text = data.get('text')
        if 'lang' in data.keys() and data.get('lang') == 'en':
          words = tweet_text.encode('utf-8').split()
          if len(words) > 1:
            tweet_score = 0
            for word in words:
              if word in scores:
                tweet_score += scores[word]
            for word in words:
              if word not in scores:
                if not word.startswith('https'):
                  clean_word = re.sub('[^A-Za-z]+', '', word).lower()
                  if len(clean_word) > 1:
                    if clean_word not in new_word_score:
                      new_word_score[clean_word] = tweet_score
                      word_freq[clean_word] = 1
                    else:
                      new_word_score[clean_word] += tweet_score
                      word_freq[clean_word] += 1      
    for word in new_word_score:
      new_word_score[word] /= word_freq[word]
      print word, str(new_word_score[word])

if __name__ == '__main__':
    main()
