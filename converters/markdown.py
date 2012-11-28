from converters.base import Converter
from converters.utils import highlight, remove_ansi
from IPython.utils.text import indent


class ConverterMarkdown(Converter):
    extension = 'md'

    def __init__(self, infile, highlight_source=True, show_prompts=False,
                 inline_prompt=False, **kw):
        super(ConverterMarkdown, self).__init__(infile, **kw)
        self.highlight_source = highlight_source
        self.show_prompts = show_prompts
        self.inline_prompt = inline_prompt

    def render_heading(self, cell):
        return ['{0} {1}'.format('#' * cell.level, cell.source), '']

    def render_code(self, cell):
        if not cell.input:
            return []
        lines = []
        n = self._get_prompt_number(cell)
        if self.show_prompts and not self.inline_prompt:
            lines.extend(['*In[%s]:*' % n, ''])
        if self.show_prompts and self.inline_prompt:
            prompt = 'In[%s]: ' % n
            input_lines = cell.input.split('\n')
            src = (prompt + input_lines[0] + '\n' +
                   indent('\n'.join(input_lines[1:]), nspaces=len(prompt)))
        else:
            src = cell.input
        src = highlight(src) if self.highlight_source else indent(src)
        lines.extend([src, ''])
        if cell.outputs and self.show_prompts and not self.inline_prompt:
            lines.extend(['*Out[%s]:*' % n, ''])
        for output in cell.outputs:
            conv_fn = self.dispatch(output.output_type)
            lines.extend(conv_fn(output))

        #lines.append('----')
        lines.append('')
        return lines

    def render_markdown(self, cell):
        return [cell.source, '']

    def render_raw(self, cell):
        if self.raw_as_verbatim:
            return [indent(cell.source), '']
        else:
            return [cell.source, '']

    def render_pyout(self, output):
        lines = []

        ## if 'text' in output:
        ##     lines.extend(['*Out[%s]:*' % self._get_prompt_number(cell), ''])

        # output is a dictionary like object with type as a key
        if 'latex' in output:
            pass

        if 'text' in output:
            lines.extend(['<pre>', indent(output.text), '</pre>'])

        lines.append('')
        return lines

    def render_pyerr(self, output):
        # Note: a traceback is a *list* of frames.
        return [indent(remove_ansi('\n'.join(output.traceback))), '']

    def _img_lines(self, img_file):
        return ['', '![](%s)' % img_file, '']

    def render_display_format_text(self, output):
        return [indent(output.text)]

    def _unknown_lines(self, data):
        return ['Warning: Unknown cell', data]

    def render_display_format_html(self, output):
        return [output.html]

    def render_display_format_latex(self, output):
        return ['LaTeX::', indent(output.latex)]

    def render_display_format_json(self, output):
        return ['JSON:', indent(output.json)]

    def render_display_format_javascript(self, output):
        return ['JavaScript:', indent(output.javascript)]
