from googlefinance import getNews
import json

print json.dumps(getNews("GOOG"), indent=2)

