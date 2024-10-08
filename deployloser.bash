pip install -r LoserBot/requirements.txt && kill -9 `cat run.pid` && nohup python3 LoserBot/LoserBot.py > /dev/null 2>&1 & echo $! > run.pid
