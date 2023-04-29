# @@@SNIPSYNC data-pipeline-your-workflow-python
from datetime import timedelta
from typing import Any, List

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import TemporalCommunityPosts, post_ids, top_posts


@workflow.defn
class TemporalCommunityWorkflow:
    @workflow.run
    async def run(self) -> List[TemporalCommunityPosts]:
        news_ids: List[str] = await workflow.execute_activity(
            post_ids,
            start_to_close_timeout=timedelta(seconds=15),
            retry_policy=RetryPolicy(
                non_retryable_error_types=["Exception"],
            ),
        )
        return await workflow.execute_activity(
            top_posts,
            news_ids,
            start_to_close_timeout=timedelta(seconds=15),
        )


# @@@SNIPEND
