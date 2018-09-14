import re
import subprocess

from deoplete.util import globruntime
from .base import Base


class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'fish'
        self.mark = '[fish]'
        self.filetypes = ['fish']
        self.input_pattern = '[^. \t0-9]\.\w*'
        self.rank = 500
        self.__executable_fish = self.vim.call('executable', 'fish')

    def get_complete_position(self, context):
        m = re.search(r'\S+$', context['input'])
        return m.start() if m else -1

    def gather_candidates(self, context):
        globs = globruntime(self.vim.options['runtimepath'], 'bin/complete.fish')

        if not self.__executable_fish or not globs or not context['input']:
            return []

        try:
            output = subprocess.check_output(
                ['fish', globs[0], context['input']], timeout=0.5)
        except subprocess.SubprocessError:
            return []

        lines = [line.decode(context['encoding']).split("\t")
                 for line in output.splitlines()]

        result = []

        for line in lines:
            if len(line) > 1:
                result.append({'word': line[0], 'menu': line[1]})
            else:
                result.append({'word': line[0]})

        return result
