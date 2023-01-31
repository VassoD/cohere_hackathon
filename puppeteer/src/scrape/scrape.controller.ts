import { Body, Controller, Get, Post, Req } from '@nestjs/common';
import { Request } from 'express';
import { BlobOptions } from 'buffer';

interface paragraphs {
  actiavted: boolean;
  limit?: number;
  regex?: string[];
}

interface title {
  activated: boolean;
}

interface scrapeInfo {
  url: string;
  paragraphs: paragraphs;
  title: title;
}

const puppeteer = require('puppeteer');

@Controller('scrape')
export class ScrapeController {
  @Get('fromUrl')
  url(@Req() req: Request, @Body() dto: scrapeInfo): string {
    console.log(dto.url);
    let paragraphs = undefined;
    async function run() {
      const browser = await puppeteer.launch({
        headless: true,
        ignoreHTTPSErrors: true,
      });

      let page = await browser.newPage();
      await page.goto(dto.url, {
        waitUntil: 'domcontentloaded',
      });
      // wait for paragraphs
      await page.waitForSelector('p', { timeout: 5_000 }).then(async () => {
        let _paragraphs = await page.$$('p');
        for (let i = 0; i < _paragraphs.length; i++) {
          console.log(_paragraphs[i]);
        }
        console.log(_paragraphs.length);
        // console.log(_paragraphs[0].evaluate((node) => node.innerText));
      });
      // console.log(await page.content());
      await page.close();
      await browser.close();
    }
    run();
    return 'okok';
  }
}
