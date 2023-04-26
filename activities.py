# activities.py
from dataclasses import dataclass

import aiohttp
from temporalio import activity

TASK_QUEUE_NAME = "hackernews-task-queue"


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


@activity.defn
async def story_ids() -> list[int]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json"
        ) as response:
            top_story_ids = await response.json()
    return top_story_ids[:10]


@activity.defn
async def top_stories(story_ids) -> list[list[str]]:
    results = []
    async with aiohttp.ClientSession() as session:
        for item_id in story_ids:
            try:
                item = await fetch(
                    session,
                    f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json",
                )
                results.append([item["title"], item["by"], item["url"]])
            except KeyError:
                # For hiring posts where there is no URLs
                print(f"Error processing item {item_id}: {item}")
    return results
