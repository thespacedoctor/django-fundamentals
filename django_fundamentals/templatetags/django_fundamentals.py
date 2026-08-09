"""*template tags backing the django-fundamentals component library*

**Usage:**

```django
{% load django_fundamentals %}
{% button_classes variant="secondary" as classes %}
{% if_active "django_fundamentals_home" as isActive %}
```
"""

from django import template
from django.urls import NoReverseMatch, reverse

register = template.Library()

# SHARED BY EVERY BUTTON VARIANT — LAYOUT, FOCUS RING, DISABLED STATE
BUTTON_BASE_CLASSES = (
    "inline-flex items-center justify-center gap-2 rounded px-4 py-2 text-sm "
    "font-medium transition-colors focus:outline-none focus-visible:ring-2 "
    "focus-visible:ring-brand focus-visible:ring-offset-2 "
    "focus-visible:ring-offset-surface disabled:pointer-events-none "
    "disabled:opacity-50"
)

BUTTON_VARIANT_CLASSES = {
    "primary": "bg-brand text-brand-fg hover:opacity-90",
    "secondary": "border border-line bg-surface text-ink hover:bg-sunken",
    "ghost": "text-muted hover:bg-sunken hover:text-ink",
    "danger": "bg-danger text-white hover:opacity-90",
}


@register.simple_tag
def button_classes(variant="primary", full=False):
    """*build the full Tailwind class string for a button variant*

    **Key Arguments:**

    - ``variant`` -- one of primary, secondary, ghost, danger
    - ``full`` -- stretch the button to its container's width

    **Return:**

    - ``classes`` -- the space-separated class string

    **Usage:**

    ```django
    {% button_classes variant="danger" full=True as classes %}
    ```
    """
    variantClasses = BUTTON_VARIANT_CLASSES.get(
        variant, BUTTON_VARIANT_CLASSES["primary"]
    )
    classes = f"{BUTTON_BASE_CLASSES} {variantClasses}"
    if full:
        classes = f"{classes} w-full"
    return classes


@register.simple_tag(takes_context=True)
def is_active(context, urlName):
    """*is the named URL the one currently being viewed?*

    Compares against ``request.resolver_match.url_name`` rather than the raw
    path, so it keeps working if a project remounts the URLs at a different
    prefix.

    **Key Arguments:**

    - ``urlName`` -- the URL pattern name to test

    **Return:**

    - ``active`` -- True if ``urlName`` is the current view

    **Usage:**

    ```django
    {% is_active "django_fundamentals_home" as active %}
    ```
    """
    request = context.get("request")
    if not request:
        return False
    resolverMatch = getattr(request, "resolver_match", None)
    if not resolverMatch:
        return False
    return resolverMatch.url_name == urlName


@register.simple_tag
def nav_url(urlName):
    """*reverse a URL name, returning an empty string instead of raising*

    Sidebar entries are configured in settings, so a typo or an app that isn't
    installed should degrade to a dead link rather than 500 the whole page.

    **Key Arguments:**

    - ``urlName`` -- the URL pattern name to reverse

    **Return:**

    - ``path`` -- the resolved path, or "" if it could not be reversed

    **Usage:**

    ```django
    {% nav_url "account_login" %}
    ```
    """
    try:
        return reverse(urlName)
    except NoReverseMatch:
        return ""
