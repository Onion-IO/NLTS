import PySimpleGUI as sg
import snscrape.modules.twitter as twitter
import nltk
import csv

#Initialize Variables
DOPOS = True
DOREP = True

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

sg.theme('DarkTeal')
# Setup sg
layout = [[sg.Text('Account to scrape:')], [sg.Text('@'),
                                            sg.InputText()],
          [sg.Text('Number of Tweets to scrape')],
          [sg.Text('0<'), sg.InputText()],
          [sg.Checkbox('Include Parts of speech', default=True, key="POS")],
          [sg.Checkbox('Include replies to users', default=True, key="REP")],
          [sg.Button('Start'), sg.Button('Cancel')]]

# Create the Window
window = sg.Window('VTS', layout, no_titlebar=True, titlebar_icon=None)
# Event Loop to process "events" and get the "values" of the inputs
while True:

  event, values = window.read()
  if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
    break
  print('Scraping @', values[0], ' for ', values[1], ' Tweets.')

  #Set checkbox values
  DOPOS = values["POS"]
  DOREP = values["REP"]

  print('scraping started')
  USR = values[0]
  TTS = int(values[1])

  TTS >= 100

  # Configure the TwitterScraper object
  scraper = twitter.TwitterSearchScraper(f'from:{USR}')

  # Open a CSV file and write the tweets and their parts of speech to it
  with open('tweets_with_POS.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([
      "Tweet Number", "Word 1", "Part of Speech 1", "Word 2",
      "Part of Speech 2", "Word 3", "Part of Speech 3", "..."
    ])
    for i, tweet in enumerate(scraper.get_items()):
      if i >= TTS:
        break
      if DOREP == False and tweet.inReplyToUser != None:
        continue
      words = nltk.word_tokenize(tweet.rawContent)
      pos_tags = nltk.pos_tag(words)
      row = [i + 1]
      for word, pos in pos_tags:
        if DOPOS == True:
          row.extend([word, pos])
        else:
          row.extend([word])
      writer.writerow(row)
    print('done')

window.close()
