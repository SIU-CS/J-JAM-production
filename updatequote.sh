source djangofy/bin/activate

echo "Activated djangofy"




while true
do
  sleep 5
  python mhapsite/manage.py  quoteupdate please
  echo "Slept for 5 seconds"
done
