import json
import typer

from . import check_feeds


def main(
    yml_file=typer.Argument("agencies.yml", help="A yml file containing urls"),
    csv_file=typer.Option(None, help="A csv file (one url per line)"),
    url=typer.Option(
        None,
        help="URL to check instead of a file",
    ),
    output=typer.Option(None, help="Path to a file to save output to."),
):
    results = check_feeds(yml_file=yml_file, csv_file=csv_file, url=url)

    missing = []
    for url, data in results.items():
        statuses = [
            data["transitfeeds"]["status"],
            data["transitland"]["status"],
        ]
        if "present" not in statuses:
            missing.append(url)

    if missing:
        print(f"Unable to find {len(missing)}/{len(results)} urls:")
        for url in missing:
            print(url)
    else:
        matched = len(results) - len(missing)
        print(f"Found {matched}/{len(results)} urls were found")

    if output:
        with open(output, "w") as f:
            f.write(json.dumps(results, indent=4))
            print(f"Results saved to {output}")


typer.run(main)
