set -x
mkdir -p Log/

pip3 install -r /requirements.txt

if [ $DEBUG -eq 1 ]
then
   /usr/bin/tail -f /dev/null
fi
python3 main.py