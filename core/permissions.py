# core/settings.py

# ... other imports ...
from django.contrib.auth import get_user_model

User = get_user_model()

# --- Custom Rosetta Access Control ---
def is_user_allowed_for_rosetta(user):
    """
    Allow access to Rosetta for superusers or staff users.
    Adjust this logic if you have specific translation groups.
    """
    if not user.is_authenticated:
        return False
    # Allow superusers and staff users
    return user.is_superuser or user.is_staff

# ... (keep your existing INSTALLED_APPS, MIDDLEWARE etc.) ...