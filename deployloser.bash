pip install -r LoserBot/requirements.txt && if [-f run.pid]; then kill -9 `cat run.pid` fi && nohup python3 LoserBot/LoserBot.py > loserbot.log 2> loserbot.err < /dev/null & echo $! > run.pid && exit
