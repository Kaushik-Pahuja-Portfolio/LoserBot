pip install -r LoserBot/requirements.txt && nohup python3 LoserBot/LoserBot.py > loserbot.log 2> loserbot.err < /dev/null & echo $! > run.pid && exit
