from pathlib import Path
from random import choice

from discord import Embed, Message
from discord.ext import commands

from bot.bot import Bot
from bot.constants import Colours, NEGATIVE_REPLIES

# Defining all words in the list of words as a global variable
words_file = Path("bot/resources/fun/big.txt").read_text().splitlines()
ALL_WORDS = (x.lower() for x in filter(lambda x: x.isalpha() and x[1::].islower(), words_file))

ALL_WORDS_DICT = {}

for word in ALL_WORDS:
    if len(word) in ALL_WORDS_DICT:
        ALL_WORDS_DICT[len(word)].add(word)
    else:
        ALL_WORDS_DICT[len(word)] = { word }

CORRECT = 2
HALF_CORRECT = 1
WRONG = 0

def check_words(guess: str, correct : str) -> tuple:
    """Given a guess and the correct word, returns an integer array detailing the colors of the guess."""
    out = []
    half_correct = {}
    for i in range(len(correct)):
        if correct[i] != guess[i]:
            if correct[i] in half_correct:
                half_correct[correct[i]] += 1
            else:
                half_correct[correct[i]] = 1

    for i in range(len(correct)):
        if correct[i] == guess[i]:
            out.append(CORRECT)
        elif guess[i] in half_correct and half_correct[guess[i]] > 0:
            half_correct[guess[i]] -= 1
            out.append(HALF_CORRECT)
        else:
            out.append(WRONG)

    return out

def get_dictonary(length : int) -> dict|None:
    """"Returns a dict of every word of that given length."""
    return ALL_WORDS_DICT.get(length, None)

class Wordle(commands.Cog):
    """Cog for the Wordle game."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def create_embed(guesses: list[str], correct : str, remaining : int) -> Embed:
        """
        Helper method that creates the embed where the game information is shown.

        This includes how many and which words the user has guessed so far,
        if the letters are in the correct spot or not or if they are included in the word.
        """
        embed = Embed(
            title="Wordle",
            color=Colours.python_blue,
        )

        out = ""
        for guess in guesses:
            colors = check_words(guess, correct)
            for i in range(len(correct)):
                if colors[i] == CORRECT:
                    out += f"[1;32m{guess[i]}[0m "
                elif colors[i] == HALF_CORRECT:
                    out += f"[1;33m{guess[i]}[0m "
                else:
                    out += f"[1;0m{guess[i]}[0m "
            out += "\n"

        out += (("[1;0m☐[0m " * len(correct)) + "\n") * remaining

        embed.add_field(
            name="",
            value=f"```ansi\n{out}\n```"
        )

        return embed

    @commands.command()
    async def wordle(
            self,
            ctx: commands.Context,
            length: int = 5,
            tries: int = 6,
    ) -> None:
        """Classic wordle game where you guess the word based on what letter where correct in the previous guesses."""
        # Filtering the list of all words depending on the configuration
        filtered_words = get_dictonary(length)
        #print(filtered_words)

        if filtered_words is None:
            filter_not_found_embed = Embed(
                title=choice(NEGATIVE_REPLIES),
                description="No words could be found that fit all filters specified.",
                color=Colours.soft_red,
            )
            await ctx.send(embed=filter_not_found_embed)
            return

        word = choice(tuple(filtered_words))
        # print("The word selected is", word)
        guesses = []

        def check(msg: Message) -> bool:
            return msg.author == ctx.author and msg.channel == ctx.channel

        original_message = await ctx.send(embed=Embed(
            title="Wordle",
            description="Loading game...",
            color=Colours.soft_green
        ))

        # Game loop
        while True:
            # Edit the message to the current state of the game
            await original_message.edit(embed=self.create_embed(guesses, word, tries))

            try:
                message = await self.bot.wait_for(
                    "message",
                    timeout=60.0,
                    check=check
                )
            except TimeoutError:
                timeout_embed = Embed(
                    title="You lost",
                    description=f"Time's up! The correct word was `{word}`.",
                    color=Colours.soft_red,
                )
                await ctx.send(embed=timeout_embed)
                return

            # If the user enters a capital letter as their guess, it is automatically converted to a lowercase letter
            normalized_content = message.content.lower()

            if normalized_content == "/exit":
                letter_embed = Embed(
                    title="Exit",
                    description=f"You left the game, the word was {word}",
                    color=Colours.dark_green,
                )
                await ctx.send(embed=letter_embed, delete_after=4)
                return

            if normalized_content not in filtered_words:
                letter_embed = Embed(
                    title=choice(NEGATIVE_REPLIES),
                    description="You can only send valid words, try again!",
                    color=Colours.dark_green,
                )
                await ctx.send(embed=letter_embed, delete_after=4)
                continue

            # The user should only guess one letter per message
            if len(normalized_content) != len(word):
                letter_embed = Embed(
                    title=choice(NEGATIVE_REPLIES),
                    description=f"You can only send words of length {len(word)}, try again!",
                    color=Colours.dark_green,
                )
                await ctx.send(embed=letter_embed, delete_after=4)
                continue

            guesses.append(normalized_content)
            tries -= 1
            if word == normalized_content:
                break

            if tries <= 0:
                losing_embed = Embed(
                    title="You lost.",
                    description=f"The word was `{word}`.",
                    color=Colours.soft_red,
                )
                await original_message.edit(embed=self.create_embed(guesses, word, tries))
                await ctx.send(embed=losing_embed)
                return

        # The loop exited meaning that the user has guessed the word
        await original_message.edit(embed=self.create_embed(guesses, word, tries))
        win_embed = Embed(
            title="You won!",
            description=f"The word was `{word}`.",
            color=Colours.grass_green
        )
        await ctx.send(embed=win_embed)


async def setup(bot: Bot) -> None:
    """Load the Wordle cog."""
    await bot.add_cog(Wordle(bot))
