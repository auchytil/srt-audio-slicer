import argparse
import os
import slicer


def slice_all(list_path: str, outdir='.'):
    """
    Slices all of the mp3s in the list

    :param list_path: path to the list
    :param outdir: output directory
    :return:
    """
    if not os.path.isfile(list_path):
        raise FileNotFoundError("List file does not exist")
    else:
        index=0
        with open(list_path, 'r') as f:
            for line in f:
                mp3, srt = line.split()
                mp3_slicer = slicer.MP3Slicer(mp3, srt)
                mp3_slicer.slice(prefix=str(index))
                index += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MP3 slicer')
    parser.add_argument('--mp3', type=str, help='MP3 file')
    parser.add_argument('--srt', type=str, help='SRT file')
    parser.add_argument('--list', type=str, help='List od MP3 and SRT files')
    parser.add_argument('--outdir', type=str, help='Output directory to store files', default='.')
    args = parser.parse_args()

    if args.list:
        if args.mp3 or args.srt:
            raise ValueError("Illegal combination of parameters")
        else:
            slice_all(args.list, outdir=args.outdir)

    elif args.mp3 and args.srt:
        if args.list:
            raise ValueError("Illegal combination of parameters")
        else:
            mp3slicer = slicer.MP3Slicer(args.mp3, args.srt)
            mp3slicer.slice(outdir=args.outdir)

    else:
        raise ValueError("Missing parameters")
