# @@@SNIPSTART data-pipeline-activity-python
from dataclasses import dataclass
from typing import Any, List

import aiohttp
from temporalio import activity

TASK_QUEUE_NAME = "temporal-community-task-queue"


@dataclass
class TemporalCommunityPosts:
    title: str
    url: str
    views: int


async def fetch(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as response:
        return await response.json()


@activity.defn
async def post_ids() -> List[str]:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://community.temporal.io/latest.json") as response:
            if response.status != 200:
                raise Exception(f"Failed to fetch top stories: {response.status}")
            post_ids = await response.json()

    return [str(topic["id"]) for topic in post_ids["topic_list"]["topics"]]


@activity.defn
async def top_posts(post_ids: List[Any]) -> List[TemporalCommunityPosts]:
    results = []
    async with aiohttp.ClientSession() as session:
        for item_id in post_ids:
            try:
                async with session.get(
                    f"https://community.temporal.io/t/{item_id}.json"
                ) as response:
                    item = await response.json()
                    slug = item["slug"]
                    url = f"https://community.temporal.io/t/{slug}/{item_id}"
                    community_post = TemporalCommunityPosts(
                        title=item["title"], url=url, views=item["views"]
                    )
                    results.append(community_post)
                if response.status != 200:
                    activity.logger.error(f"Status: {response.status}")
            except KeyError:
                activity.logger.error(f"Error processing item {item_id}: {item}")
    results.sort(key=lambda x: x.views, reverse=True)
    top_ten = results[:10]
    return top_ten


# @@@SNIPEND
