cd c:/Program Files/MongoDB/server/4.2/bin/

mongoimport --authenticationDatabase=admin -u admin -p admin -d COVID19 -c covid19_brasil --type csv --file C:\Temp\covid19_13-07-2020.csv --headerline