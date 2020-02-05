# iris-bot
Discord bot for personal server.

## Requirements:
`python3`
`sqlite3`

### Python packages:
`discord.py`
`sqlalchemy`
`sqlalchemy_utils`
`alembic`
`pytz`

## Setup
1) Create a discord bot project on the discord website.
2) Create a new python file called `creds.py` with the following format:
    ```
        CREDS = {
            "DISCORD_TOKEN": "your_token_here",
            "DATABASE_CONNECTION": "sqlite:///iris.db",
            "SQL_LOGGING": True,
            "KARMA_TIMEOUT_S": 120
        }
    ```
    Where `your_token_here` comes from your discord bot project.
3) Create blank database by running: `sqlite3 iris.db "VACUUM;"`
4) Run `alembic upgrade head`
5) Manually insert first admin user into the `user` table by first running `sqlite3 iris.db`, then in the sqlite3 command line, running `INSERT INTO user (uid,admin) VALUES (your_integer_id,1);` where `your_integer_id` is your discord user id (gotten by right clicking on your user in discord and clicking `Copy Id`, make sure developer mode is enabled in Appearance settings for this option to be available).
