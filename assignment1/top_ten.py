import json
import sys
import operator

def main():
    tweet_file = open(sys.argv[1])

    hashtag_count = {}
    for line in tweet_file:
      # parse tweet
      data = json.loads(line)
      if 'lang' in data.keys() and data.get('lang') == 'en':
        if 'entities' in data.keys():
          hashtags_arr = data['entities']['hashtags']
          if len(hashtags_arr) > 0:
            for hashtag_data in hashtags_arr:
              hashtag = hashtag_data.get('text')
              if hashtag in hashtag_count:
                hashtag_count[hashtag] += 1
              else:
                hashtag_count[hashtag] = 1
    sorted_hashtag_count = sorted(hashtag_count.items(), key=operator.itemgetter(1), reverse=True)
    hashtag_index = 0
    for hashtag_data in sorted_hashtag_count:
      hashtag_index += 1
      if hashtag_index <= 10:
        print hashtag_data[0], hashtag_data[1]

if __name__ == '__main__':
    main()
