# LeetCrawler
A simple LeetCode-CN crawler.

https://git.bdaa.pro/yxonic/data-specification/wikis/LeetCode%20%E8%AE%A8%E8%AE%BA

## Usage

LeetCrawler crawls discuss **topics** ans **posts** and **replies** (yet another type of posts) under these topics. After that, LC analyzes markdown code and collects **solutions**. Solutions will be contained in primary posts.

All topics and post will be simply printed out. You might would like to redirect it:

```bash
python3 spider.py > leetcode.data
```

