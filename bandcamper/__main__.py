from argparse import ArgumentParser

from bandcamper import Bandcamper


def main():
    parser = ArgumentParser(description="Download tracks and albums from Bandcamp")
    parser.add_argument(
        "urls",
        nargs="*",
        metavar="URL",
        help="URLs/artists subdomains to download songs from.",
    )
    parser.add_argument(
        "-F",
        "--file",
        dest="files",
        metavar="<file>",
        default=[],
        action="append",
        help="Download from URLs/artists subdomains listed on file. This option can be used multiple times.",
    )
    audio_format_options = parser.add_mutually_exclusive_group()
    audio_format_options.add_argument(
        "-f",
        "--format",
        dest="download_formats",
        default=["mp3-320", "flac"],
        action="append",
        choices=["aac-hi", "aiff-lossless", "alac", "flac", "mp3-128", "mp3-320", "mp3-v0", "vorbis", "wav"],
        help="Preferred audio formats to download."
    )
    audio_format_options.add_argument(
        "--all-formats",
        dest="download_formats",
        action="store_const",
        const=["aac-hi", "aiff-lossless", "alac", "flac", "mp3-128", "mp3-320", "mp3-v0", "vorbis", "wav"],
        help="Download all available audio formats."
    )
    parser.add_argument(
        "-d",
        "--destination",
        default=".",
        help="Base destination folder for downloaded files. Defaults to current folder.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="{artist_name}/{album_title}/{track_title}.{ext}",
        help="Output filename template. See the 'Output Template' section of the README for all the info.",
    )
    parser.add_argument(
        "-i",
        "--ignore-errors",
        action="store_true",
        help="Don't end the program in case of any (predictable) error; show warning instead.",
    )
    verbosity_options = parser.add_mutually_exclusive_group()
    verbosity_options.add_argument(
        "-q",
        "--quiet",
        action="count",
        default=0,
        help="Run bandcamper with less output. Use this flag 3 times to completely disable any output.",
    )
    verbosity_options.add_argument(
        "-v",
        "--verbose",
        dest="quiet",
        action="store_const",
        const=-1,
        help="Run bandcamper with more verbose output.",
    )
    parser.add_argument(
        "--no-colors",
        dest="colored",
        action="store_false",
        help="Disable colored output.",
    )

    args = vars(parser.parse_args())
    download_formats = args.pop("download_formats")
    urls = args.pop("urls")
    bandcamper = Bandcamper(args.pop("destination"), *urls, **args)
    if not bandcamper.urls:
        bandcamper.screamer.error(
            "You must give at least one URL/artist subdomain to download",
            force_error=True,
        )

    bandcamper.download_all(download_formats)


if __name__ == "__main__":
    try:
        main()
    except RuntimeError:
        exit(1)
