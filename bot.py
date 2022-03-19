import requests
import json
import os
from telegram import *
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

API_KEY = "ef10c0aebamsh2e3ec5463be047bp1b6b07jsn95571245a1b9"
PORT = int(os.environ.get('PORT', 5000))

def getVideoID(url):
    return str(url).split('/')[-1]


def getVideoDetails(videoID):
    url = 'https://youtube-media-downloader.p.rapidapi.com/v2/video/details'
    headers = {
        'x-rapidapi-host': "youtube-media-downloader.p.rapidapi.com",
        'x-rapidapi-key': API_KEY
    }

    querystring = {"videoId": videoID}

    response = requests.request("GET", url, headers=headers, params=querystring).json()
    subtitleURL = response['subtitles']['items'][0]['url']

    return subtitleURL


def convertSubtitles(subtitleUrl):
    url = "https://youtube-media-downloader.p.rapidapi.com/v2/video/subtitles"
    headers = {
        'x-rapidapi-host': "youtube-media-downloader.p.rapidapi.com",
        'x-rapidapi-key': API_KEY
    }

    querystring = {"subtitleUrl": subtitleUrl, "format": "json"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    subtitleText = json.loads(response.text)
    finalText = ""

    for obj in subtitleText:
        finalText += (str(obj['text']) + ' \n ')
    
    return finalText


def returnSubtitleText(text):
    # pdf = FPDF()
    # pdf.add_page()
    # pdf.set_font("Arial", size=12)
    # # for evey line in the text
    text = ""
    for line in text.split('\n'):
        # pdf.cell(200, 10, txt=line, ln=1, align='C')
        text += line
    
    return text
    
    # pdf.output("D:/Ishjot/Coding/Python/Notebooks/subtitle.pdf")


videoID = getVideoID("https://youtu.be/pwHNannxolo")
subtitleURL = getVideoDetails(videoID)




def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text='Welcome to Subtitle downloader!\nPlease provide a valid url')


def textHandler(update: Update, context: CallbackContext) -> None:
    user_message = str(update.message.text)

    if update.message.parse_entities(types=MessageEntity.URL):
        videoID = getVideoID(user_message)
        subtitleURL = getVideoDetails(videoID)
        text = returnSubtitleText(subtitleURL)
        update.message.reply_text(text=f'{text}')



def main():
    TOKEN = "5226286617:AAHqsHbsCUBGHgjBrGyeLkaoqR_7qX0r74w"
    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.command, textHandler, run_async=True))
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook('https://ytsubtitlebot.herokuapp.com/' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()

