if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Bharathboy1/FILTERBOT/tree/NEW-ONE.git /FILTERBOT/tree/NEW-ONE
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /FILTERBOT/tree/NEW-ONE
fiFILTERBOT/tree/NEW-ONE
cd/
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
