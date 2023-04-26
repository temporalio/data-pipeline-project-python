# schedule_workflow.py
import asyncio
from datetime import timedelta

from temporalio.client import (
    Client,
    Schedule,
    ScheduleActionStartWorkflow,
    ScheduleIntervalSpec,
    ScheduleSpec,
    ScheduleState,
)

from activities import TASK_QUEUE_NAME
from your_workflow import HackerNewsWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    await client.create_schedule(
        "workflow-schedule-id",
        Schedule(
            action=ScheduleActionStartWorkflow(
                HackerNewsWorkflow.run,
                id="hackernews-workflow",
                task_queue=TASK_QUEUE_NAME,
            ),
            spec=ScheduleSpec(
                intervals=[ScheduleIntervalSpec(every=timedelta(hours=10))]
            ),
            state=ScheduleState(note="Getting top stories every 10 minutes."),
        ),
    )


if __name__ == "__main__":
    asyncio.run(main())
