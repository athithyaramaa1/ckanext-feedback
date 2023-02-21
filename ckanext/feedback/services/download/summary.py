import uuid
import logging
import datetime
from six import text_type
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError
from ckan.model import Resource
from ckan.plugins import toolkit
from ckanext.feedback.models.download import DownloadSummary
from psycopg2.errors import InFailedSqlTransaction, UndefinedTable

session = Session()
log = logging.getLogger(__name__)


def get_package_downloads(package_id):
    try:
        package_download_data = (
            session.query(
                Resource.package_id,
                func.sum(DownloadSummary.download).label('package_downloads'),
            )
            .join(DownloadSummary, Resource.id == DownloadSummary.resource_id)
            .group_by(Resource.package_id)
            .filter(Resource.package_id == package_id)
            .first()
        )
        if package_download_data is None:
            return 0

        return package_download_data.package_downloads
    except ProgrammingError as e:

        if isinstance(e.orig, UndefinedTable):
            log.error(
                'download_summary table does not exit. Use "feedback init" command'
            )
        elif isinstance(e.orig, InFailedSqlTransaction):
            log.error(
                'If you did not use the command "feedback init". Use "feedback init"'
            )
        toolkit.error_shout(e)
        return 'Error'
    except Exception as e:
        toolkit.error_shout(e)
        return 'Error'


def get_resource_downloads(resource_id):
    try:
        resource_downloads = (
            session.query(DownloadSummary.download)
            .filter(DownloadSummary.resource_id == resource_id)
            .first()
        )
        return resource_downloads.download
    except ProgrammingError as e:

        if isinstance(e.orig, UndefinedTable):
            log.error(
                'download_summary table does not exit. Use "feedback init" command'
            )
        elif isinstance(e.orig, InFailedSqlTransaction):
            log.error(
                'If you did not use the command "feedback init". Use "feedback init"'
            )
        toolkit.error_shout(e)
        return 'Error'
    except Exception as e:
        toolkit.error_shout(e)
        return 'Error'


def count_resource_downloads(resource_id):
    try:
        resource = (
            session.query(DownloadSummary)
            .filter(DownloadSummary.resource_id == resource_id)
            .first()
        )
        if resource is None:
            download_summary = DownloadSummary(
                text_type(uuid.uuid4()),
                resource_id,
                1,
                datetime.datetime.now(),
                datetime.datetime.now(),
            )
            session.add(download_summary)
        else:
            resource.download = resource.download + 1
            resource.updated = datetime.datetime.now()
        session.commit()
    except ProgrammingError as e:

        if isinstance(e.orig, UndefinedTable):
            log.error(
                'download_summary table does not exit. Use "feedback init" command'
            )
        elif isinstance(e.orig, InFailedSqlTransaction):
            log.error(
                'If you did not use the command "feedback init". Use "feedback init"'
            )

        toolkit.error_shout(e)
        return 'Error'
    except Exception as e:
        toolkit.error_shout(e)
        return 'Error'
