from numpy import isin
import streamlit as st
import os
import time
from inspect import currentframe, getframeinfo
import emoji


class MultiViewsApp:
    def __init__(self, title, icon, views):
        self.title = title
        self.icon = icon
        self.views = views
        self.mapping = self._build_mapping(views)
        self.mapping["error"] = dict(path="error.py", label="Error")

    @staticmethod
    def _build_mapping(views):
        mapping = {}
        for item in views:
            if isinstance(item, str):
                continue
            elif isinstance(item, tuple):
                label, name, path = item
                if name in mapping:
                    raise KeyError("Duplicated View Name")
                mapping[name] = dict(label=label, path=path)
            else:
                raise ValueError("Only str/tuple items are acceptable")

        return mapping

    def _render_sidebar(self):
        with st.sidebar:
            st.title(f"{self.icon} {self.title}")

            with st.container():
                for item in self.views:
                    if isinstance(item, str):
                        if item == "---":
                            st.markdown("---")
                        else:
                            st.header(item)
                    else:
                        label, name, path = item
                        navigate_to(label, name)
                        
    def _render_css(self):
        with st.sidebar:
            with open("style.css") as file:
                styles = file.read()

            st.markdown(f"<style>{styles}</style>", unsafe_allow_html=True)

    def _view_to_render(self) -> str:
        params = st.experimental_get_query_params()
        view = None
        if "v" in params:
            view = params["v"][0]
            if view not in self.mapping:
                return "error"
        else:
            view = next(iter(self.mapping.keys()))
            st.experimental_set_query_params(v=view)
        return view

    def _render_view(self, view: str):
        path = self.mapping[view]["path"]

        with open(os.path.join("views", path), encoding="utf-8") as file:
            code = compile(file.read(), path, mode='exec')
            exec(code, dict(__view__=view))

    def render(self):
        view_to_render = self._view_to_render()

        view_label = emoji.replace_emoji(self.mapping[view_to_render]["label"], replace="").strip()
        st.set_page_config(page_title=f"{view_label} - {self.title}", page_icon=self.icon)
        self._render_sidebar()
        self._render_css()
        
        self._render_view(view_to_render)



def navigate_to(label: str, view: str, params: dict[str, str]={}, key=None) -> None:
    """Change current dashboard view

    Args:
        label (str): Button label
        view (str): _description_
        params (dict[str, str]): _description_
    """
    i = navigate_to.counts[view] = navigate_to.counts.get(view, 0) + 1

    if not key:
        frameinfo = getframeinfo(currentframe().f_back)
        seed = f"{view}-{frameinfo.filename}-{frameinfo.lineno}"
        key = f"{view}-{hash(seed)}"

    if st.button(label, key=key):
        print(params)
        st.experimental_set_query_params(v=view, **params)
        time.sleep(0.1)
        st.experimental_rerun()

navigate_to.counts = {}
