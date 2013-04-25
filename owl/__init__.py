#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Owl markdown documentation reader

APACHE LICENSE 2.0
Copyright 2013 Sebastian Dahlgren

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import sys
import shutil
import tempfile
import argparse

import owl.generator
import owl.web_server
from owl.markdown_file import MarkdownFile
from owl.log_handler import LOGGER as logger


def main():
    """ Main function """
    parser = argparse.ArgumentParser(
        description='Owl markdown documentation generator')
    parser.add_argument('-d', '--directory',
        help='Root directory to parse from (default: current dir)')
    parser.add_argument('-o', '--output',
        help='Output directory to store HTML files in')
    parser.add_argument('generate',
        nargs='?',
        default=False,
        help='Generate HTML')
    parser.add_argument('serve',
        nargs='?',
        default=True,
        help='Start a local web server to serve the documentation')
    args = parser.parse_args()

    if args.directory:
        source_dir = os.path.expandvars(os.path.expanduser(args.directory))

        if not os.path.exists(source_dir):
            logger.error('{} does not exist'.format(source_dir))
            sys.exit(1)
        elif not os.path.isdir(source_dir):
            logger.error('{} is not a directory'.format(source_dir))
            sys.exit(1)
    else:
        source_dir = os.path.realpath(os.path.curdir)

    temp_dir_used = False
    if args.output:
        destination_root_dir = os.path.expandvars(
            os.path.expanduser(args.output))

        try:
            os.makedirs(destination_root_dir)
        except OSError as (errno, errmsg):
            if errno == 17:
                # Code 17 == File exists
                pass
            else:
                logger.error('Error creating {}: {}'.format(
                    destination_root_dir, errmsg))
                sys.exit(1)
    else:
        destination_root_dir = tempfile.mkdtemp(prefix='owl')
        logger.debug('Using temporary folder: {}'.format(destination_root_dir))
        if not args.generate:
            temp_dir_used = True

    try:
        markdown_files = find_markdown_files(source_dir, destination_root_dir)
        logger.info('Generating documentation for {:d} markdown files..'.format(
            len(markdown_files)))
        owl.generator.generate_html(markdown_files)
        owl.generator.generate_index_page(markdown_files)
        owl.generator.import_static_files(destination_root_dir)
        logger.info('Done with documentation generation!')

        if args.serve and not args.generate:
            owl.web_server.run_webserver(destination_root_dir)
        if args.generate:
            logger.info('HTML output can be found in {}'.format(
                destination_root_dir))

    finally:
        if temp_dir_used:
            logger.debug('Removing temporary folder: {}'.format(
                destination_root_dir))
            shutil.rmtree(destination_root_dir)


def find_markdown_files(source_dir, destination_root_dir):
    """ Returns a list of all Markdown files

    :type source_dir: str
    :param source_dir: Where should the Owl start looking?
    :type destination_root_dir: str
    :param destination_root_dir: Path to the output dir
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
                        destination_root_dir)
                    md_files_dict[os.path.join(dirpath, filename)] = md_file

            except ValueError:
                pass

    markdown_files = []
    for md_file in sorted(md_files_dict):
        markdown_files.append(md_files_dict[md_file])
    return markdown_files
