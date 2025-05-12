from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin as UnfoldAdmin


class BaseModelAdmin(UnfoldAdmin, ImportExportModelAdmin):
    pass
