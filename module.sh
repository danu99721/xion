echo "install module....."
sleep 0.5
clear
pkg install python-pip 
pkg install python
pkg install python2
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
