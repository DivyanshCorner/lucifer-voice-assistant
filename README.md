# Lucifer

A voice-controlled personal assistant for Windows, written in Python. Say a command out loud and Lucifer answers back or does the job for you: opening websites, playing music, reading out the weather, looking things up on Wikipedia and more.

## Features

- Speech input through the microphone (Google Web Speech) and spoken replies through the Windows speech engine
- Time of day greeting on start-up
- Tells the current time and date
- Wikipedia summaries read aloud
- Weather by city (OpenWeatherMap)
- Maths and general questions (Wolfram Alpha)
- Plays a song on YouTube, or a random track from your music folder
- Opens common sites: YouTube, Instagram, Google, Gmail, Stack Overflow, news headlines
- Google search by voice
- Volume up, down and mute
- Takes a photo with the webcam
- Logs off the PC on request

## Requirements

- Windows 10 or 11 (speech output uses SAPI5, and a few commands use Windows-only calls)
- Python 3.9 or newer
- A working microphone and an internet connection

## Installation

```bash
git clone https://github.com/DivyanshCorner/lucifer-voice-assistant.git
cd lucifer-voice-assistant
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

If `PyAudio` fails to build, install a prebuilt wheel instead:

```bash
pip install pipwin
pipwin install pyaudio
```

## Configuration

Copy `.env.example` to `.env` and fill in your own values. The file is ignored by git, so your keys stay on your machine.

| Variable              | Purpose                                              | Where to get it                                  |
| --------------------- | ---------------------------------------------------- | ------------------------------------------------ |
| `OPENWEATHER_API_KEY` | Weather lookups                                      | https://openweathermap.org/api                   |
| `WOLFRAM_APP_ID`      | Calculation and knowledge questions                  | https://developer.wolframalpha.com               |
| `MUSIC_DIR`           | Folder used by "play music" (default: `~/Music`)     | Any folder on your PC                            |

Features that need a missing key will tell you so instead of failing.

## Usage

```bash
python lucifer.py
```

Wait for "How can I help you?" and then speak.

| Say                                  | What happens                                     |
| ------------------------------------ | ------------------------------------------------ |
| "Wikipedia Albert Einstein"          | Reads a three sentence summary                   |
| "What is the time" / "What is the date" | Speaks the current time or date               |
| "Weather"                            | Asks for a city, then reports the conditions     |
| "Calculate"                          | Asks a question and answers it with Wolfram Alpha|
| "Play song on YouTube"               | Asks for a title and plays it                    |
| "Play music"                         | Plays a random track from `MUSIC_DIR`            |
| "Open YouTube" / "Open Google" / "Open Gmail" / "Open Insta" / "Open Stackoverflow" | Opens the site |
| "News"                               | Opens the Times of India headlines               |
| "Search python decorators"           | Searches Google                                  |
| "Volume up" / "Volume down" / "Mute" | Controls system volume                           |
| "Take a photo"                       | Saves `img.jpg` from the webcam                  |
| "Log off"                            | Signs out of Windows                             |
| "Good bye" / "Exit"                  | Shuts Lucifer down                               |

## Project structure

```
lucifer-voice-assistant/
├── lucifer.py          # the assistant
├── requirements.txt
├── .env.example        # template for your keys
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE
```

## Adding a command

Commands are handled in the `handle()` function in `lucifer.py`. Write a small function that does the work, then add a branch that matches the phrase you want. Simple "open this site" commands only need a new entry in the `SITES` dictionary.

## Troubleshooting

- **"Pardon me, please say that again" every time:** check that the right microphone is the Windows default input device and that you are online, since recognition is done by Google's service.
- **No voice or the wrong voice:** the second installed Windows voice is used when available. Change the index near the top of `lucifer.py` to pick another one.
- **Weather says the key is not configured:** make sure `.env` sits next to `lucifer.py` and contains `OPENWEATHER_API_KEY=...`. New keys can take a couple of hours to activate.

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Released under the [MIT License](LICENSE).
