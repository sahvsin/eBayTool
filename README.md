# eBay Item Market Analysis
Three tools to aid in eBay market tracking, benefiting consumer, vendor and analyzer


## Data Scraper
<br>

![](./scraper/GIFs/ebay_I.gif)
<p align="center">
  Enter search query (Logitech c920 -case -cable -cover), add parameters (BuyItNow/Auction/both, current/past, etc.), build URL, and store listings data (title, price, date, URL) in CSV 
</p>

<br><br>
Ask the user what to search for like a normal eBay search query and request a few additional parameters like whether to look at past or current listings or only buy-it-now or auction.

Then build a specific URL using encodings learned from [eBay API documentation](https://developer.ebay.com/api-docs/static/rest-request-components.html). Use the Python [Requests](https://requests.readthedocs.io/en/master/) library to request access to the webpage by the server managing the webpage directed by the built URL.

Finally scrape every listing using the Python [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) library and store the listings data (title, price, shipping, date, and URL) into a fresh CSV stored locally.
<br><br><br><br>

## Data Analyzer
<br>

![](./data_processing/GIFs/ebay_II.gif)
<p align="center">
  Process listings data (Logitech c920 webcam in this example) to compute min, max, mean, and mode 
</p>

<br><br>
The user digs through archived scraped eBay listings CSVs and chooses which one to process. First it loads all of the listings from the CSV into a [Pandas](https://pandas.pydata.org/) dataframe. Then it processes the data depending on whether the listings are currently live or completed.

If live, it computes logistics such as the current min, max, mode, and mean prices (+shipping) and stores them in a new CSV alongside its associated listings data.

If processing past listings, compute the same logistics, but since eBay only archives the past 90 days, compute the logistics by month and days of each month. The daily logistics are plotted in separate plots per month. Meanwhile monthly logistics are saved into a local CSV similar to the live listings logistics data. 
<br><br><br><br>

## Notifier
Currently a Work-in progress, somewhat functional
