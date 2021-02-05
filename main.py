import threading
from urllib.request import Request, urlopen
import bs4 as bs
import tkinter as tk


class Options:

    def __init__(self, callback=None, links=None,):
        self.ltp = None
        self.change = None
        self.percentage = None
        self.callback = callback
        self.links = links
        self.title = None
        self._stopScraping = threading.Event()


        if self.callback:
            threading.Thread(target=self._updater, args=(self.callback, self._stopScraping)).start()

    def getRealDictValue(self):
        return {'Company': self.title, 'ltp': self._ltp, 'change': self.change, 'percentage': self.percentage}

    def stopScraping(self):
        self._stopScraping.set()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def ltp(self):
        return self._ltp

    @ltp.setter
    def ltp(self, value):
        self._ltp = value

    @property
    def change(self):
        return self._change

    @change.setter
    def change(self, value):
        self._change = value

    @property
    def percentage(self):
        return self._percentage

    @percentage.setter
    def percentage(self, value):
        self._percentage = value

    def realData(self, callback=None):
        for link in self.links:

            req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            web_byte = urlopen(req).read()
            web_page = web_byte.decode('utf-8')
            bs_page = bs.BeautifulSoup(web_page, 'lxml')
            tags = bs_page.find_all('bdo')
            title = bs_page.title.text.replace(' - Investing.com India', '')
            lst = []
            for i in tags:
                if i.text != '':
                    lst.append(i.text)
                else:
                    pass

            if self.ltp != lst[0] and self.change != lst[1] and self.percentage != lst[2]:
                self.title = title
                self.ltp = lst[0]
                self.change = lst[1]
                self.percentage = lst[2]

                if callback:
                    callback(self.getRealDictValue())
                else:
                    self.stopScraping()


    def _updater(self, callback, isScraping):
        while not isScraping.is_set():
            self.realData(callback)

def printValues(valDict):
    print('Company ->', valDict['Company'],'Ltp ->', valDict['ltp'], 'Change ->', valDict['change'],
          'Percentage ->', valDict['percentage'], end='\r')


links = ['https://in.investing.com/equities/tata-motors-ltd',
         'https://in.investing.com/indices/s-p-cnx-nifty', 'https://in.investing.com/indices/bank-nifty']

vals = Options(printValues, links)

trackName = None
def SongNamesDisplayer(title, ltp,):
    def display():
        global trackName
        titler = vals.title
        ltpr = vals.ltp
        changer = vals.change
        percentager = vals.percentage
        title.config(text=str(titler))
        ltp.config(text=str(ltpr))
        # change.config(text=str(changer))
        # percentage.config(text=str(percentager))
        title.after(1000, display)
        ltp.after(1000, display)
        # change.after(1000, display)
        # percentage.after(1000, display)

    display()

app = tk.Tk()

canvas = tk.Canvas(app, height=250, width=250)
canvas.pack()
canvass = tk.Canvas(app, height=250, width=250)
canvass.pack()

open = tk.Button(app, text="Run Values", padx=10, pady=5, command=Options(printValues, links))
open.pack()


title = tk.Label(canvas, width=50, height=3, font="Helvetica 16 bold italic", fg="dark green")
title.pack()
ltp = tk.Label(canvass, width=50, height=3, font="Helvetica 16 bold italic", fg="dark green")
ltp.pack()
# change = tk.Label(canvas, width=50, height=3, font="Helvetica 16 bold italic", fg="dark green")
# change.pack()
# percentage = tk.Label(canvas, width=50, height=3, font="Helvetica 16 bold italic", fg="dark green")
# percentage.pack()
SongNamesDisplayer(title, ltp) #change, percentage)
app.mainloop()