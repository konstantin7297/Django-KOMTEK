from django.contrib import admin

from .models import Directory, VersionDirectory, DirectoryElement


class VersionDirectoryInline(admin.TabularInline):
    """ Встраиваемая форма для версий справочника """
    model = VersionDirectory
    fields = ('version', 'created_date')
    extra = 1


class DirectoryElementInline(admin.TabularInline):
    """ Встраиваемая форма для элементов справочника """
    model = DirectoryElement
    fields = ('code', 'value')
    extra = 1


@admin.register(Directory)
class DirectoryAdmin(admin.ModelAdmin):
    """ Административная форма для справочника """
    list_display = "id", "code", "name", "get_current_version", "get_version_date"
    list_display_links = "id", "name"
    ordering = "id", "name"
    search_fields = "code", "name"
    inlines = [VersionDirectoryInline]
    fieldsets = [
        (None, {
            "description": "Основная информация о справочнике",
            "fields": ("code", "name", "description"),
        }),
    ]

    def get_queryset(self, request):
        return Directory.objects.prefetch_related("versions")

    def get_current_version(self, obj: Directory) -> str:
        return obj.versions.latest('created_date').version

    def get_version_date(self, obj: Directory) -> str:
        return obj.versions.latest('created_date').created_date

    get_current_version.short_description = "Текущая версия"
    get_version_date.short_description = "Дата начала действия версии"


@admin.register(VersionDirectory)
class VersionDirectoryAdmin(admin.ModelAdmin):
    """ Административная форма для версий справочника """
    list_display = "get_directory_code", "get_directory_name", "version", "created_date"
    list_display_links = "version", "created_date"
    ordering = "version", "created_date"
    search_fields = "version", "created_date"
    inlines = [DirectoryElementInline]
    fieldsets = [
        (None, {
            "description": "Основная информация о версии справочника",
            "fields": ("directory", "version", "created_date"),
        }),
    ]

    def get_queryset(self, request):
        return VersionDirectory.objects.prefetch_related("elements", "directory")

    def get_directory_code(self, obj: VersionDirectory) -> str:
        return obj.directory.code

    def get_directory_name(self, obj: VersionDirectory) -> str:
        return obj.directory.name

    get_directory_code.short_description = "Код справочника"
    get_directory_name.short_description = "Наименование справочника"


@admin.register(DirectoryElement)
class DirectoryElementAdmin(admin.ModelAdmin):
    """ Административная форма для элементов версий справочника """
    fieldsets = [
        (None, {
            "description": "Основная информации об элементе справочника",
            "fields": ("version_directory", "code", "value"),
        }),
    ]
