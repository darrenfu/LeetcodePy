# How to implement a web crawler
# 	1.	Basic BFS crawler
# 	•	queue + visited
# 	•	normalize URL + same-domain filter
# 	2.	Multi-threaded architecture
# 	•	frontier queue + worker threads + visited with lock
# 	•	dynamic scaling：根据 queue backlog 调整线程数
# 	3.	GIL & concurrency model
# 	•	CPU-bound：多线程没用，用多进程
# 	•	IO-bound（爬虫）：requests 期间释放 GIL，多线程 OK / 有效
# 	•	可选：asyncio 做高并发
# 	4.	Politeness & robustness
# 	•	robots.txt（robotparser）、User-Agent
# 	•	rate limiting、backoff、max depth / max pages
# 	•	error handling, timeouts
# crawler.py
from __future__ import annotations

import threading
import queue
import time
from typing import Set, List
from urllib.parse import urlparse, urljoin, urldefrag
import urllib.robotparser as robotparser

import requests
from bs4 import BeautifulSoup


class Crawler:
    """
    A polite, multi-threaded web crawler that crawls all pages
    under the same domain as the root URL.

    Features:
    - BFS-style traversal using a frontier queue
    - Same-domain restriction
    - robots.txt respect
    - Simple per-domain rate limiting
    - Thread-safe visited set
    """

    def __init__(
            self,
            root_url: str,
            max_workers: int = 10,
            user_agent: str = "MyCrawler/1.0",
            min_interval: float = 0.5,  # per-domain min interval between requests (seconds)
    ):
        self.root_url = self._normalize_root(root_url)
        self.root_domain = urlparse(self.root_url).netloc
        self.max_workers = max_workers
        self.user_agent = user_agent
        self.min_interval = min_interval

        self.frontier: "queue.Queue[str]" = queue.Queue()
        # Improvement area: 可以用 sharded visited：
        # 	•	把 visited 切成多个 shard（比如 16 个 set）
        # 	•	根据 URL hash 分片
        # 	•	每个 shard 有自己的 lock
        # NUM_SHARDS = 16
        # visited_shards = [set() for _ in range(NUM_SHARDS)]
        # locks = [threading.Lock() for _ in range(NUM_SHARDS)]
        #
        # def get_shard(url):
        #     return hash(url) % NUM_SHARDS
        #
        # shard = get_shard(link)
        # with locks[shard]:
        #     if link not in visited_shards[shard]:
        #         visited_shards[shard].add(link)
        self.visited: Set[str] = set()
        self.visited_lock = threading.Lock()

        self.robots = self._load_robots()

        self.stop_event = threading.Event()
        self.workers: List[threading.Thread] = []

        # Simple per-domain rate-limit bookkeeping
        self.last_request_time = 0.0
        self.rate_limit_lock = threading.Lock()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run(self) -> Set[str]:
        """
        Start crawling from root_url and return the set of all visited URLs.
        """
        # Initialize frontier and visited
        with self.visited_lock:
            self.visited.add(self.root_url)
        self.frontier.put(self.root_url)

        # Start workers
        for _ in range(self.max_workers):
            t = threading.Thread(target=self._worker_loop, daemon=True)
            t.start()
            self.workers.append(t)

        # Wait until all tasks done.
        # Queue.join() blocks until task_done() has been called for every enqueued task.
        # This is often the “wait for completion” barrier in a thread pool.
        self.frontier.join()
        self.stop_event.set()

        # Gracefully join workers.
        # This ensures:
        # 	•	No threads are left dangling.
        # 	•	No background workers continue running after the program is done.
        # 	•	Resources are cleaned up.
        for t in self.workers:
            t.join(timeout=1.0)

        return self.visited

    # ------------------------------------------------------------------
    # Worker logic
    # ------------------------------------------------------------------
    def _worker_loop(self) -> None:
        while not self.stop_event.is_set():
            try:
                # Dequeue ONE specific item
                url = self.frontier.get(timeout=1.0)
            except queue.Empty:
                # If queue is empty and no new tasks come in, worker can exit
                if self.frontier.empty():
                    return
                continue

            try:
                self._process_url(url)
            finally:
                # This implicitly matches the last get() executed by that thread.
                # There is a 1:1 relationship: queue.get()  ↔  queue.task_done()
                self.frontier.task_done()

    def _process_url(self, url: str) -> None:
        print("process_url: ", url)
        # robots.txt check
        if not self._allowed_by_robots(url):
            print("robots disallowed")
            return

        html, content_type = self._fetch(url)
        if not html:
            return

        links = self._extract_links(url, html, content_type)
        for link in links:
            with self.visited_lock:
                if link in self.visited:
                    continue
                self.visited.add(link)
            self.frontier.put(link)

    # ------------------------------------------------------------------
    # Normalization & robots
    # ------------------------------------------------------------------
    @staticmethod
    def _normalize_root(root_url: str) -> str:
        root_url, _ = urldefrag(root_url)
        parsed = urlparse(root_url)
        if not parsed.scheme:
            # default to http if scheme missing
            root_url = "http://" + root_url
        return root_url

    def _load_robots(self):
        """
        Load robots.txt for the root domain.
        """
        rp = robotparser.RobotFileParser()
        robots_url = urljoin(self.root_url, "/robots.txt")
        try:
            # You can choose verify=False to skip bad SSL certs
            resp = requests.get(robots_url, headers={"User-Agent": self.user_agent},
                                timeout=5, verify=False)
            if resp.status_code == 200:
                rp.parse(resp.text.splitlines())
            else:
                # treat as empty robots (allow all)
                rp.parse([])
        except Exception:
            # treat as empty robots (allow all)
            rp.parse([])
        return rp

    def _allowed_by_robots(self, url: str) -> bool:
        if not self.robots:
            return True
        try:
            return self.robots.can_fetch(self.user_agent, url)
        except Exception:
            # Fail open: if robots parsing fails, allow
            return True

    # ------------------------------------------------------------------
    # Fetching & parsing
    # ------------------------------------------------------------------
    def _rate_limited_sleep_if_needed(self) -> None:
        """
        Very simple per-domain rate limiting: ensure that at least
        min_interval seconds pass between requests.
        """
        with self.rate_limit_lock:
            now = time.time()
            delta = now - self.last_request_time
            if delta < self.min_interval:
                time.sleep(self.min_interval - delta)
            self.last_request_time = time.time()

    def _fetch(self, url: str) -> tuple[str | None, str | None]:
        """
        Fetch HTML content from a URL with basic error handling.
        """
        self._rate_limited_sleep_if_needed()

        headers = {"User-Agent": self.user_agent}
        try:
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code != 200:
                return None, None
            return resp.text, resp.headers.get("Content-Type")
        except Exception:
            return None, None

    def _extract_links(self, url: str, html: str, content_type: str | None = None) -> list[str]:
        """
        Extract and normalize same-domain links from HTML or XML.
        Automatically selects the parser based on content type or URL suffix.
        """
        # Determine if XML/RSS/Atom
        is_xml = False

        if content_type:
            ct = content_type.lower()
            if ("xml" in ct) or ("rss" in ct) or ("atom" in ct):
                is_xml = True
        else:
            # fallback: detect by URL suffix
            if url.endswith(".xml") or url.endswith(".rss") or url.endswith(".atom"):
                is_xml = True

        # Select parser
        if is_xml:
            # Requires `pip install lxml`
            soup = BeautifulSoup(html, features="xml")
        else:
            soup = BeautifulSoup(html, "html.parser")

        # Collect href links
        links: list[str] = []
        for a in soup.find_all("a", href=True):
            norm = self._normalize_url(url, a["href"])
            if norm:
                links.append(norm)

        return links

    def _normalize_url(self, base_url: str, link: str) -> str | None:
        """
        Join relative URLs, strip fragments, enforce same-domain and http(s).
        """
        abs_url = urljoin(base_url, link)
        abs_url, _ = urldefrag(abs_url)
        parsed = urlparse(abs_url)

        if parsed.scheme not in ("http", "https"):
            return None
        if parsed.netloc != self.root_domain:
            return None

        return abs_url


# ----------------------------------------------------------------------
# Main: simple CLI
# ----------------------------------------------------------------------
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Simple multi-threaded domain web crawler")
    parser.add_argument("root", help="Root URL to start crawling from")
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=10,
        help="Maximum number of worker threads (default: 10)",
    )
    parser.add_argument(
        "--min-interval",
        type=float,
        default=0.5,
        help="Minimum interval between requests in seconds (default: 0.5)",
    )
    args = parser.parse_args()

    crawler = Crawler(
        root_url=args.root,
        max_workers=args.workers,
        min_interval=args.min_interval,
    )
    visited = crawler.run()

    for url in sorted(visited):
        print(url)


if __name__ == "__main__":
    main()