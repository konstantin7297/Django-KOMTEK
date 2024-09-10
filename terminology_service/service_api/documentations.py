from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, \
    OpenApiResponse, inline_serializer
from rest_framework.fields import CharField, BooleanField

from service_api.serializers import DirectorySerializer, DirectoryElementSerializer


response_404 = OpenApiResponse(
    response=inline_serializer(
        name='Response-404',
        fields={"error": CharField()},
    ),
    description="Returned when any error is received",
)
parameter_version = OpenApiParameter(
    name="version",
    type=str,
    required=False,
    description="Returns the directory entries for the specified version.",
    examples=[
        OpenApiExample(
            name="version",
            value="1.0",
            description="format: Number.Number",
        ),
    ],
)

directory_docs = extend_schema(
    tags=['Directory'],
    summary="Getting reference books by the specified date",
    parameters=[
        OpenApiParameter(
            name="date",
            type=str,
            required=False,
            description="Returns directories with a date in the range "
                        "before the specified date",
            examples=[
                OpenApiExample(
                    name="date",
                    value="2023-12-28",
                    description="format: YYYY-MM-DD"
                ),
            ],
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name='Directories',
                fields={"refbooks": DirectorySerializer(many=True)},
            ),
            description="Returns on successful request",
        ),
        404: response_404,
    },
)

directory_element_docs = extend_schema(
    tags=['Directory'],
    summary="Getting a specific directory item",
    parameters=[parameter_version],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name='Directory-elements',
                fields={"elements": DirectoryElementSerializer(many=True)},
            ),
            description="Returns on successful request",
        ),
        404: response_404,
    },
)

directory_check_docs = extend_schema(
    tags=['Directory'],
    summary="Checking if a directory element exists in the database",
    parameters=[
        parameter_version,
        OpenApiParameter(
            name="code",
            type=str,
            required=True,
            description="Element code",
            examples=[
                OpenApiExample(
                    name="code",
                    value="Code1",
                    description="format: string",
                ),
            ],
        ),
        OpenApiParameter(
            name="value",
            type=str,
            required=True,
            description="Element value",
            examples=[
                OpenApiExample(
                    name="value",
                    value="Value1",
                    description="format: string",
                ),
            ],
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name='Response-boolean',
                fields={"exists": BooleanField()},
            ),
            description="Returns on successful request",
        ),
        404: response_404,
    },
)
