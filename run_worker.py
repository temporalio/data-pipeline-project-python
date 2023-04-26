# run_worker.py
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import TASK_QUEUE_NAME, story_ids, top_stories
from your_workflow import HackerNewsWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE_NAME,
        workflows=[HackerNewsWorkflow],
        activities=[top_stories, story_ids],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
