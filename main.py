# code is not adapted for pyinstaller so keep that in mind

import time,math,datetime,pygame, webview,threading,os
from flask import Flask, render_template, jsonify
from flask_cors import CORS

today = datetime.date.today()
new_year = datetime.date(today.year + 1, 1, 1)

config = {
    "song": "TheFatRat - Xenogenesis",
    "volume": 0.5,
    "debug": False, # to test the song
    "temp": {
        "didDebug": False,
        "didPlay": False
    }
}

drops = {
    "TheFatRat - Xenogenesis": 58.5 # time where the drop starts
}

pygame.mixer.init()
app = Flask(__name__)
CORS(app)

# totally not yoinked from stack overflow
def add_secs(tm, secs):
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate.time()

def play_song(song_path):
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.set_volume(config["volume"])
    pygame.mixer.music.play()

def get_unix_to_new_year():
    global new_year, today

    if config["debug"]:
        if not config["temp"]["didDebug"]:
            config["temp"]["didDebug"] = True

            # very long line so what this does is
            # it gets the current time and adds the whole song length untill the drop + 3 seconds to the current time
            # and sets it as the new year. This is basically to test the song not used anymore.
            new_year = datetime.datetime.combine(datetime.date.today(), add_secs(datetime.datetime.now().time(), drops[config["song"]]+3))
    else:

        # if time is greater than new year + 7 days then set new year to next year
        if time.time() > time.mktime(new_year.timetuple()) + 604800:
            new_year = datetime.date(today.year + 1, 1, 1)
            today = datetime.date.today()
    
    return time.mktime(new_year.timetuple())

def close_window():
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os._exit(0)
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_countdown')
def new_year_countdown():
    nextYearUnix = get_unix_to_new_year()
    timeLeft = nextYearUnix - time.time()

    if timeLeft <= drops[config["song"]] and not config["temp"]["didPlay"]:
        config["temp"]["didPlay"] = True
        play_song('music/' + config["song"] + '.mp3')

    return jsonify({"countdown": "{:,}".format(math.floor(timeLeft))})

if __name__ == '__main__':
    threading.Thread(target=app.run, kwargs={'port': 8080}).start()

    window = webview.create_window('New Year Countdown | Made by upio', 'http://localhost:8080', width=800, height=800, resizable=False)
    window.events.closing += close_window

    webview.start()

