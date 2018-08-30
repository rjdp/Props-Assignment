import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime

import xlrd
import xlsxwriter
from django.conf import settings
from django.http import HttpResponse
from io import BytesIO
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Address
from .serializers import AddressSerializer


class AddressApiViewSet(ModelViewSet):
    queryset = Address.objects
    serializer_class = AddressSerializer

    @action(detail=True, methods=["get"])
    def xls(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.get_xls([serializer.data])

    @action(detail=False, methods=["get"])
    def lsxls(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return self.get_xls(serializer.data)

    def get_xls(self, qs):
        output = BytesIO()
        xldoc = xlsxwriter.Workbook(output)
        worksheet = xldoc.add_worksheet()
        header = [field.name for field in Address._meta.fields]
        for i, col_name in enumerate(header):
            worksheet.write(0, i, col_name.replace("_", " ").capitalize())

        for i, row_dict in enumerate(qs):
            for j, key in enumerate(header):
                worksheet.write(i + 1, j, row_dict.get(key, ""))

        xldoc.close()
        response = HttpResponse(
            output.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=address-%s.xlsx" % (
            datetime.now().strftime("%Y/%m/%d-%H:%M:%S.%f")
        )
        return response

    def perform_create(self, serializer):
        extras = {}
        book = xlrd.open_workbook(
            file_contents=serializer.validated_data["imported_xl"].read()
        )
        first_sheet = book.sheet_by_index(0)
        if (
            first_sheet.row_values(0)
            and first_sheet.row_values(0)[0].lower() == "address"
            and first_sheet.row_values(1)
        ):
            params = {
                "address": first_sheet.row_values(1)[0],
                "key": settings.GEOCODING_API_KEY,
            }
            qstring = urllib.parse.urlencode(params)
            url = settings.GEOCODING_API + "?" + qstring
            f = urllib.request.urlopen(url)
            result = json.loads(f.read().decode("utf-8"))
            if result.get("status") == "OK":
                extras["address"] = result["results"][0].get("formatted_address")
                extras["lat"] = (
                    result["results"][0].get("geometry").get("location").get("lat")
                )
                extras["lng"] = (
                    result["results"][0].get("geometry").get("location").get("lng")
                )
            else:
                raise serializers.ValidationError("Invalid data in uploaded excel file")
        serializer.save(**extras)
