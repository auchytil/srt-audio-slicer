# slicer.py

from pydub import AudioSegment
import pysrt


class MP3Slicer:
    """
    Class that takes care of mp3 slicing.
    """
    def __init__(self, mp3_path: str, srt_path: str):
        """
        Initializes MP3 slicer

        :param mp3_path: path to mp3 file
        :param srt_path: path to srt file
        """
        self.mp3 = None
        self.srt = None
        self.load_files(mp3_path, srt_path)

    def load_files(self, mp3_path: str, srt_path: str):
        """
        Loads files into MP3Slicer

        :param mp3_path: path to mp3 file
        :param srt_path: path to srt file
        """
        self.mp3 = AudioSegment.from_mp3(mp3_path)
        self.srt = pysrt.open(srt_path)

    def _save_mp3_part(self, start: int, end: int, file_name: str):
        """
        Saves part of the mp3 to single file

        :param start: starting millisecond
        :param end: ending millisecond
        :param file_name: output file name
        :return:
        """
        part = self.mp3[start:end]
        part.export(file_name)

    @staticmethod
    def _save_srt_part(sub: pysrt.SubRipItem, file_name: str):
        """
        Saves a subtitle into single file

        :param sub: subtitle object
        :param file_name: file name
        :return:
        """
        start_new = pysrt.SubRipTime.from_ordinal(0)
        end_new = pysrt.SubRipTime.from_ordinal(sub.end.ordinal - sub.start.ordinal)
        with open(file_name, 'w') as f:
            f.write("1\n")
            f.write("{0} --> {1}\n".format(start_new, end_new))
            f.write(sub.text)

    def slice(self, outdir='.', prefix=''):
        """
        Slices mp3 file into multiple files.

        :param outdir: path to directory where will the mp3s be stored
        :param prefix: file prefix
        :return:
        """
        for sub in self.srt.data:
            file_name_base = '{0}/{1}{2}'.format(outdir, prefix, sub.text.replace('/', '_'))
            file_mp3 = '{0}.mp3'.format(file_name_base)
            file_srt = '{0}.srt'.format(file_name_base)

            self._save_mp3_part(sub.start.ordinal, sub.end.ordinal, file_mp3)
            MP3Slicer._save_srt_part(sub, file_srt)
