"""Jira case management tool handlers — thin wrappers around jira_client functions."""
from jira_client import add_comment as _add_comment
from jira_client import resolve_issue as _resolve_issue
from input_models.models import JiraCommentInput, JiraResolveInput


async def jira_add_comment(params: JiraCommentInput) -> str:
    """Add a comment to the active Jira incident ticket."""
    await _add_comment(params.issue_key, params.comment)
    return f"Comment added to {params.issue_key}"


async def jira_resolve_issue(params: JiraResolveInput) -> str:
    """Transition Jira ticket to resolved state with a resolution summary."""
    await _resolve_issue(params.issue_key, params.resolution_comment, params.resolution)
    return f"{params.issue_key} marked as resolved"
