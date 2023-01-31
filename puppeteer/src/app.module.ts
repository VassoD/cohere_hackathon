import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ScrapeController } from './scrape/scrape.controller';

@Module({
  imports: [],
  controllers: [AppController, ScrapeController],
  providers: [AppService],
})
export class AppModule {}
