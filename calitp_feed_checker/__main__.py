import typer

from . import check_feeds


def main(
    yml_file=typer.Argument("agencies.yml", help="A yml file containing urls"),
    csv_file=typer.Option(None, help="A csv file (one url per line)"),
    url=typer.Option(None, help="URL to check instead of a file",),
    output=typer.Option(None, help="Path to a file to save output to."),
    verbose: bool = typer.Option(False, help="Print a result table to stdout"),
):
    check_feeds(
        yml_file=yml_file, csv_file=csv_file, url=url, output=output, verbose=verbose,
    )


typer.run(main)
