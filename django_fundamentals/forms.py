"""*forms backing the user settings pages*"""

from django import forms
from django.contrib.auth import get_user_model

# GENEROUS FOR A PHOTO OFF A PHONE, SMALL ENOUGH THAT AvatarView STREAMING IT
# PER REQUEST STAYS CHEAP
MAX_AVATAR_BYTES = 5 * 1024 * 1024


class ProfileForm(forms.ModelForm):
    """*edit the parts of a user account that the user owns*

    Email is deliberately absent: allauth manages email addresses through its
    own ``account_email`` page, which supports multiple addresses, primary
    selection and re-verification. Editing ``User.email`` directly here would
    silently bypass all of that.

    **Usage:**

    ```python
    form = ProfileForm(instance=request.user)
    ```
    """

    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "avatar"]
        labels = {
            "first_name": "First name",
            "last_name": "Last name",
            "avatar": "Profile picture",
        }
        widgets = {
            # VISUALLY HIDDEN, NOT DISABLED — THE STYLED <label> IN
            # settings_profile.html IS THE VISIBLE CONTROL AND CLICKING IT
            # STILL OPENS THE FILE PICKER. KEYBOARD USERS REACH THE REAL INPUT.
            "avatar": forms.ClearableFileInput(attrs={"class": "sr-only"}),
        }

    def clean_avatar(self):
        """*reject uploads too large to be a sensible avatar*

        **Return:**

        - ``avatar`` -- the cleaned upload

        **Usage:**

        ```python
        form.is_valid()
        ```
        """
        avatar = self.cleaned_data.get("avatar")

        # ONLY A FRESH UPLOAD HAS `size`; AN UNCHANGED ImageFieldFile DOESN'T
        # NEED RE-CHECKING AND MAY POINT AT A FILE THAT NO LONGER EXISTS.
        if avatar and hasattr(avatar, "size") and avatar.size > MAX_AVATAR_BYTES:
            raise forms.ValidationError(
                f"Keep profile pictures under {MAX_AVATAR_BYTES // (1024 * 1024)}MB."
            )

        return avatar
