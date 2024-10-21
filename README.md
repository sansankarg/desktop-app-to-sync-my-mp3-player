# SoulSync 🎧 - Sync Your MP3 Player with Your Soul (And Cloud)

**This is not a revolutionizing idea, but that’s exactly what makes it so great—it’s just one of those little things that makes everyday life a bit easier.**

## The Story Behind SoulSync 📖

Okay, so here’s what happened. Today’s class was *exceptionally* boring. Like, zoning-out-and-thinking-about-life boring. And while I was deep in thought, an idea hit me. 💡

Since I was a kid, I’ve always loved listening to music (who doesn’t, right?). And up until now, I still use my good old MP3 player. It’s a special kind of nostalgia, but there’s one big problem: **Spotify ruined everything**. 😅 In an age where everything’s streaming, it’s just not convenient to transfer songs to an MP3 player.

The thing I love about the MP3 player? It's **disconnected**—no distractions, no internet, just music. Downloading songs is easy with mod spotify apks, but syncing the latest songs to the mp3 player ? That’s a real pain. I mean, I download songs on my phone, but then transferring them to my MP3 player? Ugh, I always found it way too hard.

So I thought, why not solve this problem once and for all?

💡 **SoulSync** was born.

I decided to create a cloud-based solution where I can upload my favorite songs (when I discover them) and sync them to my MP3 player automatically. Whenever I charge my MP3 player using my laptop, it should sync with the latest music stored in the cloud. Cool, right? So, here’s **SoulSync**, powered by Google Drive’s API.

---

## How It Works 🚀

- **Main Application (`main.py`)**: This is the core application with a simple, minimalistic user interface built using Tkinter. It lets you add or delete music files to/from your Google Drive, and yes, you can also sync manually if you like! 🎵

    ![WhatsApp Image 2024-10-21 at 22 50 08_40468e82](https://github.com/user-attachments/assets/da7e7c2e-7be7-431f-a8a0-4e1900367212)

  
- **Forever Sync (`forever.py`)**: This script is set to run on startup (inspired by Samsung DeX). It constantly checks if your MP3 player is connected to your laptop. As soon as it detects your device, it automatically opens SoulSync and starts syncing your music files from Google Drive to your MP3 player.

    Imagine, I just added a kabira song to Google Drive through my phone. That song hasn’t synced to my MP3 player yet. But when I plug in my MP3 player to charge through my laptop, SoulSync detects it, launches, and starts syncing. And yes, don’t judge my song choice, I listen to *all kinds of music*. 😄



https://github.com/user-attachments/assets/1d0f76e7-2525-4712-bc8f-213810365f2e



---

## How to Set It Up 🛠️

1. **Clone the repo** to your local machine:
   ```bash
   git clone https://github.com/sansankarg/desktop-app-to-sync-my-mp3-player
   ```

2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Google Drive API Setup**:
   - Create a project in the [Google Developers Console](https://console.cloud.google.com/).
   - Enable the Google Drive API for your project.
   - Download the `credentials.json` file and place it in the same directory as your code.
   - Follow the Google API authentication flow the first time you run the app.

4. **Run the main app**:
   ```bash
   python main.py
   ```

5. **Set `forever.py` to run on startup**:
   - For Windows users, you can add a shortcut to this script in the Startup folder.
   - For Mac or Linux, use cron jobs or any other preferred method.

---

## Features ✨

- Add and delete songs from Google Drive using a simple UI.
- Automatically sync your MP3 player when it’s connected to your laptop.
- Manual sync option for when you just can’t wait.
- Set and forget: `forever.py` handles the rest.

---


## Conclusion

This might not be revolutionary, but hey, it solved a pain point in my daily routine, and I hope it can help you too! 🙌

