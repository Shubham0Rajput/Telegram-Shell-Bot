import logging
import subprocess
from subprocess import Popen, PIPE 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
	update.message.reply_text('Hi! use /cmd or /cmdR to enter command')


def help(update, context):
	update.message.reply_text('/start- To Start the Bot \n /help- To Know About the Commands \n '
	'/cmdR [COMMAND]- To Run Shell {WHEN REALTIME OUTPUT REQUIRED} \n'
	'/cmd [COMMAND]- To perform command \n')


def error(update, context):
	logger.warning('Update "%s" caused error "%s"', update, context.error)



def cmdR(update, context):
	txt=update.message.text 
	if "/cmdR" == txt.strip()[:5]:
		command = " ".join(txt.strip().split(" ")[1:])
	else :
		update.message.reply_text("Enter Correct Command")  
	
	for path in run(command):
		print(path)
		update.message.reply_text(path)


def cmd(update, context):
	txt=update.message.text 
	if "/cmd" == txt.strip()[:4]:
		command = " ".join(txt.strip().split(" ")[1:])
	else :
		update.message.reply_text("Enter Correct Command")  
	update.message.reply_text(subprocess.check_output(command))

def run(command):
	process=Popen(command,stdout=PIPE,shell=True)
	while True:
		line=process.stdout.readline().rstrip()
		if not line:
			break
		yield line


def main():
	updater = Updater("TOKEN", use_context=True)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("cmd", cmd))
	dp.add_handler(CommandHandler("cmdR", cmdR))

	dp.add_error_handler(error)
	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()
