three ways to manage a message queue using different MariaDB ifeatures :

1. rocksdb

2. blackhole + localhost semisync replication + schema name rewrite

3. innodb with sacrificed durability and script replayability

4. memory + sync_binlog=1



