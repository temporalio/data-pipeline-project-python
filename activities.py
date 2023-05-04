# @@@SNIPSTART data-pipeline-activity-python
from dataclasses import dataclass
from typing import Any, List

import aiohttp
from temporalio import activity

TASK_QUEUE_NAME = "temporal-community-task-queue"


@dataclass
class TemporalCommunityPost:
    title: str
    url: str
    views: int


@activity.defn
async def post_ids() -> List[str]:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://community.temporal.io/latest.json") as response:
            if not 200 <= int(response.status) < 300:
                raise RuntimeError(f"Status: {response.status}")
            post_ids = await response.json()

    return [str(topic["id"]) for topic in post_ids["topic_list"]["topics"]]


@activity.defn
async def top_posts(post_ids: List[str]) -> List[TemporalCommunityPost]:
    results: List[TemporalCommunityPost] = []
    async with aiohttp.ClientSession() as session:
        for item_id in post_ids:
            async with session.get(
                f"https://community.temporal.io/t/{item_id}.json"
            ) as response:
                if response.status < 200 or response.status >= 300:
                    raise RuntimeError(f"Status: {response.status}")
                item = await response.json()
                slug = item["slug"]
                url = f"https://community.temporal.io/t/{slug}/{item_id}"
                community_post = TemporalCommunityPost(
                    title=item["title"], url=url, views=item["views"]
                )
                results.append(community_post)
    results.sort(key=lambda x: x.views, reverse=True)
    top_ten = results[:10]
    return top_ten


# @@@SNIPEND
