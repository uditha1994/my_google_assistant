"""#steps todo
1.   Give input , Some Questions
2.   Based on questions, decide what to do
      * on device operation
      * Who are you kinds of message?
      * Asking some questions?
3.   Give proper answer for responce
4.   If the question is related to search internet, get the answer from google Gemini model
5.   If you got an answer, then plz convert it to Text to Speech (gTTS)


"""

!pip install -q -U google-generativeai
!pip install gTTS

import pathlib
import textwrap

import google.generativeai as genai
from gtts import gTTS

from IPython.display import display
from IPython.display import Markdown
from IPython.display import Audio, display


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

genai.configure(api_key=GOOGLE_API_KEY)

from google.colab import userdata
GOOGLE_API_KEY = userdata.get('GOOGLE_API_KEY')
model = genai.GenerativeModel('gemini-pro')

#step 01
def ask_question(name):
  ques = "Hey "+name+", What do you want?"
  ques = input(ques)
  return ques

ask_question("Kamal")

#step 02
def classify_questions(ques):
  goahead_with_web_search = False
  device_lst = ['alarm','reminder','message','call']
  personal_lst = ['who are you?','who created you']

  device = False
  for i in device_lst:
    if i in ques:
      device = True

  personal_question = False
  for i in personal_lst:
    if i in ques.lower():
      personal_question = True

  if personal_question:
    print("Hey I am a personal assistant created by Uditha")

  if device:
    print("This question is related to device things, which is not supported in our google assistant!!")

  if device:
    goahead_with_web_search = False
  elif personal_question:
    goahead_with_web_search = False
  else:
    goahead_with_web_search = True

  return goahead_with_web_search

classify_questions("Who are you?")

#Start searching with google gemini

def ask_gemini(ques):
  modified_promt = "give me answer to this question" + ques + 'in maximum of 50 words'
  response = model.generate_content(modified_promt)
  #get formated responce
  to_markdown(response.text)
  #get responce
  return response.text

def speak(answer):
  tts = gTTS(answer)
  tts.save('audio.mp3')
  display(Audio('audio.mp3', autoplay=True))

#finalize function
have_any_other_ques = 'y'
name = ''

while have_any_other_ques == 'y':

  if name == '':
    name = input("Hey, What is your name?")

  q = ask_question(name)

  go_ahead = classify_questions(q)
  answer = ''

  if go_ahead == True:
    answer = ask_gemini(q)
    print(answer)
    speak(answer)

  have_any_other_ques = input("Do you have any other questions??")
