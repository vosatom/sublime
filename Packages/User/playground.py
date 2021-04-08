# Plugin Playground
import sublime
import sublime_plugin


from threading import Timer


def debounce(wait):
    """ Decorator that will postpone a functions
        execution until after wait seconds
        have elapsed since the last time it was invoked. """
    def decorator(fn):
        def debounced(*args, **kwargs):
            def call_it():
                fn(*args, **kwargs)
            try:
                debounced.t.cancel()
            except(AttributeError):
                pass
            debounced.t = Timer(wait, call_it)
            debounced.t.start()
        return debounced
    return decorator

# from LSP.plugin.code_actions import CodeActionsManager.
# from LSP.plugin.code_actions import actions_manager
# from LSP.plugin.code_actions import run_code_action_or_command
# from LSP.plugin.code_actions import CodeActionOrCommand, CodeActionsResponse, CodeActionsByConfigName
# from LSP.plugin.core.typing import Any, List, Dict, Callable, Optional, Union, Tuple, Mapping, TypedDict
# actions_manager = CodeActionsManager()

# class Tomo2Command(sublime_plugin.ViewEventListener):
#   def on_query_completions(self, prefix, locations):
#     print("sdf")

#     # self.view.run_command(
#     #     "auto_complete", {
#     #         'disable_auto_insert': True,
#     #         'api_completions_only': False,
#     #         'next_completion_if_showing': False
#     #     })

    

#     # return None
#     return (
#       [
#         ["log", "console.log($0);"],
#         ["me2", "method2()"]
#       ],
#       0
#       # sublime.INHIBIT_WORD_COMPLETIONS
#       # sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS
#     )

#   # def on_post_text_command(self, command_name, args):
#   #   print(command_name, args)

#   #   if command_name == "insert_best_completion" and args['default'] == "\t":
#   #     print("ghg")
#   #     sel = self.view.sel()[0].begin()
#   #     # print(sel)
#   #     # dir(sel)
#   #     sublime.set_timeout(lambda: self.view.run_command("tomo", {'sel': sel}), 1000)
#   #   # if command_name == "swap_line_up" or command_name == "swap_line_down":
#   #   #   sublime.set_timeout(lambda: self.view.run_command("lsp_format_document", {}), 100)
      
#   #   # if command_name == "insert_best_completion":
#   #   #   print(args)


# #     print(command_name)


class TomoCommand(sublime_plugin.TextCommand):

#   def handle_responses(self, responses: CodeActionsByConfigName) -> None:


#     print(responses)
#     for config, commands in responses.items():
#       for command in commands:
#         print(command)
#         if 'existing import' in command['title'] or 'Import ' in command['title']:
#           run_code_action_or_command(self.view, config, command)
#           return
#         # results.append((config, command['title'], command))
#     return None

  @debounce(0.3)
  def increment(self):
    print("format")
    self.view.run_command("lsp_format_document_range")
    # self.view.sel().subtract(self.old_region)

  def run(self, edit):
    # print(command)
    # self.view.run_command(command)
    # self.view.run_command("reindent", {"single_line": True})

    # self.view.run_command(
    #     "auto_complete", {
    #         'disable_auto_insert': True,
    #         'api_completions_only': False,
    #         'next_completion_if_showing': False
    #     })
    # # print("lsp_format_document", sel)
    # self.commands = []  # type: List[Tuple[str, str, CodeActionOrCommand]]
    # self.commands_by_config = {}  # type: CodeActionsByConfigName
    # actions_manager.request(self.view, sel, self.handle_responses)
    # sublime.active_window().active_view().run_command("lsp_format_document", {})
    # sublime.active_window().active_view().run_command("expand_selection", { "to": "line"})
    self.view.run_command("swap_line_up", {})
    self.old_selection = self.view.sel()
    self.old_region = sublime.Region(self.old_selection[0].a, self.old_selection[0].b + 1)
    self.view.sel().add(self.old_region)
    self.increment()


# # lsp_format_document