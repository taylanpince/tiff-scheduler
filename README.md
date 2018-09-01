# TIFF Scheduler

Schedule creator for Toronto International Film Festival. It will fetch film schedules from TIFF.net and create a ticket calendar recommendation for you. It will make sure that films don't overlap, and it can optimize for daytime or evening screenings.

## Usage

Run it using Python 3 with the provided command line options:

    python tiff.py --film-urls-file-path=2018_films --optimize-for=evening

You can provide a sample text file that contains a TIFF.net film URL on every line, or a list of film URLs in the command line, separated by commas.

`optimize-for` option can take `day` or `evening` as an option.

## Credits

Built by [Hipo](https://hipolabs.com), for the love of film.
