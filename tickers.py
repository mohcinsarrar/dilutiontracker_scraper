###### import general libraries
import settings
import random
import requests
from requests.auth import HTTPBasicAuth
import time
import logging
import sys
from datetime import datetime
import pandas as pd

######### import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as chromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
#############


## class definition
class tickers:

    logging.basicConfig(level=logging.WARNING, format='%(asctime)s : %(message)s')

    # class constructor
    def __init__(self,ticker):
        
        # initial the requests_html session
        self.session = requests.Session()
        self.columns = []
        # get the ticker symbol and add it to info
        self.ticker = ticker
        
        # login to dilutiontracker
        self.login()

    # rotate headers
    def get_headers(self):

        headers = {
            'User-Agent': random.choice(settings.USER_AGENT),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://dilutiontracker.com',
            'Connection': 'keep-alive',
            'Referer': 'https://dilutiontracker.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        return headers

    # rotate proc=xies
    def get_proxy(self):
        if settings.USE_PROXIES:
            return random.choice(settings.PROXIES)
        else:
            return {}
    
    # init columns
    def init_column(self):

        historical_dates = []
        params = {
        'ticker': self.ticker,
        }
        try:
            historicalOS = self.session.get('https://api.dilutiontracker.com/v1/getSharesOS',proxies=self.get_proxy(), headers=self.get_headers(), params=params).json()

            for historical in historicalOS['timeSeriesData']:
                if 'Historical Outstanding' in historical:
                    historical_dates.append(historical['name'])
        except:
            pass

        Atm_nbr = 20
        Warrants_nbr = 20
        Shelf_nbr = 20
        Convertible_Note_nbr = 20
        Convertible_Preferred_nbr = 20
        Equity_Line_nbr = 20
        S1_Offering_nbr = 20

        Atm_columns = ['ATM']
        Warrants_columns = ['Warrant']
        Shelf_columns = ['Shelf']
        Convertible_Note_columns = ['Convertible Note']
        Convertible_Preferred_columns = ['Convertible Preferred']
        Equity_Line_columns = ['Equity Line']
        S1_Offering_columns = ['S-1 Offering']
        

        for i in range(Atm_nbr):
            ll = [
            'Security Name',
            'registrationStatus',
            'Remaining ATM Capacity',
            'Total ATM Capacity',
            'Placement Agent',
            'Agreement Start Date',
            'Last Update Date',
            ]
            
            Atm_columns = Atm_columns + ['ATM_'+str(i+1)+' '+l for l in ll]
        
        for i in range(Warrants_nbr):
            ll = [
            'Security Name',
            'registrationStatus',
            'Remaining Warrants Outstanding',
            'Exercise Price',
            'Total Warrants Issued',
            'Known Owners',
            'Underwriter/Placement agent',
            'Price Protection',
            'Issue Date',
            'Expiration Date',
            'Last Update Date',
            ]
            
            Warrants_columns = Warrants_columns + ['Warrant_'+str(i+1)+' '+l for l in ll]
        
        for i in range(Shelf_nbr):
            ll = [
            'Security Name',
            'registrationStatus',
            'Current Raisable Amount',
            'Total Shelf Capacity',
            'Baby Shelf Restriction',
            'Total Amount Raised',
            'Total Amt. Raised Last 12 Mo. under IB6',
            'Outstanding Shares',
            'Float',
            'Highest 60 Day Close',
            'Price To Exceed Baby Shelf',
            'IB6 Float Value',
            'Last Banker',
            'Effect Date',
            'Expiration Date',
            'Last Update Date',
            ]
            
            Shelf_columns = Shelf_columns + ['Shelf_'+str(i+1)+' '+l for l in ll]

        for i in range(Convertible_Note_nbr):
            ll = [
            'Security Name',
            'registrationStatus',
            'Remaining Shares to be Issued When Converted',
            'Remaining Principal Amount',
            'Conversion Price',
            'Total Shares Issued When Converted',
            'Total Principal Amount',
            'Known Owners',
            'Underwriter/Placement Agent',
            'Price Protection',
            'Issue Date',
            'Maturity Date',
            'Last Update Date',
            ]
            
            Convertible_Note_columns = Convertible_Note_columns + ['Convertible_Note_'+str(i+1)+' '+l for l in ll]
        
        for i in range(Convertible_Preferred_nbr):
            ll = [
            'Security Name',
            'registrationStatus',
            'Remaining Shares to be Issued When Converted',
            'Remaining Dollar Amount',
            'Conversion Price',
            'Total Shares Issued When Converted',
            'Total Dollar Amount Issued',
            'Known Owners',
            'Underwriter/Placement Agent',
            'Price Protection',
            'Issue Date',
            'Maturity Date',
            'Last Update Date',
            ]
            
            Convertible_Preferred_columns = Convertible_Preferred_columns + ['Convertible_Preferred_'+str(i+1)+' '+l for l in ll]

        for i in range(Equity_Line_nbr):
            ll = [
            'Security Name',
            'registrationStatus',
            'Remaining Equity Line Capacity',
            'Total Equity Line Capacity',
            'Agreement Start Date',
            'Agreement End Date',
            'Last Update Date',
            ]
            
            Equity_Line_columns = Equity_Line_columns + ['Equity_Line_'+str(i+1)+' '+l for l in ll]

        for i in range(S1_Offering_nbr):
            ll = [
            'Security Name',
            'registrationStatus',
            'Status',
            'Underwriter/Placement Agent',
            'S-1 Filing Date',
            'Warrant Coverage',
            'Last Update Date',
            'Final Deal Size',
            'Final Pricing',
            'Final Shares Offered',
            'Final Warrant Coverage',
            'Exercise Price',
            ]
            
            S1_Offering_columns = S1_Offering_columns + ['S1_Offering_'+str(i+1)+' '+l for l in ll]


        columns1 = [
            'Scraping Date',
            'Ticker',
            'Mkt Cap',
            'Est. Cash/Sh',
            'T25 Inst Own',
            'short Interest',

            'Overall Risk',
            'Offering Ability',
            'Dilution Amt Ex. Shelf',
            'Historical',
            'Cash Need',

            'Current OS',
            'Float',
            
        ]

        columns2 = [
            '(Quarterly) Operating Cash-Flow',
            'Capital Raise',
            'Months of Cash left',
            'Quarterly Burn',
            'Positive Cash Flow',
            'Historical Cash',
            'Estimated Current Cash',
        ]

        CompletedOfferings_nbr = 30
        CompletedOfferings_columns = []
        for i in range(CompletedOfferings_nbr):
            ll = [
                'Type',
                'Method',
                'Share Equivalent',
                'Price',
                'Warrants',	
                'Offering Amt',
                'Bank',
                'Date',
            ]
            CompletedOfferings_columns = CompletedOfferings_columns + ['Completed_Offerings_'+str(i+1)+' '+l for l in ll]


        columns = \
            columns1 + \
            Atm_columns + \
            Warrants_columns + \
            Shelf_columns + \
            Convertible_Note_columns + \
            Convertible_Preferred_columns + \
            Equity_Line_columns + \
            S1_Offering_columns + \
            columns2 + \
            historical_dates + \
            CompletedOfferings_columns
        
        return columns


    # get historical date
    def get_historical_date(self):

        historical_dates = []
        params = {
        'ticker': self.ticker,
        }
        try:
            historicalOS = self.session.get('https://api.dilutiontracker.com/v1/getSharesOS',proxies=self.get_proxy(), headers=self.get_headers(), params=params).json()

            for historical in historicalOS['timeSeriesData']:
                if 'Historical Outstanding' in historical:
                    historical_dates.append(historical['name'])
        except:
            pass
            
        Atm_nbr = 0
        Warrants_nbr = 0
        Shelf_nbr = 0
        Convertible_Note_nbr = 0
        Convertible_Preferred_nbr = 0
        Equity_Line_nbr = 0
        S1_Offering_nbr = 0

        try:
            getTicker = self.session.get('https://api.dilutiontracker.com/v1/getTicker',proxies=self.get_proxy(), headers=self.get_headers(), params=params).json()

            

            if 'msg' not in getTicker:
                for key,getticker in getTicker.items():
                    
                    if getticker['offeringType'] == 'ATM':
                        Atm_nbr+=1

                    if getticker['offeringType'] == 'Warrant':
                        Warrants_nbr+=1
                    
                    if getticker['offeringType'] == 'Shelf':
                        Shelf_nbr+=1

                    if getticker['offeringType'] == 'Convertible Note':
                        Convertible_Note_nbr+=1

                    if getticker['offeringType'] == 'Convertible Preferred':
                        Convertible_Preferred_nbr+=1
                    
                    if getticker['offeringType'] == 'Equity Line':
                        Equity_Line_nbr+=1
                    
                    if getticker['offeringType'] == 'S-1 Offering':
                        S1_Offering_nbr+=1
        except:
            pass

        CompletedOfferings_nbr = 0

        try:
            CompletedOfferingsReq = self.session.get('https://api.dilutiontracker.com/v1/getCompletedOfferings',proxies=self.get_proxy(), headers=self.get_headers(), params=params).json()   
            
            for key,offer in CompletedOfferingsReq.items():
                CompletedOfferings_nbr+=1
        except:
            pass

        Atm_columns = ['ATM']
        Warrants_columns = ['Warrant']
        Shelf_columns = ['Shelf']
        Convertible_Note_columns = ['Convertible Note']
        Convertible_Preferred_columns = ['Convertible Preferred']
        Equity_Line_columns = ['Equity Line']
        S1_Offering_columns = ['S-1 Offering']
        

        for i in range(Atm_nbr):
            ll = [
            'Security Name',
            'registrationStatus',
            'Remaining ATM Capacity',
            'Total ATM Capacity',
            'Placement Agent',
            'Agreement Start Date',
            'Last Update Date',
            ]
            
            Atm_columns = Atm_columns + ['ATM_'+str(i+1)+' '+l for l in ll]
        
        for i in range(Warrants_nbr):
            ll = [
            'Security Name',
            'registrationStatus',
            'Remaining Warrants Outstanding',
            'Exercise Price',
            'Total Warrants Issued',
            'Known Owners',
            'Underwriter/Placement agent',
            'Price Protection',
            'Issue Date',
            'Expiration Date',
            'Last Update Date',
            ]
            
            Warrants_columns = Warrants_columns + ['Warrant_'+str(i+1)+' '+l for l in ll]
        
        for i in range(Shelf_nbr):
            ll = [
            'Security Name',
            'registrationStatus',
            'Current Raisable Amount',
            'Total Shelf Capacity',
            'Baby Shelf Restriction',
            'Total Amount Raised',
            'Total Amt. Raised Last 12 Mo. under IB6',
            'Outstanding Shares',
            'Float',
            'Highest 60 Day Close',
            'Price To Exceed Baby Shelf',
            'IB6 Float Value',
            'Last Banker',
            'Effect Date',
            'Expiration Date',
            'Last Update Date',
            ]
            
            Shelf_columns = Shelf_columns + ['Shelf_'+str(i+1)+' '+l for l in ll]

        for i in range(Convertible_Note_nbr):
            ll = [
            'Security Name',
            'registrationStatus',
            'Remaining Shares to be Issued When Converted',
            'Remaining Principal Amount',
            'Conversion Price',
            'Total Shares Issued When Converted',
            'Total Principal Amount',
            'Known Owners',
            'Underwriter/Placement Agent',
            'Price Protection',
            'Issue Date',
            'Maturity Date',
            'Last Update Date',
            ]
            
            Convertible_Note_columns = Convertible_Note_columns + ['Convertible_Note_'+str(i+1)+' '+l for l in ll]
        
        for i in range(Convertible_Preferred_nbr):
            ll = [
            'Security Name',
            'registrationStatus',
            'Remaining Shares to be Issued When Converted',
            'Remaining Dollar Amount',
            'Conversion Price',
            'Total Shares Issued When Converted',
            'Total Dollar Amount Issued',
            'Known Owners',
            'Underwriter/Placement Agent',
            'Price Protection',
            'Issue Date',
            'Maturity Date',
            'Last Update Date',
            ]
            
            Convertible_Preferred_columns = Convertible_Preferred_columns + ['Convertible_Preferred_'+str(i+1)+' '+l for l in ll]

        for i in range(Equity_Line_nbr):
            ll = [
            'Security Name',
            'registrationStatus',
            'Remaining Equity Line Capacity',
            'Total Equity Line Capacity',
            'Agreement Start Date',
            'Agreement End Date',
            'Last Update Date',
            ]
            
            Equity_Line_columns = Equity_Line_columns + ['Equity_Line_'+str(i+1)+' '+l for l in ll]

        for i in range(S1_Offering_nbr):
            ll = [
            'Security Name',
            'registrationStatus',
            'Status',
            'Underwriter/Placement Agent',
            'S-1 Filing Date',
            'Warrant Coverage',
            'Last Update Date',
            'Final Deal Size',
            'Final Pricing',
            'Final Shares Offered',
            'Final Warrant Coverage',
            'Exercise Price',
            ]
            
            S1_Offering_columns = S1_Offering_columns + ['S1_Offering_'+str(i+1)+' '+l for l in ll]


        columns1 = [
            'Scraping Date',
            'Ticker',
            'Mkt Cap',
            'Est. Cash/Sh',
            'T25 Inst Own',
            'short Interest',

            'Overall Risk',
            'Offering Ability',
            'Dilution Amt Ex. Shelf',
            'Historical',
            'Cash Need',

            'Current OS',
            'Float',
            
        ]

        columns2 = [
            '(Quarterly) Operating Cash-Flow',
            'Capital Raise',
            'Months of Cash left',
            'Quarterly Burn',
            'Positive Cash Flow',
            'Historical Cash',
            'Estimated Current Cash',
        ]

        CompletedOfferings_columns = []
        for i in range(CompletedOfferings_nbr):
            ll = [
                'Type',
                'Method',
                'Share Equivalent',
                'Price',
                'Warrants',	
                'Offering Amt',
                'Bank',
                'Date',
            ]
            CompletedOfferings_columns = CompletedOfferings_columns + ['Completed_Offerings_'+str(i+1)+' '+l for l in ll]


        columns = \
            columns1 + \
            Atm_columns + \
            Warrants_columns + \
            Shelf_columns + \
            Convertible_Note_columns + \
            Convertible_Preferred_columns + \
            Equity_Line_columns + \
            S1_Offering_columns + \
            columns2 + \
            historical_dates + \
            CompletedOfferings_columns
        
        self.columns = columns

        self.results_df = pd.DataFrame(columns=columns)

        self.results_dict =  dict.fromkeys(columns , "")

        self.results_dict['Ticker'] = self.ticker
        
        now = datetime.now()
        dt_string = now.strftime("%d %B %Y")
        self.results_dict['Scraping Date'] = dt_string
        
    
    # login
    def login(self):
        '''
        Login function
        return True if login to dilutiontracker API success and False else.
        '''
        auth_data = {
            'email': settings.EMAIL,
            'password': settings.PASSWORD,
        }

        try:
            response = self.session.post('https://api.dilutiontracker.com/v1/login',proxies=self.get_proxy(), headers=self.get_headers())
            print(response.json())
            if response.json()['msg'] == 'success':
                logging.warning(f'Login to dilutiontracker for {settings.EMAIL} success...')
            else:
                logging.error('Login to dilutiontracker failed...')
                sys.exit(0)
        except:
            logging.error('Login to dilutiontracker failed...')
            sys.exit(0)

    # get to info
    def get_top_info(self):
        params = {
        'ticker': self.ticker,
        }
        
        try:
            float_value = self.session.get('https://api.dilutiontracker.com/v1/getFloat',proxies=self.get_proxy(), headers=self.get_headers(), params=params).json()['latestFloat']
            self.results_dict['Float'] = round(float_value,2)
        except:
            pass
        try:
            Est_Cash_Sh = self.session.get('https://api.dilutiontracker.com/v1/getCashPerShare',proxies=self.get_proxy(), headers=self.get_headers(), params=params).json()['cashPerShare']
            self.results_dict['Est. Cash/Sh'] = Est_Cash_Sh
        except:
            pass
            
        try:
            marketCap = self.session.get('https://api.dilutiontracker.com/v1/getMarketCap',proxies=self.get_proxy(), headers=self.get_headers(), params=params).json()['marketCap']
            self.results_dict['Mkt Cap'] = marketCap
        except:
            pass

        try:
            totalInstOwnPct = self.session.get('https://api.dilutiontracker.com/v1/getInstOwn',proxies=self.get_proxy(), headers=self.get_headers(), params=params).json()['totalInstOwnPct']
            self.results_dict['T25 Inst Own'] = totalInstOwnPct
        except:
            pass

        try:
            shortInterest = self.session.get('https://api.dilutiontracker.com/v1/getShortInterest',proxies=self.get_proxy(), headers=self.get_headers(), params=params).json()['shortInterestAsPercentOfFloat']
            self.results_dict['short Interest'] = shortInterest
        except:
            pass
        
        
        
        
        
    # get historical info from historical graph
    def get_historical_OS(self):
        params = {
        'ticker': self.ticker,
        }
        try:
            historicalOS = self.session.get('https://api.dilutiontracker.com/v1/getSharesOS',proxies=self.get_proxy(), headers=self.get_headers(), params=params).json()

            Current_OS = 0
            for historical in historicalOS['timeSeriesData']:
                if 'Historical Outstanding' in historical:
                    self.results_dict[historical['name']] = historical['Historical Outstanding']
                if 'Current Outstanding' in historical:
                    Current_OS = round(historical['Current Outstanding'],2)

            self.results_dict['Current OS'] = Current_OS
        except:
            pass

    # get rating (risk)
    def get_rating(self,driver):
            
        # get risk info
        try:
            WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.dilutionRatingSingleWrapper'))
            )
        except:
            pass
        
        try:
            rating = driver.find_elements(By.CSS_SELECTOR, 'div.dilutionRatingSingleWrapper')
        except:
            rating = []

        # risk data not found
        if not rating:
            return False
            
        ratings = []

        for rat in rating:
            ratings.append(rat.find_elements(By.TAG_NAME,'span')[-1].text)

        try:
            self.results_dict['Overall Risk'] = ratings[0]
        except:
            self.results_dict['Overall Risk'] = ""

        try:
            self.results_dict['Offering Ability'] = ratings[1]
        except:
            self.results_dict['Offering Ability'] = ""

        try:
            self.results_dict['Dilution Amt Ex. Shelf'] = ratings[2]
        except:
            self.results_dict['Dilution Amt Ex. Shelf'] = ""

        try:
            self.results_dict['Historical'] = ratings[3]
        except:
            self.results_dict['Historical'] = ""

        try:
            self.results_dict['Cash Need'] = ratings[4]
        except:
            self.results_dict['Cash Need'] = ""
    

    # get atm, warrants ... from historical graph, and get risks
    def get_rating_warrants(self):

        # initial headless browser
        options = chromeOptions()
        if not settings.HEADLESS:
            options.add_argument('--headless')
        user_agent = random.choice(settings.USER_AGENT)
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager(log_level=0, print_first_line=False).install()), 
            options=options)

        # login to dilutiontracker with selenium
        login_url = 'https://dilutiontracker.com/login'

        try:

            driver.get(login_url)

            email = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input#email"))
            )
            password = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input#password"))
            )

            login_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button.LoaderButton"))
            )

            email.send_keys(settings.EMAIL)
            password.send_keys(settings.PASSWORD)

            login_button.click()

            time.sleep(5)

        except:
            logging.error('Login to dilutiontracker failed, Try again')
            sys.exit(0)
        

        # go to ticker page
        ticker_url = f'https://dilutiontracker.com/app/search/{self.ticker}'

        driver.get(ticker_url)
        time.sleep(settings.DELAY_JS)

        # get risk data
        self.get_rating(driver)

        # get info from historical graph
        try:
            WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.CSS_SELECTOR, '.recharts-surface')))

            element_to_hover_over = driver.find_element(By.CSS_SELECTOR,'.recharts-surface').find_elements(By.CSS_SELECTOR,'.recharts-bar-rectangle')[-1]
                
            hover = ActionChains(driver).move_to_element(element_to_hover_over)
            hover.perform()

            time.sleep(settings.DELAY_JS)

            txt = driver.find_element(By.CSS_SELECTOR,'div.recharts-tooltip-wrapper').text
            shares = txt.splitlines()
                
            if not shares:
                logging.error('Error loading page, cant extract ATM warrants ... from historical graph, Try again or extend DELAY_JS')

            for share in shares:
                if 'ATM' in share:
                    self.results_dict['ATM'] = share.split(' ')[-1]

                if 'Warrant' in share:
                    self.results_dict['Warrant'] = share.split(' ')[-1]

                if 'Shelf' in share:
                    self.results_dict['Shelf'] = share.split(' ')[-1]

                if 'Convertible Preferred' in share:
                    self.results_dict['Convertible Preferred'] = share.split(' ')[-1]

                if 'Convertible Note' in share:
                    self.results_dict['Convertible Note'] = share.split(' ')[-1]

                if 'Equity Line' in share:
                    self.results_dict['Equity Line'] = share.split(' ')[-1]

                if 'S-1 Offering' in share:
                    self.results_dict['S-1 Offering'] = share.split(' ')[-1]
        except:
            logging.error("failed to extract warrants data from historical graph, try again or extend DELAY_JS")
        
        driver.close()

    # get info from cash position graph
    def get_cash_position(self):
        params = {
        'ticker': self.ticker,
        }
        try:
            cashPosition = self.session.get('https://api.dilutiontracker.com/v1/getCashPosition',proxies=self.get_proxy(), headers=self.get_headers(), params=params).json()

            Historical_Cash_List = []
            Capital_Raise = 0
            Prorated_quarterly_cf = 0
            Quarterly_Operating_Cashflow = 0
            Last_Cash_Date = ""
            Current_Estimated_Cash = 0
            Historical_Cash = 0
            months = 0
            for cash in cashPosition['timeSeriesData']:
                if 'Historical Cash' in cash:
                    Historical_Cash_List.append(cash)
                if cash['name'] == 'recent offerings':
                    Capital_Raise = cash['Recent Offerings']
                if cash['name'] == 'quarterly operating cashflow':
                    Quarterly_Operating_Cashflow = cash['Quarterly Operating Cashflow']
                if cash['name'] == 'last cash date':
                    Last_Cash_Date = str(cash['Last Cash Date'])

            Historical_Cash = Historical_Cash_List[-1]['Historical Cash']

            date_format = "%m/%d/%Y"
            last_date = datetime.strptime(Last_Cash_Date, date_format)
            last_date = datetime.timestamp(last_date)* 1000
            now = datetime.timestamp(datetime.now())* 1000
            days = abs((last_date-now)/864e5)

            Prorated_quarterly_cf = round(Quarterly_Operating_Cashflow / 3 / 30 * days,2)


            if Prorated_quarterly_cf<0:
                Prorated_quarterly_cf=Prorated_quarterly_cf-0.01
            else:
                Prorated_quarterly_cf=Prorated_quarterly_cf+0.01
                    
            Current_Estimated_Cash = Capital_Raise + Historical_Cash + Prorated_quarterly_cf

            if Quarterly_Operating_Cashflow<0:
                months = round(-Current_Estimated_Cash / Quarterly_Operating_Cashflow * 3 ,1)
            

            if Prorated_quarterly_cf != 0.0: self.results_dict['(Quarterly) Operating Cash-Flow'] = Prorated_quarterly_cf
            if Capital_Raise != 0: self.results_dict['Capital Raise'] = Capital_Raise
            if months != 0.0: self.results_dict['Months of Cash left'] = months
            if Quarterly_Operating_Cashflow<0: self.results_dict['Quarterly Burn'] = Quarterly_Operating_Cashflow
            if Quarterly_Operating_Cashflow>0: self.results_dict['Positive Cash Flow'] = Quarterly_Operating_Cashflow
            self.results_dict['Historical Cash'] = Historical_Cash
            self.results_dict['Estimated Current Cash'] = round(Current_Estimated_Cash, 1)

        except:
            logging.error("extract cash position failed, try again !!")

    # get completed offerings
    def get_completed_offerings(self):
        params = {
        'ticker': self.ticker,
        }

        try:
            CompletedOfferingsReq = self.session.get('https://api.dilutiontracker.com/v1/getCompletedOfferings',proxies=self.get_proxy(), headers=self.get_headers(), params=params).json()   
            i = 1
            for key,offer in CompletedOfferingsReq.items():
                self.results_dict[f'Completed_Offerings_{i} Type'] = offer['type']
                self.results_dict[f'Completed_Offerings_{i} Method'] = offer['method']
                self.results_dict[f'Completed_Offerings_{i} Share Equivalent'] = offer['sharesEquivalent']
                self.results_dict[f'Completed_Offerings_{i} Price'] = offer['price']
                self.results_dict[f'Completed_Offerings_{i} Warrants'] = offer['warrants']
                self.results_dict[f'Completed_Offerings_{i} Offering Amt'] = offer['offeringAmount']
                self.results_dict[f'Completed_Offerings_{i} Bank'] = offer['bank']
                self.results_dict[f'Completed_Offerings_{i} Date'] = offer['pricingDatetime']
                i+=1
        
        except:
            logging.error("extract completed offerings failed, try again !!")
        
    # get aTM, warrants all data from API
    def get_all_warrants(self):

        Atm_list = []
        Warrants_list = []
        Shelf_list = []
        Convertible_Note_list = []
        Convertible_Preferred_list = []
        Equity_Line_list = []
        S1_Offering_list = [] 
        
        params = {
        'ticker': self.ticker,
        }
        
        try :
            getTicker = self.session.get('https://api.dilutiontracker.com/v1/getTicker',proxies=self.get_proxy(), headers=self.get_headers(), params=params).json()

            if 'msg' in getTicker:
                return False
            
            

            for key,getticker in getTicker.items():
                if getticker['offeringType'] == 'ATM':
                    data = dict()
                    data['registrationStatus'] = getticker['registrationStatus']
                    Atm_list.append({**data, **getticker['data']})

                if getticker['offeringType'] == 'Warrant':
                    data = dict()
                    data['registrationStatus'] = getticker['registrationStatus']
                    Warrants_list.append({**data, **getticker['data']})
                
                if getticker['offeringType'] == 'Shelf':
                    data = dict()
                    data['registrationStatus'] = getticker['registrationStatus']
                    Shelf_list.append({**data, **getticker['data']})
                
                if getticker['offeringType'] == 'Convertible Note':
                    data = dict()
                    data['registrationStatus'] = getticker['registrationStatus']
                    Convertible_Note_list.append({**data, **getticker['data']})
                
                if getticker['offeringType'] == 'Convertible Preferred':
                    data = dict()
                    data['registrationStatus'] = getticker['registrationStatus']
                    Convertible_Preferred_list.append({**data, **getticker['data']})
                
                if getticker['offeringType'] == 'Equity Line':
                    data = dict()
                    data['registrationStatus'] = getticker['registrationStatus']
                    Equity_Line_list.append({**data, **getticker['data']})
                
                if getticker['offeringType'] == 'S-1 Offering':
                    data = dict()
                    data['registrationStatus'] = getticker['registrationStatus']
                    S1_Offering_list.append({**data, **getticker['data']})
            
        except:
            logging.error("extract warrants all data failed, try again !!")
            

        # merge all warrants 
        i = 1
        for d in Atm_list:
            for key, value in d.items():
                self.results_dict[f'ATM_{i} {key}'] = value
            i+=1

        i = 1
        for d in Warrants_list:
            for key, value in d.items():
                self.results_dict[f'Warrant_{i} {key}'] = value
            i+=1
        
        i = 1
        for d in Shelf_list:
            for key, value in d.items():
                self.results_dict[f'Shelf_{i} {key}'] = value
            i+=1
  
        i = 1
        for d in Convertible_Note_list:
            for key, value in d.items():
                self.results_dict[f'Convertible_Note_{i} {key}'] = value
            i+=1

        i = 1
        for d in Convertible_Preferred_list:
            for key, value in d.items():
                self.results_dict[f'Convertible_Preferred_{i} {key}'] = value
            i+=1

        i = 1
        for d in Equity_Line_list:
            for key, value in d.items():
                self.results_dict[f'Equity_Line_{i} {key}'] = value
            i+=1
        
        i = 1
        for d in S1_Offering_list:
            for key, value in d.items():
                self.results_dict[f'S1_Offering_{i} {key}'] = value
            i+=1

        
    # parse all list and dict to dataframe
    def parse_ticker_info(self):
        self.results_df = pd.DataFrame(self.results_dict, index=[0])
        