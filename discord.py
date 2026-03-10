import discord
import 
from discord.ext import commands
import sqlite3
import os

# 1. Setup the Database
def init_db():
    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            author TEXT,
            submitted_by TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 2. Bot Configuration
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')

# 3. Command: Add a Quote
@bot.command()
async def addquote(ctx, content: str, *, author: str = "Unknown"):
    """Usage: !addquote "The quote text" Author Name"""
    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO quotes (content, author, submitted_by) VALUES (?, ?, ?)',
        (content, author, str(ctx.author))
    )
    conn.commit()
    conn.close()
    await ctx.send(f"✅ Quote added by {author}!")

# 4. Command: Get a Random Quote
@bot.command()
async def quote(ctx):
    """Usage: !quote"""
    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT content, author FROM quotes ORDER BY RANDOM() LIMIT 1')
    row = cursor.fetchone()
    conn.close()

    if row:
        await ctx.send(f'> "{row[0]}"\n— **{row[1]}**')
    else:
        await ctx.send("The database is empty! Add some wisdom first.")

# 5. Run the Bot
# Replace 'YOUR_TOKEN_HERE' with your actual bot token from the Discord Developer Portal
bot.run(os.getenv('DISCORD_TOKEN'))