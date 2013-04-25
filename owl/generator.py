# -*- coding: utf-8 -*-
""" The generator creating the output HTML

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
import shutil
import datetime

import jinja2
import markdown2

from owl.log_handler import LOGGER as logger


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
        logger.debug(
            'Generating HTML for {}..'.format(markdown_file.source_file))

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
                    'destination_root_dir': markdown_file.destination_root_dir,
                    'markdown_html': markdown2.markdown(
                        text,
                        extras=['fenced-code-blocks', 'wiki-tables'])
                })
            file_handle.write(html.encode('utf-8'))

        logger.debug('Wrote {}'.format(markdown_file.destination_file))


def generate_index_page(markdown_files):
    """ Generate the index page

    :type markdown_files: list
    :param markdown_files: List of MarkdownFile objects to print to the index
    """
    logger.debug('Generating index page..')
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'templates')))
    template = env.get_template('index.html')

    markdown_metadata = []
    for markdown_file in markdown_files:
        markdown_metadata.append(markdown_file.metadata)

    index_path = os.path.join(markdown_file.destination_root_dir, 'index.html')
    with open(index_path, 'w') as file_handle:
        file_handle.write(template.render(
            {
                'markdown_metadata': markdown_metadata,
                'generation_timestamp': datetime.datetime.utcnow().strftime(
                    '%Y-%m-%d %H:%M')
            }))


def import_static_files(destination_root_dir):
    """ Import all static files to the HTML output dir

    :type destination_root_dir: str
    :param destination_root_dir: Destination folder for HTML pages
    """
    if os.path.exists(os.path.join(destination_root_dir, '_owl_static')):
        shutil.rmtree(
            os.path.join(destination_root_dir, '_owl_static'),
            ignore_errors=True)

    shutil.copytree(
        os.path.join(os.path.dirname(__file__), 'static'),
        os.path.join(destination_root_dir, '_owl_static'))
