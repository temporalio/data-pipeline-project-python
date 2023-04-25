# run_workflow.py
import asyncio

import pandas as pd
from temporalio.client import Client

from activities import TASK_QUEUE_NAME
from your_workflow import HackerNewsWorkflow


async def main():
    client = await Client.connect("localhost:7233")

    data = await client.execute_workflow(
        HackerNewsWorkflow.run,
        id="hackernews-workflow",
        task_queue=TASK_QUEUE_NAME,
    )

    df = pd.DataFrame(data)

    print(df)


if __name__ == "__main__":
    asyncio.run(main())
