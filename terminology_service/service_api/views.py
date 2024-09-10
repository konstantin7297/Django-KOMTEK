from datetime import date
from sqlite3 import Date

from django.db.models import Prefetch, Max, Subquery
from django.http import HttpResponseNotFound
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Directory, DirectoryElement, VersionDirectory
from .serializers import DirectorySerializer, DirectoryElementSerializer
from .documentations import (
    directory_docs,
    directory_element_docs,
    directory_check_docs,
)


def page_not_fount(request, exception):
    """ Основная функция для отображения при ошибке 404. Просто заглушка для Debug = off """
    return HttpResponseNotFound("<h1>Page not found</h1>")


class DirectoryView(GenericAPIView):
    """ Endpoint for getting a list of reference books for a given date """
    queryset = (
        Directory.objects
        .prefetch_related("versions")
        .values("id", "code", "name")
        .distinct()
    )
    serializer_class = DirectorySerializer

    @directory_docs
    def get(self, request: Request, *args, **kwargs) -> Response:
        try:
            get_date = request.query_params.dict().get("date")

            if get_date:
                year, month, day = get_date.split("-")
                date_obj = Date(int(year), int(month), int(day))
                result = self.get_queryset().filter(versions__created_date__lte=date_obj)
            else:
                result = self.get_queryset()

            return Response({"refbooks": result.all()})
        except Exception as e:
            return Response({"error": str(e)}, 404)


class DirectoryElementView(GenericAPIView):
    """ Endpoint for getting a specific directory item """
    preloaded = Prefetch(
        "version_directory",
        queryset=VersionDirectory.objects.select_related("directory")
    )
    queryset = (
        DirectoryElement.objects
        .prefetch_related(preloaded)
        .values("code", "value")
        .distinct()
    )
    serializer_class = DirectoryElementSerializer

    @directory_element_docs
    def get(self, request: Request, *args, **kwargs) -> Response:
        try:
            directory_id = int(kwargs.get("id"))
            version = request.query_params.dict().get("version")
            query = self.get_queryset().filter(
                version_directory__directory__id=directory_id
            )

            if version:
                result = query.filter(version_directory__version=version)
            else:
                today = date.today()

                max_date_subquery = Subquery(
                    VersionDirectory.objects
                    .filter(directory_id=directory_id, created_date__lte=today)
                    .values('created_date')
                    .annotate(max_date=Max('created_date'))
                    .values('max_date')[:1]
                )
                result = query.filter(
                    version_directory__created_date=max_date_subquery
                )

            return Response({"elements": result.all()})
        except Exception as e:
            return Response({"error": str(e)}, 404)


class DirectoryCheckView(GenericAPIView):
    """ Endpoint for checking if a directory element exists in the database """
    preloaded = Prefetch(
        "version_directory",
        queryset=VersionDirectory.objects.select_related("directory")
    )
    queryset = (
        DirectoryElement.objects
        .prefetch_related(preloaded)
        .distinct()
    )

    @directory_check_docs
    def get(self, request: Request, *args, **kwargs) -> Response:
        try:
            directory_id = int(kwargs.get("id"))
            code, value, version = request.query_params.dict().values()
            query = self.get_queryset().filter(
                version_directory__directory__id=directory_id,
                code=code,
                value=value,
            )

            if version:
                result = query.filter(version_directory__version=version)
            else:
                today = date.today()

                max_date_subquery = Subquery(
                    VersionDirectory.objects
                    .filter(directory_id=directory_id, created_date__lte=today)
                    .values('created_date')
                    .annotate(max_date=Max('created_date'))
                    .values('max_date')[:1]
                )
                result = query.filter(
                    version_directory__created_date=max_date_subquery
                )

            return Response({"exists": bool(result.exists())})
        except Exception as e:
            return Response({"error": str(e)}, 404)
