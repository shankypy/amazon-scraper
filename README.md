# amazon-scraper
This is a simple scrapy project which scraps amazon.com 
all best selling ebooks data from 
https://www.amazon.com/s?k=best+selling+books&i=stripbooks-intl-ship&ref=nb_sb_noss

Note: This is only for practise purpose.

# Dependencies & Installation
Used python 3.6.5 and its virtual environment

Install dependencies through requirements.txt using either 
pip3 or activating the virtual environment

pip3 install -r requirements.txt

# Extracted Data
```
{
   "image":"https://m.media-amazon.com/images/I/81VgmjQIl9L._AC_UY218_.jpg",
   "title":"Too Much and Never Enough: How My Family Created the World’s Most Dangerous Man",
   "published_date":"Jul 14, 2020",
   "author":"Mary L. Trump Ph.D.",
   "reviews":"3,467",
   "ratings":"4.6",
   "book_type_price":{
      "Kindle":"$14.99",
      "Audiobook":"$0.00",
      "Hardcover":"$16.80",
      "Audio CD":"$25.99"
   }
}
```

# Scraped data to JSON file
amazon_best_seller.json file will be located in scrapy
root directory.

# Spiders
$ scrapy list

amazon_ebooks

# Running the spiders
scrapy crawl amazon_ebooks 