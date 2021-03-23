import eventtig.process
import argparse
import os


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="subparser_name")

    foo_parser = subparsers.add_parser('build')
    foo_parser.add_argument('source')
    foo_parser.add_argument("--sqlite", help="Location of SQLite file")

    args = parser.parse_args()

    if args.subparser_name == 'build':

        if not args.sqlite:
            print("You must specify one of the build options when running build.")
            exit(-1)

        eventtig.process.go(args.source, os.path.join(args.source, 'eventtig.yaml'), args)

if __name__ == "__main__":
    main()
