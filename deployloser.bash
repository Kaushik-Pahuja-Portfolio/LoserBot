pip install -r LoserBot/requirements.txt
kill -9 `cat run.pid` 
nohup python3 LoserBot/LoserBot.py > loserbot.log 2> loserbot.err < /dev/null & echo $! > run.pid && exit
