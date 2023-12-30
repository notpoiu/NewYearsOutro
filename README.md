# NewYearsOutro
A custom new years countdown app made using pywebview &amp; flask &amp; firework.js

## Setting up
You need [python](https://www.python.org/) & [git](https://git-scm.com/)
clone the repo and then install the requirements:
```bash
$ git clone https://github.com/notpoiu/NewYearsOutro.git
...
$ cd NewYearsOutro && pip3 install -r requirements.txt
```

## Testing
To test the app you can edit the "debug" property in the configuration dictionary in `main.py`:
```python
config = {
    "song": "TheFatRat - Xenogenesis",
    "volume": 0.5,
    "debug": True, # to test the song
    "debugSettings": {
        "secondsLeft": 3, # seconds left untill new year + song drop length, you can put negative numbers too
    },
    "refreshCountdown": 100, # seconds untill the countdown refreshes to the next year
    "temp": {
        "didDebug": False,
        "didPlay": False
    }
}
```

## Changing the song
To change the song you can edit the "song" property in the configuration dictionary in `main.py`:
```python
config = {
    "song": "your song",
    "volume": 0.5,
    "debug": True, # to test the song
    "debugSettings": {
        "secondsLeft": 3, # seconds left untill new year + song drop length, you can put negative numbers too
    },
    "refreshCountdown": 100, # seconds untill the countdown refreshes to the next year
    "temp": {
        "didDebug": False,
        "didPlay": False
    }
}
```
Then you need to define at what time the song's beat drop will occur in seconds.
You can do this by adding a new property to the drop dictionary in `main.py`:
```python
drops = {
    "TheFatRat - Xenogenesis": 58.5, # time where the drop starts (s)
    "your song": 0 # time where the drop starts (s)
}
```
Finally you need to add the song into the music directory and name the mp3 file the same as the song property in the configuration dictionary:
```
music
├── TheFatRat - Xenogenesis.mp3
└── your song.mp3
```