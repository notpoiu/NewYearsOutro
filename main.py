# code is not adapted for pyinstaller so keep that in mind

import time, math, datetime, pygame, webview

today = datetime.date.today()
new_year = datetime.date(today.year + 1, 1, 1)

config = {
    "song": "TheFatRat - Xenogenesis",
    "volume": 0.5,
    "debug": True, # to test the song
    "debugSettings": {
        "secondsLeft": -19, # seconds left untill new year + song drop length, you can put negative numbers too
    },
    "refreshCountdown": 100, # seconds untill the countdown refreshes to the next year
    "temp": {
        "didDebug": False,
        "didPlay": False
    }
}

drops = {
    "TheFatRat - Xenogenesis": 58.5 # time where the drop starts
}

pygame.mixer.init()

# totally not yoinked from stack overflow
def add_secs(tm, secs):
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate.time()

def play_song(song_path, timeLeft):
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.set_volume(config["volume"])
    pygame.mixer.music.play(start=abs(timeLeft)) # abs cuz the timeLeft is negative

def get_unix_to_new_year():
    global new_year, today, config

    if config["debug"]:
        if not config["temp"]["didDebug"]:
            config["temp"]["didDebug"] = True

            # very long line so what this does is
            # it gets the current time and adds the whole song length untill the drop + debugSettings to the current time
            # and sets it as the new year. This is basically to test the song not used anymore.
            new_year = datetime.datetime.combine(datetime.date.today(), add_secs(datetime.datetime.now().time(), drops[config["song"]]+config["debugSettings"]["secondsLeft"]))

    # if time is greater than new year + config["refreshCountdown"] then set new year to next year
    if time.time() > time.mktime(new_year.timetuple()) + config["refreshCountdown"]:
        pygame.mixer.music.stop()
        new_year = datetime.date(today.year + 1, 1, 1)
        today = datetime.date.today()
        config["temp"]["didPlay"] = False
    
    return time.mktime(new_year.timetuple())

def close_window():
    pygame.mixer.music.fadeout(2000)
    pygame.mixer.music.stop()
    pygame.mixer.quit()

def get_countdown():
    nextYearUnix = get_unix_to_new_year()
    timeLeft = nextYearUnix - time.time()

    if timeLeft <= drops[config["song"]] and not config["temp"]["didPlay"]:
        config["temp"]["didPlay"] = True
        play_song('music/' + config["song"] + '.mp3', timeLeft - drops[config["song"]])

    return {"countdown": "{:,}".format(math.floor(timeLeft))}

if __name__ == '__main__':
    window = webview.create_window('New Year Countdown | Made by upio', 'index.html', width=800, height=800, resizable=False)
    window.expose(get_countdown)
    window.events.closing += close_window

    webview.start()

