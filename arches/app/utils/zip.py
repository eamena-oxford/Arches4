"""
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import os
import zipfile
import datetime
from io import BytesIO
from arches.app.models import models
from django.http import HttpResponse


def create_zip_file(files_for_export):
    """
    Given a list of export file names, zips up all the files with those names and returns and http response.
    """
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip:
        for f in files_for_export:
            f["outputfile"].seek(0)
            zip.writestr(f["name"], f["outputfile"].read())

    zip.close()
    buffer.flush()
    zip_stream = buffer.getvalue()
    buffer.close()
    return zip_stream


def zip_response(files_for_export, zip_file_name=None):
    """
    Given a list of export file names, zips up all the files with those names and returns and http response.
    """
    zip_stream = create_zip_file(files_for_export)
    response = HttpResponse()
    response["Content-Disposition"] = "attachment; filename=" + zip_file_name
    response["Content-length"] = str(len(zip_stream))
    response["Content-Type"] = "application/zip"
    response.write(zip_stream)
    return response
