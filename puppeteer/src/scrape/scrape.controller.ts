import { Body, Controller, Get, Post, Req } from '@nestjs/common';
import { Request, response } from 'express';
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
const cohere = require('cohere-ai');
cohere.init('lJR6qlpmD2AzOAjbX36VM9FgcGTnWvMh8Uj6oGdg');

interface exampleTemplate {
  text: string;
  label: string;
}
const Example = (text, label): exampleTemplate => {
  let ret: exampleTemplate = {
    text,
    label,
  };
  return ret;
};

@Controller('scrape')
export class ScrapeController {
  @Get('fromUrl')
  async url(@Req() req: Request, @Body() dto: scrapeInfo) {
    console.log(dto.url);
    let paragraphs: string[] = [];
    let ret = {};
    async function run() {
      const browser = await puppeteer.launch({
        headless: true,
        ignoreHTTPSErrors: true,
      });

      let page = await browser.newPage();
      await page.goto(dto.url, {
        waitUntil: 'domcontentloaded',
      });
      console.log(await page.content());
      const pElements = await page.$$eval('p', (p) =>
        p.map((p) => p.innerText),
      );
      // remove empty string
      pElements.map((el) => {
        el !== '' && paragraphs.push(el);
      });
      console.log(paragraphs);
      // close puppeteer
      await page.close();
      await browser.close();

      const response = await cohere.classify({
        inputs: paragraphs,
        examples: [
          Example(
            "I've still got my Christmas tree up - it's so cosy and too much effort to take down",
            'positive',
          ),
          Example(
            'How black barbers in London are giving poor mental health the chop',
            'positive',
          ),
          Example(
            'European equities are holding steady in a solid range with Dax and FTSE both stalling at resistance.',
            'neutral',
          ),
          Example(
            'This morning saw the release of Nationwide housing price data out of the UK ',
            'neutral',
          ),
          Example(
            'For six days, a blast of polar air from Canada has been wrecking holiday travel plans as it lumbers across the country, leaving power outages, canceled flights and dangerous roads in its wake.',
            'negative',
          ),
          Example(
            'Western New York saw days of sustained blizzard conditions',
            'negative',
          ),
        ],
      });
      console.log(JSON.stringify(response));
      let [positive, negative, neutral] = [0, 0, 0];
      const iter = (obj) => {
        Object.keys(obj).forEach((key) => {
          console.log(key);
          if (typeof obj[key] === 'object' && obj[key] !== null) iter(obj[key]);
        });
      };
      return response;
    }
    return await run();
  }
}
