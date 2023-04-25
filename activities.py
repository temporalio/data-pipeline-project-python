# activities.py
from dataclasses import dataclass

import requests
from temporalio import activity

TASK_QUEUE_NAME = "hackernews-task-queue"


@dataclass
class HackerNewsTopStoryIds:
    ids: list


@activity.defn
async def hackernews_top_story_ids() -> list:
    top_story_ids = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json"
    ).json()
    return top_story_ids[:10]


@activity.defn
async def hackernews_top_stories(hackernews_top_story_ids):
    results = []
    for item_id in hackernews_top_story_ids:
        item = requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
        ).json()
        results.append([item["title"], item["by"], item["url"]])
    return results
