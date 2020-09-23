import sublime
import sublime_plugin

# Plugin to fix characters from PDF
#
# They say it's fast
# https://stackoverflow.com/questions/3411771/best-way-to-replace-multiple-characters-in-a-string
class FixCharactersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        for region in selection:
            region_text = self.view.substr(region)
            randomized_text = self.randomize_text(region_text)
            self.view.replace(edit, region, randomized_text)

    def randomize_text(self, text):
        # ˇ e

        text = text.replace('ˇz', 'ž')
        text = text.replace('ˇs', 'š')
        text = text.replace('ˇc', 'č')
        text = text.replace('ˇr', 'ř')
        text = text.replace('ˇd', 'ď')
        text = text.replace('ˇt', 'ť')
        text = text.replace('ˇn', 'ň')
        text = text.replace('´a', 'á')
        text = text.replace('´ı', 'í')
        text = text.replace('ˇe', 'ě')
        text = text.replace('´e', 'é')
        text = text.replace('´o', 'ó')
        text = text.replace('´y', 'ý')
        text = text.replace('ˇr', 'ř')
        text = text.replace('t’', 'ť')
        text = text.replace('ˇ o', 'o')

        text = text.replace('∈', '\\in')
        text = text.replace('λ', '\\lambda ')
        text = text.replace('...', '\\dots')
        text = text.replace(' ˚u', 'ů')
        text = text.replace(' ˇ c', 'č')
        text = text.replace(' ˇ e', 'ě')
        text = text.replace('ˇ', '')
        text = text.replace('→', '\\to')

        return text



