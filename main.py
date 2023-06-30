import angel_one_api_connect as api


def main():
    print(1)
    dh = api.DataHandling()
    dh.Login()
    dh.initializeTokenMap()

    stocks = ['SBIN', 'SRF', 'KTKBANK']
    data_df = dh.dataDownloader(stocks, "2021-12-06 00:00", "2021-12-15 00:00")
    print(data_df)

    print(dh.dateTimeCounter(data_df))





if __name__ == "__main__":
    main()
