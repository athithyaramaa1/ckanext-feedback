from ckan.model.group import Group
from ckan.model.package import Package
from ckan.model.resource import Resource
from sqlalchemy import func, or_

from ckanext.feedback.models.issue import IssueResolutionSummary
from ckanext.feedback.models.session import session
from ckanext.feedback.models.utilization import Utilization


# Get records from the Utilization table
def get_utilizations(
    id=None, keyword=None, approval=None, owner_orgs=None, owner_org=None
):
    query = (
        session.query(
            Utilization.id,
            Utilization.title,
            Utilization.comment,
            Utilization.created,
            Utilization.approval,
            Resource.name.label('resource_name'),
            Resource.id.label('resource_id'),
            Package.name.label('package_name'),
            Package.owner_org,
            Group.title.label('organization_name'),
            func.coalesce(IssueResolutionSummary.issue_resolution, 0).label(
                'issue_resolution'
            ),
        )
        .join(Resource, Utilization.resource)
        .join(Package)
        .join(Group, Package.owner_org == Group.id)
        .outerjoin(IssueResolutionSummary)
        .order_by(Utilization.created.desc())
    )
    if id:
        query = query.filter(or_(Resource.id == id, Package.id == id))
    if keyword:
        query = query.filter(
            or_(
                Utilization.title.like(f'%{keyword}%'),
                Resource.name.like(f'%{keyword}%'),
                Package.name.like(f'%{keyword}%'),
                Package.owner_org.like(f'%{keyword}%'),
                Group.title.like(f'%{keyword}%'),
            )
        )
    if approval is not None:
        query = query.filter(Utilization.approval == approval)
    if owner_orgs is not None:
        query = query.filter(
            or_(Utilization.approval, Package.owner_org.in_(owner_orgs))
        )
    if owner_org is not None:
        query = query.filter(Package.owner_org == owner_org)

    return query.all()
