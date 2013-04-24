#!/usr/bin/env python
""" Owl markdown documentation reader """

import os
import sys
import tempfile
import markdown
import argparse


def main():
    """ Main function """
    parser = argparse.ArgumentParser(
        description='Owl markdown documentation generator')
    parser.add_argument('-d', '--directory',
        help='Root directory to parse from (default: current dir)')
    parser.add_argument('-o', '--output',
        help='Output directory to store HTML file in (default: )')
    args = parser.parse_args()

    if args.directory:
        root_dir = os.path.expandvars(os.path.expanduser(args.directory))

        if not os.path.exists(root_dir):
            print('{} does not exist'.format(root_dir))
            sys.exit(1)
        elif not os.path.isdir(root_dir):
            print('{} is not a directory'.format(root_dir))
            sys.exit(1)
    else:
        root_dir = os.path.realpath(os.path.curdir)

    if args.output:
        output_dir = os.path.expandvars(os.path.expanduser(args.output))

        try:
            os.makedirs(output_dir)
        except OSError as (errno, errmsg):
            if errno == 17:
                # Code 17 == File exists
                pass
            else:
                print('Error creating {}: {}'.format(output_dir, errmsg))
                sys.exit(1)
    else:
        output_dir = tempfile.mkdtemp(prefix='owl')

    md_files = find_markdown_files(root_dir)
    for md_file in md_files:
        generate_html(root_dir, md_file, output_dir)


def generate_html(root_dir, input_file, output_dir, output_format='html5'):
    """ Generate HTML from a given markdown file

    :type root_dir: str
    :param root_dir: Starting path
    :type input_file: str
    :param input_file: Path to the Markdown file
    :type output_dir: str
    :param output_dir: Path to the output dir
    :type output_format: str
    :param output_format:
        Markdown output format, see
        http://pythonhosted.org/Markdown/reference.html
    """
    print('Generating HTML for {}..'.format(input_file))

    input_file_dir = os.path.dirname(input_file).replace(
        '{}/'.format(root_dir), '')
    output_dir = os.path.join(output_dir, input_file_dir)
    output_dir = output_dir.replace('/./', '/')
    output_filename = os.path.basename(input_file).rsplit('.', 1)[0]
    output_filename = '{}.html'.format(output_filename)

    # Ensure that the output directory exists
    try:
        os.makedirs(output_dir)
    except OSError as (errno, errmsg):
        if errno == 17:
            # Code 17 == File exists
            pass
        else:
            raise

    with open(input_file, 'r') as file_handle:
        text = file_handle.read()

    with open(os.path.join(output_dir, output_filename), 'w') as file_handle:
        file_handle.write(markdown.markdown(text, output_format='html5'))

    print('Wrote {}'.format(os.path.join(output_dir, output_filename)))


def find_markdown_files(root_dir='.'):
    """ Returns a list of all Markdown files

    :type root_dir: str
    :param root_dir: Where should the Owl start looking?
    """
    md_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            try:
                _, extension = filename.rsplit('.', 1)
                if extension in ['md', 'mdown', 'markdown']:
                    md_files.append('{}/{}'.format(dirpath, filename))
            except ValueError:
                pass

    return md_files


if __name__ == '__main__':
    main()
