cp ~/pgsql/wyvern/pg_hba.conf ~/pg_hba.conf
rm ~/pgsql/wyvern/ -r
initdb -D /home/ryan/pgsql/wyvern
cp ~/pg_hba.conf /home/ryan/pgsql/wyvern

