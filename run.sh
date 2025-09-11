


source env/bin/activate
for i in {1..5}; do
   python3 main.py $i &
done