from datetime import date
from sqlite3 import Date

from django.db.models import Prefetch, Max, Subquery
from django.http import HttpResponseNotFound
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Directory, DirectoryElement, VersionDirectory
from .serializers import (
    DirectorySerializer,
    DirectoryElementSerializer,
    DateSerializer,
    CheckSerializer,
)
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
    @directory_docs
    def get(self, request: Request, *args, **kwargs) -> Response:
        try:
            query = Directory.objects.prefetch_related("versions") \
                .values("id", "code", "name") \
                .distinct()

            if request.query_params.dict().get("date"):
                serializer = DateSerializer(request.query_params.dict())

                if serializer.is_valid():
                    query = query.filter(
                        versions__created_date__lte=serializer.validated_data.get("date")
                    )

            return Response({"refbooks": DirectorySerializer(query, many=True).data})
        except Exception as e:
            return Response({"error": str(e)}, 404)


class DirectoryElementView(GenericAPIView):
    """ Endpoint for getting a specific directory item """
    @directory_element_docs
    def get(self, request: Request, *args, **kwargs) -> Response:
        try:
            directory_id = int(kwargs.get("id"))
            version = request.query_params.dict().get("version")

            preloaded = Prefetch(
                "version_directory",
                queryset=VersionDirectory.objects.select_related("directory")
            )
            query = DirectoryElement.objects.prefetch_related(preloaded) \
                .values("code", "value") \
                .distinct() \
                .filter(version_directory__directory__id=directory_id)

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

            return Response({
                "elements": DirectoryElementSerializer(result.all(), many=True).data
            })
        except Exception as e:
            return Response({"error": str(e)}, 404)


class DirectoryCheckView(GenericAPIView):
    """ Endpoint for checking if a directory element exists in the database """
    @directory_check_docs
    def get(self, request: Request, *args, **kwargs) -> Response:
        try:
            directory_id = int(kwargs.get("id"))

            serializer = CheckSerializer(data=request.query_params.dict())

            if serializer.is_valid():
                preloaded = Prefetch(
                    "version_directory",
                    queryset=VersionDirectory.objects.select_related("directory")
                )
                query = DirectoryElement.objects.prefetch_related(preloaded).distinct() \
                    .filter(
                    version_directory__directory__id=directory_id,
                    code=serializer.validated_data.get("code"),
                    value=serializer.validated_data.get("value"),
                )

                if serializer.validated_data.get("version"):
                    result = query.filter(
                        version_directory__version=serializer.validated_data.get("version")
                    )
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
