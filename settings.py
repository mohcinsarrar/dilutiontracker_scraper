# Email and Password
EMAIL = 'your_mail'
PASSWORD = 'your_password'


# show the browser
HEADLESS = False
# Delay to wait until javascript parsed (use a delay greater than 15 seconds)
DELAY_JS = 10
# Configure a delay between requests (this delay applied 5 times, use a delay greater than 1 seconds)
DELAY = 1

# folder to store the Master Sheet
FOLDER = "./"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = [
        ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/57.0.2987.110 '
        'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/61.0.3163.79 '
        'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
        'Gecko/20100101 '
        'Firefox/55.0'),  # firefox
        ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/61.0.3163.91 '
        'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/62.0.3202.89 '
        'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/63.0.3239.108 '
        'Safari/537.36'),  # chrome
]

# use proxies to hide your IP address, and bypass IP blocking 
USE_PROXIES = True
PROXIES = [
    {'http' : 'http://43.128.165.181:59394'},
]


