# -*- coding: utf-8 -*-
""" Embedded web server implementation

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
from flask import Flask, redirect, send_from_directory


def run_webserver(destination_root_dir):
    """ Run a local """
    destination_root_dir = destination_root_dir
    if destination_root_dir.startswith('/'):
        destination_root_dir = destination_root_dir[1:]

    if destination_root_dir.endswith('/'):
        destination_root_dir = destination_root_dir[:-1]

    app = Flask(__name__)
    @app.route('/<path:filename>')
    def index(filename='index.html'):
        if filename.startswith(destination_root_dir):
            filename = filename.replace('{}/'.format(destination_root_dir), '')
            return redirect('/{}'.format(filename))
        return send_from_directory('/{}'.format(destination_root_dir), filename)

    app.run()