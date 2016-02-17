cp ~/pgsql/anychat/pg_hba.conf ~/pg_hba.conf
rm ~/pgsql/anychat/ -r
initdb -D /home/ryan/pgsql/anychat
cp ~/pg_hba.conf /home/ryan/pgsql/anychat

