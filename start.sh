if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Bharathboy/url-auto-delete-shortener-bot.git /url-auto-delete-shortener-bot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /url-auto-delete-shortener-bot
fi
cd /url-auto-delete-shortener-bot
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
##if [ -z $UPSTREAM_REPO ]

#then

  #echo "Cloning main Repository"
#
  #git clone https://github.com/LazyDeveloperr/LazyPrincess.git /LazyPrincess

#else

  #echo "Cloning Custom Repo from $UPSTREAM_REPO "

  #git clone $UPSTREAM_REPO /LazyPrincess

#fi

#cd /LazyPrincess

#pip3 install -U -r requirements.txt

#echo "Starting Bot...."

#python3 bot.py
