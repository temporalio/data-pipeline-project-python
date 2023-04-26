# your_workflow.py
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import story_ids, top_stories


@workflow.defn
class HackerNewsWorkflow:
    @workflow.run
    async def run(self) -> list:
        news_id = await workflow.execute_activity(
            story_ids,
            start_to_close_timeout=timedelta(seconds=15),
        )
        return await workflow.execute_activity(
            top_stories,
            news_id,
            start_to_close_timeout=timedelta(seconds=15),
        )
