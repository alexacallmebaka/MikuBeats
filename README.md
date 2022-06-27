# MikuBeats
#### *music made simple.*
---
MikuBeats is a very simple Discord bot who plays music from YouTube. She is meant for small servers of trusted friends, so she does not have a permission system similar to what other music bots may have.

MikuBeats is meant for private use only, please do not host her as a public bot.

### Hosting
MikuBeats requires `python >= 3.5`, an `ffmpeg` or `avconv` runtime in your system path, and the modules in `requirements.txt` in order to run. You will also need to create and configure an app through the [Discord Developer Portal](https://discord.com/developers/docs/getting-started). You can also grab a token for your bot there as well.

In MikuBeat's working directory, create a file at `creds/creds.json`. Place your token in this file as follows:
```json
{
        "token":"your_token_here"
}
```

From here, all you need to do to start MikuBeats is to run the `main.py` file. If you feel so inclined, you can run MikuBeats as a [systemd](https://systemd.io/) service by installing the `MikuBeats.service` file onto your system.

Happy listening!
