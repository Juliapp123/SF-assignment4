import unittest

from bot.exts.fun.wordle import CORRECT, HALF_CORRECT, WRONG, check_words, get_dictonary


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
        
    def test_no_dictonary(self) -> None:
        """Test that no dictonary exists."""
        self.assertEqual(None, get_dictonary(123))
        self.assertEqual(None, get_dictonary(-1))
    
    # get dictionary seems to error rather tahn return None when is does not exist

if __name__ == "__main__":
    unittest.main()
