"""*file storage for user-uploaded assets shipped by this package*"""

from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible

# UPLOADS LAND HERE WHEN A PROJECT HAS NO MEDIA_ROOT — RELATIVE TO BASE_DIR IF
# THE PROJECT DEFINES ONE, OTHERWISE THE WORKING DIRECTORY.
DEFAULT_MEDIA_DIRNAME = "media"


@deconstructible
class AvatarStorage(FileSystemStorage):
    """*filesystem storage that works whether or not the host project configures ``MEDIA_ROOT``*

    This package is upgraded into projects that were generated before avatars
    existed, and those projects have no ``MEDIA_ROOT``/``MEDIA_URL`` at all.
    Rather than making every project owner edit ``settings.py`` before uploads
    work, the location is resolved at *call* time from whatever the project
    does have.

    Resolution is deliberately lazy for two reasons: settings are not loaded
    when the model module is imported, and ``@deconstructible`` bakes the
    constructor arguments into the migration — a path resolved in
    ``__init__`` would be frozen into ``0002_user_avatar.py`` as an absolute
    path from whichever machine generated it.

    **Usage:**

    ```python
    avatar = models.ImageField(upload_to="avatars/", storage=AvatarStorage())
    ```
    """

    @property
    def base_location(self):
        mediaRoot = getattr(settings, "MEDIA_ROOT", None)
        if mediaRoot:
            return Path(mediaRoot)

        baseDir = getattr(settings, "BASE_DIR", None)
        if baseDir:
            return Path(baseDir) / DEFAULT_MEDIA_DIRNAME

        return Path.cwd() / DEFAULT_MEDIA_DIRNAME

    @property
    def location(self):
        return str(self.base_location.resolve())
