import angel_one_api_connect as api

def main():
    stocks = ['SBIN', 'SRF', 'KTKBANK']
    print(api.Run(stocks, "2021-12-06 00:00", "2021-12-15 00:00"))

if __name__ == "__main__":
    main()