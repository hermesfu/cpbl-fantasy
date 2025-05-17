import asyncio
from pyppeteer import launch
import sys

wait_time = 1

async def scraper():
    browser =await launch(
      executablePath='C:/Program Files/Google/Chrome/Application/chrome.exe',
      headless=False
      )
    page = await browser.newPage()
    await page.goto('https://www.cpbl.com.tw/stats/recordall/')

    await page.waitForSelector('th[data-sortby="02"]')
    await page.click('th[data-sortby="02"]')
    await asyncio.sleep(wait_time)

    while True:
        await asyncio.sleep(wait_time)
        rows = await page.querySelectorAll('table tr')
        for row in rows:
            cells = await row.querySelectorAll('th, td')
            row_data = []
            for cell in cells:
                text = await page.evaluate('(el) => el.textContent', cell)
                row_data.append(text.strip())
            print(row_data)
        
        if not await page.querySelector('a[class="next"]'):
            break
        await page.click('a[class="next"]')

    await browser.close()

asyncio.run(scraper())