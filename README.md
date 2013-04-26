# markdown-docs - Documentation generator for Markdown projects

markdown-docs is a documentation generator for projects using Markdown. The problem with having Markdown files spread around your project is that it is hard to get an overview of all your documentation. markdown-docs solves this by collecting all of your Markdown files into one browsable HTML hierarchy.

## Screenshot

![screenshot](https://raw.github.com/sebdah/markdown-docs/gh-pages/img/screenshot.png)

## Usage

### Browsing docs with the embedded web server

Run the following to fire up a local web server with your documentation

    cd your/project/path
    markdown-docs

or

    markdown-docs serve

Then point your browser to [http://localhost:5000/](http://localhost:5000/).

### Generating HTML output

    cd your/project/path
    markdown-docs generate --output ~/docs

If you do not set `--output` a temporary directory will be created for you.


## Installation

The easiest way is to install markdown-docs via `pip`

    pip install markdown-docs

## Features

- Quick overview of all project Markdown files
- Adding [Table of contents](http://pythonhosted.org/Markdown/extensions/toc.html)
- [Syntax highlighting](http://pythonhosted.org/Markdown/extensions/code_hilite.html)
- Reads title from [metadata](http://pythonhosted.org/Markdown/extensions/meta_data.html)
- Support for the [Markdown tables extension](http://pythonhosted.org/Markdown/extensions/tables.html)
- No Internet connection needed
- markdown-docs comes with an embedded web server for serving static HTML locally

### Metadata details

markdown-docs is looking for Markdown meta data. Currently markdown-docs is only taking the `Title` meta data attribute in consideration. Meta data in Markdown looks like this

    Title: Document title
    Date: 2013-04-25

    This is where my Markdown really starts

Using meta data in markdown-docs is optional. If the `Title` tag is there, markdown-docs will show that document title instead of the file name on the index page.

### Syntax highlighting

markdown-docs supports syntax highlighting via the `Markdown` module. You can define the programming language by adding `:::language` as in this example

    :::python
    print('This is highlighted as Python code')

More details can be found in the [module docs](http://pythonhosted.org/Markdown/extensions/code_hilite.html).

### Adding Table of contents

A table of contents will be automatically generated in the HTML output if markdown-docs finds a `[TOC]` tag anywhere in the Markdown.

    # Table of contents

    [TOC]

    # My header

    ## My subheader

Release information
-------------------

**0.2.0 (2013-04-26)**

- First public release

Author
------

This project is maintained by [Sebastian Dahlgren](http://www.sebastiandahlgren.se) ([GitHub](https://github.com/sebdah) | [Twitter](https://twitter.com/sebdah) | [LinkedIn](http://www.linkedin.com/in/sebastiandahlgren))

License
-------

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
