import asyncio
import json
from statistics import mean

from discord.ext.commands import Cog

from acolyte.constants import STATE_CHECK_STEPS, STATE_CHECK_TIMEOUT


class Brain(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        if self.bot.user.mentioned_in(message):
            await self.process_message(message)
        # Иначе закидываем сообщение на тренировку модели (кроме своих сообщений).
        else:
            text = message.content
            await self.bot.brain.post('http://brain:8080/train', data=text)

    async def process_message(self, message):
        if 'state' in message.content:
            await message.channel.send(
                'Не может быть, соизволил поинтересоваться моим самочувствием? '
                'Погоди, прощупаю свои чумные бубоны.'
            )
            states = []
            for step in range(STATE_CHECK_STEPS):
                response = await self.bot.brain.get('http://brain:8080/state')
                states.append(json.loads(await response.text()))
                await asyncio.sleep(STATE_CHECK_TIMEOUT)
            mean_cpu = mean(state['cpu'] for state in states)
            mean_ram = mean(state['mem'] for state in states)
            current_queue_size = states[-1]['queue_size']
            seconds_passed = STATE_CHECK_STEPS * STATE_CHECK_TIMEOUT
            messages_processed = states[0]['queue_size'] - current_queue_size
            processing_speed = messages_processed / seconds_passed
            output = "\n".join(
                [
                    f':cyclone: **ЦПУ**: *{mean_cpu}%*',
                    f':closed_book: **Память**: *{mean_ram}%*',
                    f':chains: **В очереди**: *{current_queue_size}*',
                    f':recycle: **Скорость обработки**: *{processing_speed}/с*',
                ]
            )
        else:
            response = await self.bot.brain.get('http://brain:8080/test')
            output = await response.text()
        await message.channel.send(output)


def setup(bot):
    bot.add_cog(Brain(bot))
