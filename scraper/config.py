import os

#skeleton for ebay search URL: 
#"https://www.ebay.com/sch/i.html?_from=R40&_nkw=____&_sacat=0&_sop=____&_ipg=____&rt=nc&LH_BIN=1&LH_Sold=____&LH_Complete=____&LH_ItemCondition=1000|1500|2000|2500|2750|3000|4000|5000|6000&_udlo=____&_udhi=____&_pgn=____"
#fill in for ____ (4 underscores)
#nkw= (search text, i.e.  searching for iPhone 11 -> nkw=iPhone+11)
#sacat=0& (category, just leave as is)
#sop=10 (sorting parameter, 10 - "newly listed", 15 - "Price+Shipping lowest first", 16 - "Price+Shipping Highest")
#ipg (items per page) - 25, 50, or 200
#not sure what rt=nc means
#LH_BIN=1 (set to "Buy It Now" only), LH_ALL=1 ("All Listings"), LH_Auction=1 (set to "Auction" only)
#LH_Sold=1 (set to already sold listings)
#LH_Complete=1 (set to already complete listings)
#NOTE: sop=10 -> "ended recently" sorting if LH_Sold or LH_Complete are set to 1
#&LH_ItemCondition= (item condition) - 1000 (New), 1500 (Open Box), 2000 (Manufacturer Refurbished), 2500 (Seller Refurbished), 2750 (Like New), 3000 (Used), 4000 (Very Good), 5000 (Good), 6000 (Acceptable)  
#NOTE: use logical/boolean OR ('|') to include multiple
#udlo= (lower price threshold), udhi= (upper price threshold)
#pgn= (listings page number)
#test = "https://www.ebay.com/sch/139971/i.html?_from=R40&_nkw=sega+saturn+&LH_TitleDesc=0&_sop=10&_ipg=200&rt=nc&LH_BIN=1&LH_Sold=1&LH_Complete=1"

cur_dir = os.getcwd()
cat_filename = "mini_CategoryIDs.csv"
ebay_cat_csv = os.path.join(cur_dir, cat_filename)
ebay_item_folder = "item_csv"
ebay_item_dir = os.path.join(os.path.dirname(cur_dir), ebay_item_folder)
