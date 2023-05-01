# @@@SNIPSTART data-pipeline-run-workflow-python
import asyncio

import pandas as pd
from temporalio.client import Client

from activities import TASK_QUEUE_NAME
from your_workflow import TemporalCommunityWorkflow


async def main():
    client = await Client.connect("localhost:7233")

    stories = await client.execute_workflow(
        TemporalCommunityWorkflow.run,
        id="temporal-community-workflow",
        task_queue=TASK_QUEUE_NAME,
    )
    df = pd.DataFrame(stories)
    df.columns = ["Title", "URL", "Views"]
    print("Top 10 stories on Temporal Community:")
    print(df)
    return df


if __name__ == "__main__":
    asyncio.run(main())
# @@@SNIPEND
