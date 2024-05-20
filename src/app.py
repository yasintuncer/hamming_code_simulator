import uix
from uix.core.session import context
from uix.elements import page, main, container, header
from view.hamming_code_ui import HammingCodeUI

def root():
    user = context.session.user = None  # Authentication not implemented for simplicity

    with page("", id="page") as main_page:
        with header("").cls("header-content"):
            pass  # Add any header elements if necessary

        with main(id="main-page").cls("main-page"):
            with container(id="main").style("min-height", "100%").style("scroll-snap-align", "start"):
                HammingCodeUI(id="hamming-code-ui").cls("tool-container")

    return main_page

DEBUG_MODE = True

uix.start(ui=root, config={"debug": DEBUG_MODE})
