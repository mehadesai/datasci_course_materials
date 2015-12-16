import json
import sys
import re

def main():
    tweet_file = open(sys.argv[1])

    word_freq = {}
    total_words = 0.0
    for line in tweet_file:
      data = json.loads(line)
      if 'text' in data.keys():
        tweet_text = data.get('text')
        if 'lang' in data.keys() and data.get('lang') == 'en':
          words = tweet_text.encode('utf-8').split()
          for word in words:
            if not word.startswith('https'):
              clean_word = re.sub('[^A-Za-z]+', '', word).lower()
              if len(clean_word) > 1:
                total_words += 1.0
                if clean_word not in word_freq:
                  word_freq[clean_word] = 1.0
                else:
                  word_freq[clean_word] += 1.0
    for word in word_freq:
      per_word_freq = round(float(word_freq[word]/total_words), 4)
      print word, per_word_freq

if __name__ == '__main__':
    main()
