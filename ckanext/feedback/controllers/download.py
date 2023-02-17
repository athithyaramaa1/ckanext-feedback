import ckan.plugins.toolkit as tk
from ckanext.feedback.services.download.summary import increase_resource_download_count 

class DownloadController:

    def increase_resource_download_count(target_resource_id):
        increase_resource_download_count(target_resource_id)
        return tk.render("download/download.html")