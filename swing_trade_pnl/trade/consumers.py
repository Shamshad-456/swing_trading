import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from datetime import datetime, time
import pytz  # Import timezone handling library
from .views import calculate_pnl  

class PnlConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.trade_id = self.scope['url_route']['kwargs']['trade_id']
        self.room_group_name = f'pnl_updates_{self.trade_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Start periodic updates
        self.send_task = asyncio.create_task(self.send_pnl_periodically())

    async def disconnect(self, close_code):
        self.send_task.cancel()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_pnl_periodically(self):
        # Set the correct timezone (assuming market time is in IST)
        tz = pytz.timezone('Asia/Kolkata')

        while True:
            now = datetime.now(tz).time()  # Get the current time with timezone
            market_open = time(9, 15)
            market_close = time(15, 30)

            if market_open <= now <= market_close:
                # print("Market is open")
                await self.send_pnl_update()
            else:
                await self.send(text_data=json.dumps({'message': 'Market is closed'}))
            
            await asyncio.sleep(0.1)  # Update interval in seconds

    async def send_pnl_update(self):
        trade_data = self.scope['session'].get(f'trade_data_{self.trade_id}')
        if not trade_data:
            await self.send(text_data=json.dumps({'error': 'Trade data not found.'}))
            return

        # Calculate P&L asynchronously
        result = await sync_to_async(calculate_pnl)(
            trade_data['scrip'],
            float(trade_data['buy_price']),
            int(trade_data['quantity']),
            datetime.strptime(trade_data['trade_date'], '%Y-%m-%d').date(),
            float(trade_data['margin']),
            float(trade_data['interest_rate']),
            trade_data['exchange']
        )

        await self.send(text_data=json.dumps(result))
