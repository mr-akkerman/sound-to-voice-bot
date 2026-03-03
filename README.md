# sound-to-voice-bot

Telegram bot that converts MP3 files into voice messages.

Send it an `.mp3` — it replies with a voice message. That's it.

## Requirements

- Python 3.11+
- ffmpeg

## Running locally

```bash
git clone https://github.com/mr-akkerman/sound-to-voice-bot
cd sound-to-voice-bot
pip install -r requirements.txt
cp .env.example .env
# put your bot token in .env
python main.py
```

Get a bot token from [@BotFather](https://t.me/BotFather).

## Deploy on Railway

1. Fork this repo
2. Create a new Railway project → connect the fork
3. Add `BOT_TOKEN` to environment variables
4. Deploy — ffmpeg is picked up automatically via `nixpacks.toml`

## Environment variables

| Variable | Description |
|---|---|
| `BOT_TOKEN` | Telegram bot token |

## How it works

1. User sends an MP3 as a file attachment
2. Bot downloads it to a temp directory
3. [pydub](https://github.com/jiaaro/pydub) converts it to OGG/Opus via ffmpeg
4. Bot sends the result as a Telegram voice message
5. Temp files are deleted

## License

MIT
