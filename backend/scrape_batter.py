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
batters = db.batter

async def scraper():
    browser = await launch(
      executablePath='C:/Program Files/Google/Chrome/Application/chrome.exe',
      headless=True
      )
    page = await browser.newPage()
    await page.goto('https://www.cpbl.com.tw/stats/recordall/')

    #sort by G to get all players instead of qualified players
    await page.waitForSelector('th[data-sortby="02"]')
    await page.click('th[data-sortby="02"]')

    while True:
        await asyncio.sleep(wait_time)
        rows = await page.querySelectorAll('table tr')

        for row in rows:
            cells = await row.querySelectorAll('td')
            row_data = []
            for cell in cells:
                text = await page.evaluate('(el) => el.textContent', cell)
                row_data.append(text.strip())

            #skip title line
            if (not cells):
                continue
            
            columnzero = row_data[0].replace(' ', '').split('\n')
            playername = columnzero[-1]
            team = columnzero[-2]

            batters.update_one({"name": playername},
                                {"$set": {"team": team,
                                          "avg": float(row_data[1]),
                                          "G": int(row_data[2]),
                                          "PA": int(row_data[3]),
                                          "AB": int(row_data[4]),
                                          "R": int(row_data[5]),
                                          "RBI": int(row_data[6]),
                                          "H": int(row_data[7]),
                                          "1B": int(row_data[8]),
                                          "2B": int(row_data[9]),
                                          "3B": int(row_data[10]),
                                          "HR": int(row_data[11]),
                                          "TB": int(row_data[12]),
                                          "XBH": int(row_data[13]),
                                          "BB": int(row_data[14]),
                                          "IBB": int(row_data[15].replace('（', '').replace('）', '')),
                                          "HBP": int(row_data[16]),
                                          "SO": int(row_data[17]),
                                          "GIDP": int(row_data[18]),
                                          "SAC": int(row_data[19]),
                                          "SF": int(row_data[20]),
                                          "SB": int(row_data[21]),
                                          "CS": int(row_data[22]),
                                          "OBP": float(row_data[23]),
                                          "SLG": float(row_data[24]),
                                          "OPS": float(row_data[25]),
                                          "GO/AO": float(row_data[26]),
                                          "K/BB": float(row_data[27])}},
                                    upsert=True      
                               )

        if not await page.querySelector('a[class="next"]'):
            break
        await page.click('a[class="next"]')

    await browser.close()

asyncio.run(scraper())