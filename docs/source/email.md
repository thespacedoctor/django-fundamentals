# Email

`ACCOUNT_EMAIL_VERIFICATION` is `"mandatory"` in every environment, so a new
signup cannot log in until they click the link in their confirmation email.
That means email has to work before signup works.

## Development — nothing to configure

Generated projects use Django's console backend outside production:

```python
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

The confirmation email is printed to the terminal running `runserver`. As a
convenience, when `DEBUG` is true the **"verify your email" page also shows the
confirmation link directly**, so you can finish signing up without leaving the
browser. That affordance is strictly gated on `DEBUG` (see
`django_fundamentals/adapters.py`) and never appears in production, where it
would let anyone verify someone else's address.

## Production — Gmail SMTP

Gmail works well for low-volume transactional mail. It will **not** accept your
normal account password — you need an App Password, which requires 2-Step
Verification.

### 1. Create an App Password

1. Enable 2-Step Verification: <https://myaccount.google.com/signinoptions/two-step-verification>
2. Go to <https://myaccount.google.com/apppasswords>
3. Create a password (name it after your app), and copy the 16-character value.
   Spaces in the displayed value are cosmetic — they can be included or omitted.

If `/apppasswords` says the option isn't available, 2-Step Verification isn't
fully enabled yet, or the account is a Workspace account whose administrator has
disabled app passwords.

### 2. Supply the settings via environment variables

A generated project already reads these from the environment in production:

```bash
export DJANGO_ENV=production
export EMAIL_HOST=smtp.gmail.com
export EMAIL_PORT=587
export EMAIL_HOST_USER=you@gmail.com
export EMAIL_HOST_PASSWORD=xxxxxxxxxxxxxxxx   # the 16-character App Password
export DEFAULT_FROM_EMAIL="Your App <you@gmail.com>"
```

Port 587 with `EMAIL_USE_TLS = True` is the combination to use. (Port 465 is the
implicit-TLS alternative and needs `EMAIL_USE_SSL = True` instead — set exactly
one of the two; enabling both raises an error.)

Never commit these values. On a droplet, the Ansible role in
`deploy/deploy-<project>/` writes them to an environment file readable only by
the app user.

### 3. Check it

```bash
python manage.py shell -c "
from django.core.mail import send_mail
send_mail('Test', 'It works.', None, ['you@gmail.com'])
"
```

### Caveats

- **`DEFAULT_FROM_EMAIL` must match the authenticated account** (or an alias you
  have configured in Gmail). Gmail rewrites or rejects mismatched senders.
- **Sending limits**: roughly 500 recipients/day on a free account, 2,000 on
  Workspace. Fine for signup and password-reset mail; not for newsletters.
- **Deliverability**: mail sent this way is "from" a gmail.com address, so it
  cannot be SPF/DKIM-aligned with your own domain. For anything customer-facing
  at volume, prefer a transactional provider (Amazon SES, Postmark, Mailgun,
  Resend) — they use the same `EMAIL_*` settings with a different host, so
  switching later is a config change, not a code change.
