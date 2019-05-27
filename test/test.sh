curl 'localhost:50000/sample'

curl 'localhost:50000/tables'

curl 'localhost:50000/measurement/0/1558674701'
curl 'localhost:50000/measurement/0/1558674702'
curl 'localhost:50000/measurement/0/1558674700'

curl 'localhost:50000/measurements/0'
echo
curl 'localhost:50000/measurements/1'
echo
curl 'localhost:50000/measurements/2'
echo
curl 'localhost:50000/measurements/0?from=1558674702'
echo
curl 'localhost:50000/measurements/1?to=1558674702'
echo
curl 'localhost:50000/measurements/1?from=1558674702&to=1558674703'
echo
