import asyncio
from pyppeteer import launch
import sys
from dotenv import load_dotenv
import os
from pymongo import MongoClient

wait_time = 1

# Load environment variables
load_dotenv()
mongo_url = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_url)
db = client.cpblfantasy
pitchers = db.pitcher

async def scraper():
    browser = await launch(
      executablePath='C:/Program Files/Google/Chrome/Application/chrome.exe',
      headless=True
      )
    page = await browser.newPage()
    await page.goto('https://www.cpbl.com.tw/stats/recordall/')

    #go to pitcher page
    await page.select('#Position', '02')

    #sort by G to get all players instead of qualified players
    await page.waitForSelector('th[data-sortby="02"]')
    await page.click('th[data-sortby="02"]')

    while True:
        await asyncio.sleep(wait_time)
        rows = await page.querySelectorAll('table tr')

        for row in rows:
            cells = await row.querySelectorAll('td')

            #skip title line
            if (not cells):
                continue
                
            row_data = []
            for cell in cells:
                text = await page.evaluate('(el) => el.textContent', cell)
                row_data.append(text.strip())
            
            columnzero = row_data[0].replace(' ', '').split('\n')
            playername = columnzero[-1]
            team = columnzero[-2]

            #SP or RP
            positions = ['P']
            if (int(row_data[3]) > 0):
                positions.append("SP")
            if (int(row_data[4]) > 0):
                positions.append("RP")
            positions.sort()

            pitchers.update_one({"name": playername},
                                {"$set": {"team": team,
                                          "positions": positions,
                                          "ERA": float(row_data[1]),
                                          "G": int(row_data[2]),
                                          "GS": int(row_data[3]),
                                          "GR": int(row_data[4]),
                                          "CG": int(row_data[5]),
                                          "SHO": int(row_data[6]),
                                          "W": int(row_data[7]),
                                          "L": int(row_data[8]),
                                          "SV": int(row_data[9]),
                                          "HLB": int(row_data[10]),
                                          "BF": int(row_data[11]),
                                          "NP": int(row_data[12]),
                                          "IP": float(row_data[13]),
                                          "H": int(row_data[14]),
                                          "HR": int(row_data[15]),
                                          "R": int(row_data[16]),
                                          "ER": int(row_data[17]),
                                          "BB": int(row_data[18]),
                                          "IBB": int(row_data[19].replace('（', '').replace('）', '')),
                                          "HBP": int(row_data[20]),
                                          "SO": int(row_data[21]),
                                          "WP": int(row_data[22]),
                                          "BK": int(row_data[23]),
                                          "WHIP": float(row_data[24]),
                                          "AVG": float(row_data[25]),
                                          "GO/AO": float(row_data[26]),
                                          "K/BB": float(row_data[27]),
                                          "K/9": float(row_data[28]),
                                          "BB/9": float(row_data[29]),
                                          "H/9": float(row_data[30])}},
                                    upsert=True      
                               )

        if not await page.querySelector('a[class="next"]'):
            break
        await page.click('a[class="next"]')

    await browser.close()

asyncio.run(scraper())