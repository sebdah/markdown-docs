#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Owl markdown documentation reader """

import os
import sys
import shutil
import tempfile
import argparse

import jinja2
import markdown2


class MarkdownFile:
    """ Definition of a Markdown file """
    metadata = {}

    # Starting point for this indexing
    source_dir = None

    # Full path to the source markdown file
    source_file = None

    # Root output directory
    destination_dir = None

    # Full path to the destination HTML file
    destination_file = None

    # Relative path to the markdown source file (relative to source_dir)
    relative_source_file = None

    # Relative path to the HTML page (relative to destination_dir)
    relative_destination_file = None

    def __init__(self, source_file, source_dir, destination_dir):
        """ Constructor

        :type source_file: str
        :param source_file: Full path to the markdown file
        :type source_dir: str
        :param source_dir: Starting point for this indexing
        :type destination_dir: str
        :param destination_dir: Destination folder for HTML pages
        """
        self.source_file = source_file
        self.source_dir = source_dir
        self.destination_dir = destination_dir

        self.relative_source_file = self.source_file.replace(
            '{}/'.format(source_dir), '')

        self.destination_file = os.path.join(
            self.destination_dir, self.relative_source_file)
        self.destination_file = self.destination_file.rsplit('.', 1)[0]
        self.destination_file = '{}.html'.format(self.destination_file)

        self.relative_destination_file = self.destination_file.replace(
            '{}/'.format(destination_dir), '')

        # Generate the metadata
        self.generate_metadata()

    def generate_metadata(self):
        """ Populate the metadata for this markdown object """
        self.metadata = {
            'title': os.path.basename(self.source_file),
            'url': self.relative_destination_file,
            'path': os.path.dirname(self.relative_destination_file)
        }

    def get_metadata(self, attribute):
        """ Returns the attribute attribute from self.metadata

        :returns: str or None -- Returns the attribute
        """
        return self.metadata.get(attribute, None)


def main():
    """ Main function """
    parser = argparse.ArgumentParser(
        description='Owl markdown documentation generator')
    parser.add_argument('-d', '--directory',
        help='Root directory to parse from (default: current dir)')
    parser.add_argument('-o', '--output',
        help='Output directory to store HTML files in')
    args = parser.parse_args()

    if args.directory:
        source_dir = os.path.expandvars(os.path.expanduser(args.directory))

        if not os.path.exists(source_dir):
            print('{} does not exist'.format(source_dir))
            sys.exit(1)
        elif not os.path.isdir(source_dir):
            print('{} is not a directory'.format(source_dir))
            sys.exit(1)
    else:
        source_dir = os.path.realpath(os.path.curdir)

    if args.output:
        destination_dir = os.path.expandvars(os.path.expanduser(args.output))

        try:
            os.makedirs(destination_dir)
        except OSError as (errno, errmsg):
            if errno == 17:
                # Code 17 == File exists
                pass
            else:
                print('Error creating {}: {}'.format(destination_dir, errmsg))
                sys.exit(1)
    else:
        destination_dir = tempfile.mkdtemp(prefix='owl')

    markdown_files = find_markdown_files(source_dir, destination_dir)
    generate_html(markdown_files)
    generate_index_page(markdown_files)
    import_static_files(destination_dir)


def find_markdown_files(source_dir, destination_dir):
    """ Returns a list of all Markdown files

    :type source_dir: str
    :param source_dir: Where should the Owl start looking?
    :type destination_dir: str
    :param destination_dir: Path to the output dir
    :returns: list -- List of MarkdownFile objects
    """
    md_files_dict = {}
    for dirpath, _, filenames in os.walk(source_dir):
        for filename in filenames:
            try:
                _, extension = filename.rsplit('.', 1)
                if extension in ['md', 'mdown', 'markdown']:
                    md_file = MarkdownFile(
                        os.path.join(dirpath, filename),
                        source_dir,
                        destination_dir)
                    md_files_dict[os.path.join(dirpath, filename)] = md_file

            except ValueError:
                pass

    markdown_files = []
    for md_file in sorted(md_files_dict):
        markdown_files.append(md_files_dict[md_file])
    return markdown_files


def generate_html(markdown_files):
    """ Generate HTML from a given markdown file

    :type markdown_files: [MarkdownFile]
    :param markdown_files: List of MarkdownFile object
    """
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'templates')))
    template = env.get_template('markdown-template.html')

    for markdown_file in markdown_files:
        print('Generating HTML for {}..'.format(markdown_file.source_file))

        # Ensure that the output directory exists
        try:
            os.makedirs(markdown_file.destination_dir)
        except OSError as (errno, errmsg):
            if errno == 17:
                # Code 17 == File exists
                pass
            else:
                raise

        with open(markdown_file.source_file, 'r') as file_handle:
            text = file_handle.read()

        with open(markdown_file.destination_file, 'w') as file_handle:
            html = template.render(
                {
                    'title': markdown_file.get_metadata('title'),
                    'destination_dir': markdown_file.destination_dir,
                    'markdown_html': markdown2.markdown(
                        text,
                        extras=['fenced-code-blocks'])
                })

            file_handle.write(html)

        print('Wrote {}'.format(markdown_file.destination_file))


def generate_index_page(markdown_files):
    """ Generate the index page

    :type markdown_files: list
    :param markdown_files: List of MarkdownFile objects to print to the index
    """
    print('Generating index page..')
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'templates')))
    template = env.get_template('index.html')

    markdown_metadata = []
    for markdown_file in markdown_files:
        markdown_metadata.append(markdown_file.metadata)

    index_path = os.path.join(markdown_file.destination_dir, 'index.html')
    with open(index_path, 'w') as file_handle:
        file_handle.write(template.render(
            {
                'markdown_metadata': markdown_metadata
            }))


def import_static_files(destination_dir):
    """ Import all static files to the HTML output dir

    :type destination_dir: str
    :param destination_dir: Destination folder for HTML pages
    """
    if os.path.exists(os.path.join(destination_dir, '_owl_static')):
        shutil.rmtree(
            os.path.join(destination_dir, '_owl_static'),
            ignore_errors=True)

    shutil.copytree(
        os.path.join(os.path.dirname(__file__), 'static'),
        os.path.join(destination_dir, '_owl_static'))


if __name__ == '__main__':
    main()
