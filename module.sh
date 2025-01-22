echo "install module....."
sleep 0.5
clear
pip install  time
pip install requests
pip install subprocess
pip install psutil

clear

rm -rf xion 
clear
git clone https://github.com/danu99721/xion
cd xion 
python main.py
