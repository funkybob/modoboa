
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _, ugettext_lazy

from modoboa.lib import parameters, events

BASE_EVENTS = [
    "CanCreate",

    "AccountCreated",
    "AccountAutoCreated",
    "AccountModified",
    "AccountDeleted",
    "AccountExported",
    "AccountImported",
    "PasswordUpdated",
    "ExtraAccountActions",
    "RoleChanged",
    "GetExtraRoles",
    "GetExtraRolePermissions",
    "PasswordChange",
    "UserCanSetRole",

    "InitialDataLoaded",

    "UserMenuDisplay",
    "AdminMenuDisplay",
    "GetStaticContent",

    "UserLogin",
    "UserLogout",

    "GetAnnouncement",

    "TopNotifications",
    "ExtraAdminContent",

    "ExtraUprefsRoutes",
    "ExtraUprefsJS",

    "GetExtraParameters",
    "ExtraFormFields",
    "SaveExtraFormFields",
]

PERMISSIONS = {
    "DomainAdmins": [
        ["core", "user", "add_user"],
        ["core", "user", "change_user"],
        ["core", "user", "delete_user"],
    ],
    "SimpleUsers": []
}


def load_core_settings():
    """Load core settings.

    This function must be manually called (see :file:`urls.py`) in
    order to load base settings.
    """
    from modoboa.core.app_settings import GeneralParametersForm, UserSettings

    parameters.register(GeneralParametersForm, ugettext_lazy("General"))
    parameters.register(UserSettings, ugettext_lazy("General"))
    events.declare(BASE_EVENTS)


@events.observe("TopNotifications")
def check_for_new_version(request, include_all):
    """
    Check if a new version of Modoboa is available.
    """
    from modoboa.core.utils import new_version_available

    if not request.user.is_superuser:
        return []
    if new_version_available(request) is None:
        return [{"id": "newversionavailable"}] if include_all else []
    return [{
        "id": "newversionavailable",
        "url": reverse("core:index") + "#info/",
        "text": _("New Modoboa version available"),
        "level": "info",
    }]
