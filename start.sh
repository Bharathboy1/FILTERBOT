if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Bharathboy1/FILTERBOT.git /FILTERBOT
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /FILTERBOT
fi 
cd/FILTERBOT
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
