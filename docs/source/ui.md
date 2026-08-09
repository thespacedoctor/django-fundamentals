# UI skeleton

`django-fundamentals` ships a complete, themeable UI skeleton: an app shell with
a sidebar and top navbar, a centered layout for authentication pages, styled
status pages, favicons, and dark mode. It is built from
[atomic-design](https://bradfrost.com/blog/post/atomic-web-design/) components
using only the existing stack — Django templates, HTMX, Alpine.js and Tailwind.

## Changing the design: one file

All colours and core dimensions come from CSS custom properties in your
project's **`static/src/tokens.css`**. That is the only file you need to touch
to re-skin the whole application:

```css
:root {
  --color-brand:   8 145 178;   /* #0891b2 */
  --color-surface: 255 255 255;
  --color-ink:     15 23 42;
  --sidebar-w:     16rem;
  --navbar-h:      3.5rem;
  --radius:        0.5rem;
}
.dark { --color-brand: 34 211 238; /* ... */ }
```

Then rebuild: `npm run build:css`.

Colours are **space-separated RGB channels rather than hex** so Tailwind's
opacity modifiers keep working (`bg-brand/10`, `text-ink/70`). Each line carries
its hex equivalent in a comment.

A Tailwind preset shipped *inside the package* maps semantic utility names onto
those variables:

| Token | Utilities |
|---|---|
| `--color-brand` | `bg-brand` `text-brand` `border-brand` |
| `--color-surface` / `--color-raised` / `--color-sunken` | `bg-surface` `bg-raised` `bg-sunken` |
| `--color-ink` / `--color-muted` | `text-ink` `text-muted` |
| `--color-line` | `border-line` |
| `--sidebar-w` | `w-sidebar` `pl-sidebar` |
| `--navbar-h` | `h-navbar` `top-navbar` |
| `--radius` | `rounded` |
| `--content-max` / `--shell-max` | `max-w-content` `max-w-shell` |

The mapping lives in the package so it reaches your project through
`pip install -U django-fundamentals`; the *values* stay yours.

## Layouts

| Layout | Use |
|---|---|
| `django_fundamentals/layouts/base.html` | `<html>` skeleton, `<head>`, theme boot, favicons. Rarely extended directly. |
| `django_fundamentals/layouts/app.html` | App shell — sidebar + navbar + content + footer. |
| `django_fundamentals/layouts/auth.html` | Centered single-column card, no sidebar. |
| `django_fundamentals/layouts/settings.html` | The app shell plus the settings tab rail. |

```django
{% extends "django_fundamentals/layouts/app.html" %}
{% block head_title %}Dashboard &middot; {{ block.super }}{% endblock %}
{% block content %}...{% endblock %}
```

Available blocks: `head_title`, `content`, `content_outer`, `navbar`, `sidebar`,
`footer`, `page_header`, `extra_head`, `extra_body`, `styles`, `scripts`,
`favicons`.

Set `page_title` (and optionally `page_subtitle`) in a view's context to get a
standard page header for free.

### Wrapping pages you don't own: `content_outer`

`app.html` nests the content block inside a second one:

```django
{% block content_outer %}{% block content %}{% endblock %}{% endblock %}
```

A sub-layout overrides `content_outer` to add chrome around *any* page that
extends it, including pages whose templates you don't control. Child templates
keep overriding `content` as normal and land inside the wrapper. This is how the
settings tab rail appears on allauth's email and password pages without
overriding either of them:

```django
{% extends "django_fundamentals/layouts/app.html" %}

{% block content_outer %}
<div class="flex gap-10">
    {% include "django_fundamentals/organisms/settings_tabs.html" %}
    <div class="min-w-0 flex-1">{{ block.super }}</div>
</div>
{% endblock %}
```

`{{ block.super }}` must sit directly inside the `content_outer` override. Wrap
it in a further `{% block %}` and `block.super` resolves against *that* name,
which the parent never defines — the page body then renders as nothing.

## Components

- **atoms/** — `button.html`, `alert.html`, `icon.html`
- **molecules/** — `form_field.html`, `nav_item.html`, `theme_toggle.html`,
  `user_menu.html`, `brand_mark.html`, `avatar.html`
- **organisms/** — `navbar.html`, `sidebar.html`, `footer.html`,
  `messages.html`, `page_header.html`, `settings_tabs.html`

Components are parameterised `{% include %}`s:

```django
{% include "django_fundamentals/atoms/button.html" with label="Save" %}
{% include "django_fundamentals/atoms/button.html" with label="Cancel" variant="secondary" href=back_url %}
{% include "django_fundamentals/atoms/icon.html" with name="home" %}
```

`button` variants: `primary` (default), `secondary`, `ghost`, `danger`.
`icon` names: `home`, `menu`, `close`, `sun`, `moon`, `user`, `shield`, `key`,
`mail`, `chevron-down`, `external`, `check`, `alert`, `settings`, `terminal`,
`eye`, `eye-off`, `copy`, `refresh`, `camera`. Icons are inline SVG using
`currentColor`, so they inherit colour and theme automatically.

`avatar` renders a user's profile picture, falling back to their initials — the
default for every new account, so it is the path most users see:

```django
{% include "django_fundamentals/molecules/avatar.html" with user=request.user %}
{% include "django_fundamentals/molecules/avatar.html" with user=someUser size="h-20 w-20" text="text-2xl" %}
```

## Sidebar navigation

Configured in settings — no template override needed:

```python
DJANGO_FUNDAMENTALS_SITE_NAME = "My App"

DJANGO_FUNDAMENTALS_SIDEBAR_NAV = [
    {"label": "Home", "url_name": "django_fundamentals_home", "icon": "home"},
    {"section": "Billing"},                       # a group heading
    {"label": "Invoices", "url_name": "invoices", "icon": "mail"},
]
```

An entry whose `url_name` cannot be reversed is skipped rather than raising, so
it is safe to list routes that don't exist yet. The active link is detected from
`request.resolver_match.url_name`.

Account tools are deliberately absent from the default nav — they live on the
settings page, reached from the navbar avatar.

## User settings page

`/settings/` gives a signed-in user one place for everything personal, with a
tab rail down the left:

| Tab | Owned by |
|---|---|
| Profile | this package — avatar, username, first/last name |
| Email addresses | allauth (`account_email`) |
| Change password | allauth (`account_change_password`) |
| API | this package — view, copy and regenerate the DRF token |

The tabs come from `SETTINGS_TABS` in `context_processors.py` and are supplied to
every template, because two of them render on allauth's own pages where there is
no view of ours to add context in.

Profile pictures are stored on disk (`MEDIA_ROOT`, falling back to
`BASE_DIR/media`) and served by `AvatarView` rather than by the web server, so a
project needs no `MEDIA_URL` and no Apache `Alias` for uploads to work. Users
without a picture get their initials via `molecules/avatar.html`.

## Dark mode

Tailwind class-based dark mode. The navbar toggle writes `localStorage.theme`
and toggles `.dark` on `<html>`; a small synchronous script in `<head>` applies
the stored (or system) preference before first paint, so there is no flash.

## allauth theming

Rather than overriding allauth's ~30 page templates, this package overrides its
three **layouts** and its **element** templates
(`allauth/elements/{button,field,fields,form,h1,p,...}.html`). Every allauth
page — including the MFA, social-account and session flows — is themed at once,
and allauth keeps its own functionality (social login, passkeys, login-by-code).

The single page template overridden is `account/verification_sent.html`, which
adds the `DEBUG`-only confirmation link described in [Email](email.md).

## Status pages

`404.html`, `403.html` and `400.html` extend the auth layout.

**`500.html` is deliberately standalone** — no `{% extends %}`, no
`{% static %}`, no `request`. Django renders it with an empty context, and the
failure that triggered it may be the database or the staticfiles backend, so it
inlines its own CSS and cannot cascade-fail. Django's default handlers pick all
of these up automatically; no `handler404` wiring is required.

## Overriding anything

Your project's `templates/` directory is searched first, so shadowing a path
replaces that component everywhere:

```
templates/django_fundamentals/organisms/footer.html   # your footer
templates/django_fundamentals/atoms/button.html       # your buttons
```
