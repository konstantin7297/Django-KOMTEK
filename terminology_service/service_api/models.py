from django.utils import timezone
from django.db import models


class Directory(models.Model):
    """ Модель для описания таблицы справочника """
    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'

    id = models.AutoField(primary_key=True, verbose_name='Идентификатор')
    code = models.CharField(
        max_length=100, null=False, blank=False, unique=True, verbose_name="Код"
    )
    name = models.CharField(
        max_length=300, null=False, blank=False, verbose_name="Наименование"
    )
    description = models.TextField(verbose_name="Описание")

    def __str__(self) -> str:
        return f"Справочник: #{self.pk}"


class VersionDirectory(models.Model):
    """ Модель для описания таблицы версий справочника """
    class Meta:
        verbose_name = 'Версия справочника'
        verbose_name_plural = 'Версии справочника'
        constraints = [
            models.UniqueConstraint(
                name="version_constraint", fields=['directory', 'version'],
            ),
            models.UniqueConstraint(
                name="date_constraint", fields=['directory', 'created_date'],
            )
        ]

    id = models.AutoField(primary_key=True, verbose_name='Идентификатор')
    directory = models.ForeignKey(
        Directory,
        on_delete=models.PROTECT,
        related_name="versions",
        verbose_name="Идентификатор справочника",
    )
    version = models.CharField(
        max_length=50, null=False, blank=False, db_index=True, verbose_name="Версия"
    )
    created_date = models.DateField(
        default=timezone.now,
        editable=True,
        db_index=True,
        verbose_name="Дата начала действия версии",
    )

    def __str__(self) -> str:
        return f"Номер версии справочника: #{self.pk}"


class DirectoryElement(models.Model):
    """ Модель для описания таблицы элементов справочника """
    class Meta:
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочника'
        constraints = [
            models.UniqueConstraint(
                name="code_constraint", fields=['version_directory', 'code'],
            ),
        ]

    id = models.AutoField(primary_key=True, verbose_name='Идентификатор')
    version_directory = models.ForeignKey(
        VersionDirectory,
        on_delete=models.PROTECT,
        related_name="elements",
        verbose_name="Идентификатор Версии справочника",
    )
    code = models.CharField(
        max_length=100, null=False, blank=False, verbose_name="Код элемента",
    )
    value = models.CharField(
        max_length=300, null=False, blank=False, verbose_name="Значение элемента",
    )

    def __str__(self) -> str:
        return f"Номер элемента справочника: #{self.pk}"
