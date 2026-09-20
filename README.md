# StudyHub — Learning Resources Portal

StudyHub is a simple learning-resources portal built with Django. It
connects routing, views, templates, static/media files, path and
query parameters, cookies, sessions, and forms into one working
system.

Core flow: Browser -> URL -> View -> Context -> Template -> Response

## Project Structure

studyhub_project/
├── manage.py
├── studyhub_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── urls.py
│   ├── views.py
│   ├── forms.py
│   ├── resources.py
│   ├── context_processors.py
│   └── templates/core/
│       ├── home.html
│       ├── resource_list.html
│       ├── resource_detail.html
│       ├── favorites.html
│       ├── preferences.html
│       ├── feedback.html
│       └── feedback_thanks.html
├── templates/
│   ├── base.html
│   └── 404.html
├── static/
│   ├── css/
│   │   ├── base.css
│   │   ├── light.css
│   │   └── dark.css
│   └── images/
│       ├── logo.png
│       └── sample_resource.jpg
└── media/

## URLs and Views

| URL                     | View               | Name                    | Notes                          |
|--------------------------|--------------------|--------------------------|---------------------------------|
| /                         | home               | core:home                | Featured resources             |
| /resources/               | resource_list      | core:resource_list       | Supports ?type= query param    |
| /resources/<int:id>/      | resource_detail    | core:resource_detail     | Path param; supports ?tab=     |
| /favorites/               | favorites          | core:favorites           | Session-based                  |
| /preferences/             | preferences        | core:preferences         | Sets theme cookie              |
| /feedback/                | feedback           | core:feedback            | GET/POST form                  |
| /feedback/thanks/         | feedback_thanks    | core:feedback_thanks     | Post/Redirect/Get target       |

All routes are declared in core/urls.py (app-level, app_name = "core")
and wired into the project with include() in studyhub_project/urls.py.
The resource detail route uses a path parameter (<int:id>), while the
resource list and detail views also read query parameters
(?type= and ?tab=) to control what is displayed. The Resources page
lets visitors filter the list by type (All, Article, Link, Video),
and the Resource Detail page switches between an Overview and a
Details tab using the same query-parameter pattern.

## Templates

templates/base.html defines the shared layout: a sticky header with
the StudyHub logo and main navigation (Home, Resources, Favorites,
Preferences, Feedback), a main content block, a footer, and a theme
class on <body>. Every page template in core/templates/core/ extends
it with {% extends "base.html" %} and fills the content block.
Navigation links use {% url %} instead of hardcoded paths. Loops and
conditions are used throughout: resource grids on the Home and
Resources pages, the filter and tab bars, and form error messages.
templates/404.html also extends base.html to keep a consistent look
for invalid resource IDs.

## Static Files

CSS and images live in static/ and are loaded with
{% load static %} / {% static '...' %}. base.css holds shared layout
rules (header, buttons, resource cards, the numbered feature grid on
the Home page, and the featured-resource banner); light.css and
dark.css hold theme-specific colors, swapped in base.html depending
on the current theme. The StudyHub logo (images/logo.png) appears in
the header on every page, and a sample resource image
(images/sample_resource.jpg) is featured on the Home page.

## Cookies

The selected theme (light or dark) is read from request.COOKIES in
core/context_processors.py, defaulting to light when the cookie is
missing or holds an invalid value. Because this is a context
processor, the current theme is available in every template without
each view having to pass it manually. The Preferences page lets the
user switch themes; the new value is stored with
response.set_cookie() in the preferences view, and the whole site's
appearance (background, cards, buttons) changes accordingly.

## Sessions

Favorite resource IDs are stored in request.session["favorites"] as
a list of integers. Adding a resource from its detail page checks
for duplicates before appending. The Favorites page reads the
session to display the full resource details and allows removing an
entry via a POST request. Favorites persist across page navigation
because they are stored in the session, not in page-local state.

## Forms

core/forms.py defines FeedbackForm (a plain forms.Form, not a
ModelForm) with name, email, message, and an optional rating field.
The feedback view displays an empty form on GET, binds submitted
data on POST, checks form.is_valid(), and uses form.cleaned_data on
success. A custom clean_message() validator enforces a minimum
message length. {% csrf_token %} is included in every POST form
across the site (Feedback, Preferences, Add to Favorites, Remove
Favorite), and errors are displayed next to each field. Following
the Post/Redirect/Get pattern, a successful feedback submission
redirects to /feedback/thanks/ instead of re-rendering the form.

## Known Limitations

- Resource data is hardcoded in core/resources.py, not stored in a
  database, per the project scope.
- Feedback submissions are not persisted anywhere; only the
  submitter's name is briefly kept in the session to personalize the
  thank-you page.
- Favorites and theme preferences are tied to the browser
  session/cookies, not to a real user account, since the project has
  no authentication system.

## Future Improvements

- Move resources into a database-backed model.
- Persist feedback submissions for review.
- Add user accounts so favorites and preferences follow a specific
  user instead of a browser session.
- Add automated tests for views and form validation.
