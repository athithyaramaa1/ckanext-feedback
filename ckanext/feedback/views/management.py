from flask import Blueprint

from ckanext.feedback.controllers import management
from ckanext.feedback.views.error_handler import add_error_handler

blueprint = Blueprint('management', __name__, url_prefix='/management')

# Add target page URLs to rules and add each URL to the blueprint
rules = [
    (
        '/comments',
        'comments',
        management.ManagementController.comments,
    ),
    (
        '/approve_bulk_utilization_comment',
        'approve_bulk_utilization_comment',
        management.ManagementController.approve_bulk_utilization_comment,
        {'methods': ['POST']},
    ),
    (
        '/approve_bulk_resource_comment',
        'approve_bulk_resource_comment',
        management.ManagementController.approve_bulk_resource_comment,
        {'methods': ['POST']},
    ),
    (
        '/delete_bulk_utilization_comment',
        'delete_bulk_utilization_comment',
        management.ManagementController.delete_bulk_utilization_comment,
        {'methods': ['POST']},
    ),
    (
        '/delete_bulk_resource_comment',
        'delete_bulk_resource_comment',
        management.ManagementController.delete_bulk_resource_comment,
        {'methods': ['POST']},
    ),
]
for rule, endpoint, view_func, *others in rules:
    options = next(iter(others), {})
    blueprint.add_url_rule(rule, endpoint, view_func, **options)


@add_error_handler
def get_management_blueprint():
    return blueprint
