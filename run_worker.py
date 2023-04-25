# run_worker.py
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import TASK_QUEUE_NAME, hackernews_top_stories, hackernews_top_story_ids
from your_workflow import HackerNewsWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE_NAME,
        workflows=[HackerNewsWorkflow],
        activities=[hackernews_top_stories, hackernews_top_story_ids],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
