VALID_THEMES = ("light", "dark")

def theme(request):
    current_theme = request.COOKIES.get("theme", "light")
    if current_theme not in VALID_THEMES:
        current_theme = "light"
    return {"theme": current_theme}