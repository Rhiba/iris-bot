# iris-bot

Discord bot for personal server.

## Requirements:

* `python3`
* `sqlite3`

### Python packages:

* `discord`
* `sqlalchemy`
* `sqlalchemy_utils`
* `alembic`
* `pytz`

## Setup

1) Create a discord bot project on the discord website.
2) Create a new python file called `iris_bot/creds.py` with the following format:

    ```python
    CREDS = {
        "DISCORD_TOKEN": "your_token_here",
        "DATABASE_CONNECTION": "sqlite:///iris.db",
        "SQL_LOGGING": True,
        "KARMA_TIMEOUT_S": 120
    }
    ```

    where `your_token_here` comes from the Bot section of your discord bot project (Settings > Bot).

3) Create blank database by running: `sqlite3 iris.db "VACUUM;"`
4) Run `alembic upgrade head`
5) Manually insert first admin user into the `user` table by running

    ```
    $ sqlite3 iris.db
    sqlite> INSERT INTO user (uid,admin) VALUES (<USER_ID>,1);
    ```

    where `<USER_ID>` is your discord integer id. You can find this by
    enabling developer mode (User Settings > Appearance), then clicking on your
    user in Discord and selecting "Copy ID".

## Running

From the repository root, run

```
python -m iris_bot
```
