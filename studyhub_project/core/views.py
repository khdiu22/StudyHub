from django.http import Http404
from django.shortcuts import render, redirect

from .forms import FeedbackForm
from .resources import RESOURCES
from .context_processors import VALID_THEMES

SESSION_FAVORITES_KEY = "favorites"


def get_resource_or_404(resource_id):
    for resource in RESOURCES:
        if resource["id"] == resource_id:
            return resource
    raise Http404("Resource not found.")


def home(request):
    context = {"featured_resources": RESOURCES[:3]}
    return render(request, "core/home.html", context)


def resource_list(request):
    selected_type = request.GET.get("type", "")
    resources = RESOURCES
    if selected_type:
        resources = [r for r in RESOURCES if r["type"] == selected_type]
    resource_types = sorted({r["type"] for r in RESOURCES})
    context = {"resources": resources, "resource_types": resource_types, "selected_type": selected_type}
    return render(request, "core/resource_list.html", context)


def resource_detail(request, id):
    resource = get_resource_or_404(id)

    if request.method == "POST":
        favorites = request.session.get(SESSION_FAVORITES_KEY, [])
        if resource["id"] not in favorites:
            favorites.append(resource["id"])
            request.session[SESSION_FAVORITES_KEY] = favorites
        return redirect("core:resource_detail", id=resource["id"])

    active_tab = request.GET.get("tab", "overview")
    favorites = request.session.get(SESSION_FAVORITES_KEY, [])
    context = {"resource": resource, "active_tab": active_tab, "is_favorite": resource["id"] in favorites}
    return render(request, "core/resource_detail.html", context)


def favorites(request):
    if request.method == "POST":
        remove_id = request.POST.get("remove_id")
        if remove_id:
            favorite_ids = request.session.get(SESSION_FAVORITES_KEY, [])
            favorite_ids = [fid for fid in favorite_ids if fid != int(remove_id)]
            request.session[SESSION_FAVORITES_KEY] = favorite_ids
        return redirect("core:favorites")

    favorite_ids = request.session.get(SESSION_FAVORITES_KEY, [])
    favorite_resources = [r for r in RESOURCES if r["id"] in favorite_ids]
    return render(request, "core/favorites.html", {"favorite_resources": favorite_resources})


def preferences(request):
    if request.method == "POST":
        selected_theme = request.POST.get("theme", "light")
        if selected_theme not in VALID_THEMES:
            selected_theme = "light"
        response = redirect("core:preferences")
        response.set_cookie("theme", selected_theme)
        return response
    return render(request, "core/preferences.html")


def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            request.session["last_feedback_name"] = form.cleaned_data["name"]
            return redirect("core:feedback_thanks")
    else:
        form = FeedbackForm()
    return render(request, "core/feedback.html", {"form": form})


def feedback_thanks(request):
    submitted_name = request.session.pop("last_feedback_name", None)
    return render(request, "core/feedback_thanks.html", {"submitted_name": submitted_name})