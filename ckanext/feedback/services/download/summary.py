import datetime
import logging
import uuid

from ckan.model import Resource
from flask import request
from sqlalchemy import func

from ckanext.feedback.models import session
from ckanext.feedback.models.download import DownloadSummary

log = logging.getLogger(__name__)


def get_package_downloads(package_id):
    count = (
        session.query(func.sum(DownloadSummary.download))
        .join(Resource)
        .filter(Resource.package_id == package_id)
        .scalar()
    )
    return count or 0


def get_resource_downloads(resource_id):
    count = (
        session.query(DownloadSummary.download)
        .filter(DownloadSummary.resource_id == resource_id)
        .scalar()
    )
    return count or 0


def increment_resource_downloads(resource_id):
    if request.headers.get('Sec-Fetch-Dest') == 'document':
        download_summary = (
            session.query(DownloadSummary)
            .filter(DownloadSummary.resource_id == resource_id)
            .first()
        )
        if download_summary is None:
            download_summary = DownloadSummary(
                str(uuid.uuid4()),
                resource_id,
                1,
                datetime.datetime.now(),
                datetime.datetime.now(),
            )
            session.add(download_summary)
        else:
            download_summary.download = download_summary.download + 1
            download_summary.updated = datetime.datetime.now()
        session.commit()
