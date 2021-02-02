# PyFinra - A simple python script to view FINRA Daily Short Sale Volume data 
This repo is a bit of a work in progress, so please ignore the code formatting issues (lol).

Update: I meant short volume not short interest. (I'll update code in the morning to make this more clear).

**Disclaimer:  Nothing here is financial advice and the data shown is reported from FINRA's website and as such may not be entirely accurate. Please take this into consideration before using this program to make any financial decisions, as I am not responsible for any monetary loses that occur from using this information.**

### Requirements:
Python 3
Beautiful Soup 4


### What's PyFinra?
This scripts scrapes and parses the daily short interest reports that are published by [Finra](http://regsho.finra.org/regsho-Index.html) and be used to generate plots or to print out the data in a human readable form.

The daily short interest percent is calculated using the following equation:
**Short Volume = (ShortVolume/TotalVolume) * 100%**

In the get_data files two examples are provided.
1) Example #1 prints the daily short interest percent for GME for all reports within the last 10 days.
2) Example #2 plots the daily short interest percent for GME from all reports within the last 50 days

To run the code on a different symbol/ number of days, update:
**NUMBER_OF_DAYS
STOCK_SYMBOL**

### Notes:
If you would like to view the data txt files yourself:
Step 1) Figure out the datestring: YYYYMMDD
Step 2) Use url http://regsho.finra.org/CNMSshvol20210201.txt

Example:
Say you wanted to view the data for 02/01/2021
Then: 
	DateString = 20210201
	URL = http://regsho.finra.org/CNMSshvol20210201.txt



### Links:
[Finra txt file structure](http://regsho.finra.org/DailyShortSaleVolumeFileLayout.pdf)
[Daily Finra Short Sale Volume Files](http://regsho.finra.org/regsho-Index.html)

### Credits:
Special thanks to [@minigirraffe](https://twitter.com/minigirraffe) on twitter for the help!
