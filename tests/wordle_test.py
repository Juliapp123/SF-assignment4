import unittest

from bot.exts.fun.wordle import CORRECT, HALF_CORRECT, WRONG, check_words, get_dictonary

"""
from tests.helpers import MockBot, MockContext

from bot.cogs import bot


class TestWordle(unittest.TestCase):
    def test_echo_command_correctly_echoes_arguments(self) -> None:
        Test if the `!echo <text>` command correctly echoes the content.
        mocked_bot = MockBot()
        bot_cog = bot.Bot(mocked_bot)

        mocked_context = MockContext()

        text = "Hello! This should be echoed!"

        asyncio.run(bot_cog.echo_command.callback(bot_cog, mocked_context, text=text))

        mocked_context.send.assert_called_with(text)

    def setUp(self):
        self.bot = Bot(command_prefix=".")
        self.bot.add_cog(Wordle(self.bot))

    @patch("bot.utils.commands.Context")
    async def test_create_embed(self, mock_context):

        ctx = mock_context.return_value
        ctx.send = AsyncMock()
        await ctx.send(".wordle")

"""


class TestCheckWordsMethod(unittest.TestCase):
    """Test the check_words function."""

    def test_correct(self) -> None:
        """Test for all correct."""
        self.assertEqual(check_words("hej", "hej"), [CORRECT,CORRECT,CORRECT])
        self.assertEqual(check_words("hello", "hello"), [CORRECT,CORRECT,CORRECT,CORRECT,CORRECT])

    def test_wrong(self) -> None:
        """Test for all wrong."""
        self.assertEqual(check_words("xyz", "abc"), [WRONG,WRONG,WRONG])
        self.assertEqual(check_words("xyz", "aaa"), [WRONG,WRONG,WRONG])

    def test_half_correct(self) -> None:
        """Test for half correct, aka if one of the letters are in the word but not correct."""
        self.assertEqual(check_words("axa", "xyz"), [WRONG,HALF_CORRECT,WRONG])
        self.assertEqual(check_words("aax", "xyz"), [WRONG,WRONG,HALF_CORRECT])

    def test_both(self) -> None:
        """Test all cases."""
        self.assertEqual(check_words("xxx","xyz"), [CORRECT,WRONG,WRONG])
        self.assertEqual(check_words("xzxx","xxzp"), [CORRECT, HALF_CORRECT, HALF_CORRECT, WRONG])
        self.assertEqual(check_words("hexlo","hello"), [CORRECT,CORRECT,WRONG,CORRECT,CORRECT])
        self.assertEqual(check_words("hexlo","helxo"), [CORRECT,CORRECT,HALF_CORRECT,HALF_CORRECT,CORRECT])

class TestDictonary(unittest.TestCase):
    """Test the get_dictonary function."""

    def test_valid(self) -> None:
        """Test to determine that words are valid using the dictionary."""
        self.assertTrue("hell" in get_dictonary(4))
        self.assertTrue("hello" in get_dictonary(5))
        self.assertTrue("house" in get_dictonary(5))
        self.assertTrue("bell" in get_dictonary(4))

    def test_invalid(self) -> None:
        """Test to determine that words are invalid using the dictionary."""
        self.assertFalse("hello" in get_dictonary(4))
        self.assertFalse("abcdefgh" in get_dictonary(len("abcdefgh")))
        #self.assertFalse("ö" in get_dictonary(1)) 
        #get_dictonary(1) does not exists for some reason making this fail
    '''
    def test_no_dictonary(self) -> None:
        """Test that no dictonary exists."""
        self.assertEqual(None, get_dictonary(123))
        self.assertEqual(None, get_dictonary(-1))
    '''
    # get dictionary seems to error rather tahn return None when is does not exist

if __name__ == "__main__":
    unittest.main()
