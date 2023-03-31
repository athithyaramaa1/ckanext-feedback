from ckan.common import _, c, request
from ckan.lib import helpers
from ckan.plugins import toolkit
from flask import make_response, redirect, url_for
from ckan.logic import get_action
import ckan.model as model

import ckanext.feedback.services.resource.comment as comment_service
import ckanext.feedback.services.resource.summary as summary_service
from ckanext.feedback.models.session import session


class ResourceController:
    # Render HTML pages
    # resource_comment/<resource_id>
    @staticmethod
    def comment(resource_id):
        approval = None
        if c.userobj is None or c.userobj.sysadmin is None:
            approval = True
        resource = comment_service.get_resource(resource_id)
        comments = comment_service.get_resource_comments(resource_id, approval)
        categories = comment_service.get_resource_comment_categories()
        cookie = comment_service.get_cookie(resource_id)
        context = {
                'model': model,
                'session': session,
                'for_view': True
            }
        package = get_action('package_show')(context, {'id': resource.package_id})

        return toolkit.render(
            'resource/comment.html',
            {
                'resource': resource,
                'pkg_dict': package,
                'comments': comments,
                'categories': categories,
                'cookie': cookie,
            },
        )

    # resource_comment/<resource_id>/comment/new
    @staticmethod
    def create_comment(resource_id):
        category = request.form.get('category', '')
        content = request.form.get('comment_content', '')
        rating = int(request.form.get('rating', 0))
        comment_service.create_resource_comment(resource_id, category, content, rating)
        summary_service.create_resource_summary(resource_id)
        session.commit()

        helpers.flash_success(
            _(
                'Your comment has been sent.<br>The comment will not be displayed until'
                ' approved by an administrator.'
            ),
            allow_html=True,
        )

        resp = make_response(
            redirect(url_for('resource_comment.comment', resource_id=resource_id))
        )
        resp.set_cookie(resource_id, 'alreadyPosted')

        return resp

    # resource_comment/<resource_id>/comment/approve
    @staticmethod
    def approve_comment(resource_id):
        resource_comment_id = request.form.get('resource_comment_id')
        comment_service.approve_resource_comment(resource_comment_id, c.userobj.id)
        summary_service.refresh_resource_summary(resource_id)
        session.commit()

        return redirect(url_for('resource_comment.comment', resource_id=resource_id))

    # resource_comment/<resource_id>/comment/reply
    @staticmethod
    def reply(resource_id):
        resource_comment_id = request.form.get('resource_comment_id', '')
        content = request.form.get('reply_content', '')
        comment_service.create_reply(resource_comment_id, content, c.userobj.id)
        session.commit()

        return redirect(url_for('resource_comment.comment', resource_id=resource_id))
