import json
import sys

def main():
    dictionary_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    scores = {}
    # parsing AFINN-111.txt to fetch sentiment from dictionary
    for line in dictionary_file:  
       term, score = line.split("\t")
       scores[term] = int(score)

    for line in tweet_file:
      # parse tweet
      data = json.loads(line)
      # some data may not contain actual text
      if 'text' in data.keys():
        tweet_text = data.get('text')

        # check for non-english tweets
        # if 'lang' in data.keys() and data.get('lang') == 'en':
        #  print "English"
        # else:
        #  print tweet_text

        # initialize 0 score for every tweet
        net_score = 0
        words = tweet_text.split()  
        for word in words:
          word_to_search = word.lower()
          if word_to_search in scores.keys():
            net_score += scores[word_to_search]  
          else:
            net_score += 0
        print net_score

if __name__ == '__main__':
    main()
