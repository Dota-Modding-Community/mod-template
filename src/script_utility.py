import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
minify_root = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))
if os.getcwd() != minify_root:
    os.chdir(minify_root)

if minify_root not in sys.path:
    sys.path.insert(0, minify_root)


from core import output


def run_custom_action():
    """
    Triggered when the user clicks 'Run Custom Utility Action' in the Minify settings UI.
    """
    output.add_text("Executed custom utility action from Template Mod!", indent=True)
