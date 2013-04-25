# -*- coding: utf-8 -*-
""" Class definition for a Markdown file """
import os


class MarkdownFile:
    """ Definition of a Markdown file """
    metadata = {}

    # Starting point for this indexing
    source_dir = None

    # Full path to the source markdown file
    source_file = None

    # Dir for the outputed HTML file
    destination_dir = None

    # Full path to the destination HTML file
    destination_file = None

    # Root output directory
    destination_root_dir = None

    # Relative path to the markdown source file (relative to source_dir)
    relative_source_file = None

    # Relative path to the HTML page (relative to destination_root_dir)
    relative_destination_file = None

    def __init__(self, source_file, source_dir, destination_root_dir):
        """ Constructor

        :type source_file: str
        :param source_file: Full path to the markdown file
        :type source_dir: str
        :param source_dir: Starting point for this indexing
        :type destination_root_dir: str
        :param destination_root_dir: Destination folder for HTML pages
        """
        self.source_file = source_file
        self.source_dir = source_dir
        self.destination_root_dir = destination_root_dir

        self.relative_source_file = self.source_file.replace(
            '{}/'.format(source_dir), '')

        self.destination_file = os.path.join(
            self.destination_root_dir, self.relative_source_file)
        self.destination_file = self.destination_file.rsplit('.', 1)[0]
        self.destination_file = '{}.html'.format(self.destination_file)

        self.destination_dir = os.path.dirname(self.destination_file)

        self.relative_destination_file = self.destination_file.replace(
            '{}/'.format(destination_root_dir), '')

        # Generate the metadata
        self.generate_metadata()

    def generate_metadata(self):
        """ Populate the metadata for this markdown object """
        self.metadata = {
            'title': os.path.basename(self.source_file),
            'url': self.relative_destination_file,
            'full_path': os.path.dirname(self.relative_destination_file),
            'short_path': self.shorten_path(
                os.path.dirname(self.relative_destination_file))
        }

    def get_metadata(self, attribute):
        """ Returns the attribute attribute from self.metadata

        :returns: str or None -- Returns the attribute
        """
        return self.metadata.get(attribute, None)

    def shorten_path(self, full_path, max_length=40):
        """ Takes a full path like/this/one and returns like/t/one

        The function will try to return as long paths as possible

        :type full_path: str
        :param full_path: Full path to shorten
        :type max_length: int
        :param max_length: Max length for the path
        :returns: str -- Short version of the path
        """
        if len(full_path) <= max_length:
            return full_path
        else:
            need_to_save = len(full_path) - max_length

        shortened_path = []
        for index, folder in enumerate(full_path.split('/')):
            if index == 0:
                shortened_path.append(folder)
                continue

            elif index+1 == len(full_path.split('/')):
                shortened_path.append(folder)
                continue

            else:
                if need_to_save > 0:
                    shortened_path.append(folder[0])
                    need_to_save = need_to_save - len(folder) + 1
                else:
                    shortened_path.append(folder)

        return '/'.join(shortened_path)
