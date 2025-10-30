import requests
from datetime import datetime


url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"


new_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date=%s&json"

class NbuRate:
    '''
    {
        "r030": 12,
        "txt": "Алжирський динар",
        "rate": 0.3236,
        "cc": "DZD",
        "exchangedate": "30.10.2025"
    }
    '''
    def __init__(self, j: dict | None = None):
        self.r030          = j["r030"]         if j else None
        self.full_name     = j["txt"]          if j else None
        self.rate          = j["rate"]         if j else None
        self.short_name    = j["cc"]           if j else None
        self.exchange_date = j["exchangedate"] if j else None

    def __str__(self):
        return "%s (%s) = %f" % (self.short_name, self.full_name, self.rate)

class NbuData:
    def __init__(self, date_str: str):
        request  = requests.get(new_url % date_str)
        response = request.json()
        self.rates = [NbuRate(j) for j in response]

    def size(self):
        return len(self.rates)

    def get_by_short_name(self, fragment: str) -> NbuRate | None:
        return next(
        (rate for rate in self.rates if rate.short_name == fragment.upper()),
        None
        )


    def filter(self, fragment: str):
       f = fragment.upper()
       return (
        rate for rate in self.rates
        if f in rate.short_name or f in rate.full_name.upper()
      )



def input_date():
    while True:
        s = input('Введіть дату у форматі dd.mm.yy (Enter - поточна): ').strip()
        if s == "":
            return datetime.now().strftime("%Y%m%d")

        try:
            d = datetime.strptime(s, "%d.%m.%y")
            if d > datetime.now():
                print("Дата не розпізнана або майбутня")
                continue
            return d.strftime("%Y%m%d")
        except ValueError:
            print("Дата не розпізнана або майбутня")


            
def main():
    nbu_data = NbuData(input_date())
    print("Loaded rates: ", nbu_data.size())
    fragment = input("Enter name to search: ")

    # r = nbu_data.get_by_short_name(fragment)
    # print( r if r else "Not found" )

    print(*nbu_data.filter(fragment), sep='\n')


if __name__ == '__main__':
    main()
