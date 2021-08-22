import bs4,sqlite3,requests
from datetime import datetime
symbols = []
def restore() -> []:
    bufferlist = []
    db = sqlite3.connect('data.db')
    cursor = db.cursor()
    for value in cursor.execute('SELECT * FROM return ORDER BY id DESC LIMIT 1'): 
        bufferlist.append(value)
    cursor.close()
    db.close()
    return bufferlist
def stockD(stock) -> float:
    url = requests.get(f'https://www.marketwatch.com/investing/stock/{stock.lower()}?mod=over_search')
    soup = bs4.BeautifulSoup(url.text,'lxml')
    return soup.find("div",{"class": "intraday__data"}).find("bg-quote").text

while True:
    for id, orat,perchange,crat, date ,time in restore() :pass
    stock = str(input(': ')).upper()
    try:
        stock = symbols[int(stock)]
    except: pass
    openingP = stockD(stock)
    print(openingP)
    tradet = str(input('x=🐃 || r=🐻')).lower()
    bullish = {'x' : True,"r": False}[tradet]
    input('--')
    closingP = stockD(stock)
    print(closingP)
    openingP = openingP.replace('$',"")
    closingP = closingP.replace('$',"")
    def transproc() :
        diff = ((float(closingP)-float(openingP))/float(openingP))*100
        if bullish == False:
            diff = -1*diff
        print(f'{diff}%')
        db = sqlite3.connect('data.db')
        cursor = db.cursor()
        cursor.execute('INSERT INTO stock VALUES (?,?,?,?,?)',
        (id+1,stock,openingP,closingP,bullish))
        cursor.execute('INSERT INTO return VALUES (?,?,?,?,?,?)', 
        (id+1,crat,diff,crat+diff,f"{datetime.today().strftime('%Y/%m/%d')}", f"{datetime.now().strftime('%H:%M:%S')}"))
        cursor.close()
        db.commit()
        db.close()
    transproc()