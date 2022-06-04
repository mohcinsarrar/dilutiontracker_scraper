# dilutiontracker_scraper

<div id="top"></div>
<div align="center">
  <h1 align="center">Dilutiontracker Scraper</h1>
</div>

is a simple and functional solution to extract data from [dilutiontracker.com](https://dilutiontracker.com/). dilutiontracker is Industry's Most Authoritative Source of Dilution Data trusted by $400M+ AUM Hedge Funds, Professional Proprietary Traders, and Novices Alike

The program carefully processes the website for the desired tickers, saving their data on your computer, with this program you can get dilution data for any company
<br>This program built with the python framework <a href="https://www.selenium.dev/">Selenuim</a>.

<!-- GETTING STARTED -->
## Installation

1. Clone the repo
   ```sh
   git clone https://github.com/mohcinsarrar/dilutiontracker_scraper.git
   ```
2. Install Requirements
   ```sh
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

### Scrape dilution data
to start scraping dilution data from dilutiontracker, go to the project directory, and use this command
  ```sh
     python main.py -t tickers_list
  ```
- tickers_list is the list of tickers, Exammple ["MDVL","BCYC"]


<p align="right">(<a href="#top">back to top</a>)</p>
