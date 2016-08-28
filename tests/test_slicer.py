import os
import sys
import unittest

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(file_path))

from src.slicer import MP3Slicer


class TestMP3Slices(unittest.TestCase):
    """
    Tests bad inputs to MP3Slicer class.
    """
    mp3_path = './data/test.mp3'
    srt_path = './data/test.srt'

    def test_missing_mp3(self):
        with self.assertRaises(FileNotFoundError):
            MP3Slicer('/non/existent/file', '/missing/file')

    def test_missing_srt(self):
        with self.assertRaises(FileNotFoundError):
            MP3Slicer(self.mp3_path, '/missing/file')

    def test_load(self):
        MP3Slicer(self.mp3_path, self.srt_path)


if __name__ == '__main__':
    unittest.main()