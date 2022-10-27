from helpers.multi_app import MultiViewsApp


VIEWS = [
    ("🤩 About us", "about-us", "cats.py"),
    
    "About Cats",
    ("🐈 Cat #1", "cat-1", "cats.py"),
    ("🐈 Cat #2", "cat-2", "cats.py"),
    ("🐈 Cat #3", "cat-3", "cats.py"),
    
    "About Dogs",
    ("🐕 Dog #1", "dog-1", "cats.py"),
    ("🐕 Dog #2", "dog-2", "cats.py"),
    
    "",
    ("📕 Glossary", "glossary", "cats.py"),
]


app = MultiViewsApp(title="Emoji Dashboard", icon="🤣", views=VIEWS)
app.render()