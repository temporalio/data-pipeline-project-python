# your_workflow.py
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import hackernews_top_stories, hackernews_top_story_ids


@workflow.defn
class HackerNewsWorkflow:
    @workflow.run
    async def run(self):
        news_id = await workflow.execute_activity(
            hackernews_top_story_ids,
            start_to_close_timeout=timedelta(seconds=15),
            retry_policy=RetryPolicy(
                maximum_attempts=5,
                non_retryable_error_types=["WorkflowFailureError"],
            ),
        )
        return await workflow.execute_activity(
            hackernews_top_stories,
            news_id,
            start_to_close_timeout=timedelta(seconds=15),
        )
