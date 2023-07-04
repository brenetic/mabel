import json
import telegram
import os
import logging


logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)

OK_RESPONSE = {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps('ok')
}
ERROR_RESPONSE = {
    'statusCode': 400,
    'body': json.dumps('nope')
}


def configure_telegram():
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not TELEGRAM_BOT_TOKEN:
        logger.error('Missing TELEGRAM_BOT_TOKEN')
        raise NotImplementedError

    return telegram.Bot(TELEGRAM_BOT_TOKEN)


def handler(event, _context):
    bot = configure_telegram()
    logger.info('Event: {}'.format(event))
    body = json.loads(event.get('body', {}))
    admin_id = int(os.environ.get('TELEGRAM_ADMIN_USER_ID'))

    if body.get('message', {}).get('from', {}).get('id', '') == admin_id:
        logger.info('Message received')
        update = telegram.Update.de_json(body, bot)
        chat_id = update.message.chat.id

        bot.sendMessage(chat_id=admin_id, text='Sup, {}'.format(update.message.from_user.username))
        logger.info('Message sent')

        return OK_RESPONSE

    return ERROR_RESPONSE
