from dataclasses import dataclass

import discord


@dataclass
class FileResponse:
    content: str
    file: discord.File
