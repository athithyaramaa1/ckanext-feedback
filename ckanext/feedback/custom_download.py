from ckanext.feedback.services.download.summary import count_resource_downloads
from ckan.views.resource import download

def custom_download(package_type, id, resource_id, filename=None):
    count_resource_downloads(resource_id)
    return download(package_type, id, resource_id, filename=filename)