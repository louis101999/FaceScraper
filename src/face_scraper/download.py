"""Image downloading utilities."""
from __future__ import annotations

import asyncio
from typing import Iterable, List

import aiohttp


async def _download(session: aiohttp.ClientSession, url: str, dest: str) -> None:
    async with session.get(url) as resp:
        resp.raise_for_status()
        data = await resp.read()
        with open(dest, "wb") as f:
            f.write(data)


async def _bounded_download(sem: asyncio.Semaphore, session: aiohttp.ClientSession, url: str, dest: str) -> None:
    async with sem:
        await _download(session, url, dest)


async def download_images_async(urls: Iterable[str], dest_dir: str, concurrency: int = 5) -> List[str]:
    """Download images concurrently.

    Parameters
    ----------
    urls:
        Iterable of image URLs to download.
    dest_dir:
        Directory where images should be stored.
    concurrency:
        Maximum number of concurrent downloads.

    Returns
    -------
    List[str]
        File paths of downloaded images.
    """
    paths = []
    sem = asyncio.Semaphore(concurrency)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, url in enumerate(urls):
            dest = f"{dest_dir}/img_{i}.jpg"
            paths.append(dest)
            tasks.append(_bounded_download(sem, session, url, dest))
        await asyncio.gather(*tasks)
    return paths


def download_images(urls: Iterable[str], dest_dir: str, concurrency: int = 5) -> List[str]:
    """Synchronous wrapper around :func:`download_images_async`."""
    return asyncio.run(download_images_async(urls, dest_dir, concurrency))
