
## it can:
- **Remove users without profile pictures**: Often bots or alts used for leaking/spying. Command: `/kicknopfp`
- **Remove recent joiners**: Kick anyone who joined in the last X hours (e.g., during a spam add raid). Command: `/kickjoined <hours>` (default 3 hours)

Kicks are temporary (users can rejoin), but you can edit the script for permanent bans. Built with Pyrogram for full member access.

## Setup
1. **Get Telegram API Credentials**:
   - Go to https://my.telegram.org → Create an app → Get `API_ID` and `API_HASH`.
   - Create a bot via @BotFather → Get `BOT_TOKEN`.

2.**Install Dependencies**:
  - apt update && full-upgrade -y
  - apt install git
  - git clone 
  - cd DresAntiRaid
  - pip install -r requirements.txt
     
3. **Configure .env**:       
     Copy `.env.example` to `.env` and fill in your values.

4. **Run the Bot**:       
     python Dresanti.py

5. **Add to Group**:
- Add the bot to your group/channel.
- Make it an **admin** with "Ban Users" permission.

## Usage
- `/kicknopfp`: Scan and kick all members without a profile picture (suspected bots/alts).
- `/kickjoined 2`: Kick all who joined in the last 2 hours (great for raids/spam adds). Default: 3 hours if no number given.

Only group admins can use these commands.

## Customization
- **Permanent Bans**: In `main.py`, remove/comment out `await client.unban_chat_member(...)` lines.
- **Delays**: Adjust `random.uniform(2, 5)` for slower/faster actions (to avoid rate limits).
- **Run in Background**: Use `nohup`, `screen`, or a VPS (e.g., Heroku, Render).

## Notes
- Rate limits: The bot handles Telegram's FloodWaits automatically and resumes.
- Runs as a bot with full access – use responsibly.
- Use mutliple bots if you keep getting FloodWaits

## End
    Thank you to everyone for making these past 2 years of Dres awesome we love all of you and thought we would just release this quick little side project as a thanks so thanks from the entire Dres team. 


