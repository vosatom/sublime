# Running math inline in ST
# Parts of code taken from other random plugins
import sublime
import sublime_plugin
from . import test_math

stylesheet = '''
    <style>
        div.phantom-arrow {
            border-top: 0.4rem solid transparent;
            border-left: 0.5rem solid color(var(--bluish) blend(var(--background) 30%));
            width: 0;
            height: 0;
        }
        div.phantom {
            padding: 0.4rem 0 0.4rem 0.7rem;
            margin: 0 0 0.2rem;
            border-radius: 0 0.2rem 0.2rem 0.2rem;
            background-color: color(var(--bluish) blend(var(--background) 30%));
        }
        .status-error div.phantom-arrow {
            border-left: 0.5rem solid color(var(--redish) blend(var(--background) 30%));
        }
        .status-error div.phantom {
            background-color: color(var(--redish) blend(var(--background) 30%));
        }
        div.phantom span.message {
            padding-right: 0.7rem;
        }
        div.phantom a {
            text-decoration: inherit;
        }
        div.phantom a.close {
            padding: 0.35rem 0.7rem 0.45rem 0.8rem;
            position: relative;
            bottom: 0.05rem;
            border-radius: 0 0.2rem 0.2rem 0;
            font-weight: bold;
        }
        html.dark div.phantom a.close {
            background-color: #00000018;
        }
        html.light div.phantom a.close {
            background-color: #ffffff18;
        }
    </style>
'''

template_error = '''
    <body id="inline-numbers" class="status-{state}">
        {stylesheet}
        <div class="phantom-arrow"></div>
        <div class="phantom">
            <span class="message">
                {result}
                <a class="close" href="close">''' + chr(0x00D7) + '''</a>
            </span>
        </div>
    </body>
'''

template_default = '''
    <body id="inline-numbers" class="status-{state}">
        {stylesheet}
        <div class="phantom-arrow"></div>
        <div class="phantom">
            <span class="message">
                <strong>Výsledek</strong> {result}
                <a class="close" href="close">''' + chr(0x00D7) + '''</a>
            </span>
        </div>
    </body>
'''


class SummarizeNumbersCommand(sublime_plugin.TextCommand):
  def get_number(self, val):
    try:
      val = int(val)
      return val
    except ValueError:
      return 0

  def on_phantom_close(self, href):
    if href == "close":
        self.view.erase_phantoms('sum_result')

  def print(self, html, sel, state):
    if state == 'error':
        body = template_error.format(result=str(html), stylesheet=stylesheet, state=state)
    else:
        body = template_default.format(result=str(html), stylesheet=stylesheet, state=state)
    self.view.add_phantom('sum_result', sel[-1], body, sublime.LAYOUT_BLOCK, self.on_phantom_close)

  def run(self, edit):
    self.view.erase_phantoms('sum_result')
    phantoms = []

    sum = 0
    count = 0
    selection_length = len(self.view.sel())

    if selection_length > 1:
        for region in self.view.sel():
          if not region.empty():
            s = self.view.substr(region)
            sum = sum + self.get_number(s)
            count = count + 1

        if count > 0:
          self.print(sum, self.view.sel())
    elif selection_length == 1:
        result = ""

        try:
            for region in self.view.sel():
              if not region.empty():
                s = self.view.substr(region)
                result = str(test_math.eval_expr(s))

            if len(result):
                self.print(result, self.view.sel(), 'default')
        except Exception as e:
            self.print(e, self.view.sel(), 'error')


# 1+1
# print(test_math.eval_expr("5+2"))
# print(test_math.eval_expr("C(10,2)"))
