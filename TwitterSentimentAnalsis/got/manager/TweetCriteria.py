class TweetCriteria:
    def __init__(self):
        self.maxTweets = 0
        self.within = "15mi"

    def setUsername(self, username):
        if username:
            self.username = username
        return self

    def setSince(self, since):
        if since:
            self.since = since
        return self

    def setUntil(self, until):
        if until:
            self.until = until
        return self

    def setQuerySearch(self, querySearch):
        if querySearch:
            self.querySearch = querySearch
        return self

    def setMaxTweets(self, maxTweets):
        if maxTweets:
            self.maxTweets = maxTweets
        return self

    def setTopTweets(self, topTweets):
        if topTweets:
            self.topTweets = topTweets
        return self

    def setNear(self, near):
        if near:
            self.near = near
        return self

    def setWithin(self, within):
        if within:
            self.within = within
        return self
