import json
import sys
import re

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}


def main():
    dictionary_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    scores = {}
    # parsing AFINN-111.txt to fetch sentiment from dictionary
    for line in dictionary_file:  
       term, score = line.split("\t")
       scores[term] = int(score)

    state_scores = {}
    state_tweet_count = {}
    for line in tweet_file:
      # parse tweet
      data = json.loads(line)
      # some data may not contain actual text
      if 'text' in data.keys():
        tweet_text = data.get('text')
        if 'lang' in data.keys() and data.get('lang') == 'en':
          place_data = data.get('place')
          if place_data is not None:
            country_code = place_data.get('country_code')
            if country_code == 'US':
              place_name = place_data.get('full_name')
              place_name_arr = place_name.split(', ')
              if len(place_name_arr) == 2:
                state_abbr = place_name_arr[1]
                if state_abbr in states:
                  net_score = 0.0
                  words = tweet_text.encode('utf-8').split()
                  for word in words:
                    if not word.startswith('https'):
                      clean_word = re.sub('[^A-Za-z]+', '', word).lower()
                      if clean_word in scores:
                        net_score += scores[clean_word]  
                      else:
                        net_score += 0.0
                  if state_abbr in state_scores:
                    state_scores[state_abbr] += net_score
                  else:
                    state_scores[state_abbr] = net_score

                  if state_abbr in state_tweet_count:
                    state_tweet_count[state_abbr] += 1.0
                  else:
                    state_tweet_count[state_abbr] = 1.0
    state_happiness = {}
    for state_abbr in state_scores:
      score = round(state_scores[state_abbr]/state_tweet_count[state_abbr], 4)
      if score > 0.0 and score < 1.0:
        state_happiness[state_abbr] = score

    happiest_state = 'AK'
    for state in state_happiness:
      if state_happiness[state] > state_happiness[happiest_state]:
        happiest_state = state
    print happiest_state

if __name__ == '__main__':
    main()
