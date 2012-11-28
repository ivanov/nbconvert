import os
from converters.base import Converter
from converters.utils import cell_to_lines
from shutil import rmtree
import json


class ConverterNotebook(Converter):
    """
    A converter that is essentially a null-op.
    This exists so it can be subclassed
    for custom handlers of .ipynb files
    that create new .ipynb files.

    What distinguishes this from JSONWriter is that
    subclasses can specify what to do with each type of cell.

    Writes out a notebook file.

    """
    extension = 'ipynb'

    def __init__(self, infile, outbase, **kw):
        Converter.__init__(self, infile, **kw)
        self.outbase = outbase
        rmtree(self.files_dir)

    def convert(self):
        return unicode(json.dumps(json.loads(Converter.convert(self, ',')),
                                  indent=1, sort_keys=True))

    def optional_header(self):
        s = \
"""{
 "metadata": {
 "name": "%(name)s"
 },
 "nbformat": 3,
 "worksheets": [
 {
 "cells": [""" % {'name': os.path.basename(self.outbase)}
        return s.split('\n')

    def optional_footer(self):
        s = \
"""]
  }
 ]
}"""
        return s.split('\n')

    def render_heading(self, cell):
        return cell_to_lines(cell)

    def render_code(self, cell):
        return cell_to_lines(cell)

    def render_markdown(self, cell):
        return cell_to_lines(cell)

    def render_raw(self, cell):
        return cell_to_lines(cell)

    def render_pyout(self, output):
        return cell_to_lines(output)

    def render_pyerr(self, output):
        return cell_to_lines(output)

    def render_display_format_text(self, output):
        return [output.text]

    def render_display_format_html(self, output):
        return [output.html]

    def render_display_format_latex(self, output):
        return [output.latex]

    def render_display_format_json(self, output):
        return [output.json]

    def render_display_format_javascript(self, output):
        return [output.javascript]
