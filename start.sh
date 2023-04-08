if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Bharathboy/url-auto-delete-shortener.git /url-auto-delete-shortener
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /url-auto-delete-shortener
fi
cd /url-auto-delete-shortener
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
