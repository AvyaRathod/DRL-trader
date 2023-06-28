import angel_one_api_connect as api

def main():

    dh = api.DataHandling()
    dh.Login()
    dh.initializeTokenMap()


    stocks = ['SBIN', 'SRF', 'KTKBANK']
    print(api.DataHandling.dataDownloader(stocks, "2021-12-06 00:00", "2021-12-15 00:00"))

if __name__ == "__main__":
    main()