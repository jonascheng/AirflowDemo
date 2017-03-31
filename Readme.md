# Cronjob to export GraphDB in Docker

## Build

As you update or add groovy script to export graph DB, you have to rebuild and push docker image.

```shell
$> docker build -t soocii/pepper-cron .
$> docker push soocii/pepper-cron
```

## Usage

```shell
$> docker run --name pepper-cron soocii/pepper-cron \
    [-g pepper.prod.backend.titan] \
    [-b soocii-table] \
    -d 20170323
```

* -g: specify graph table name, and `pepper.integ.backend.titan` by default.
* -b: specify S3 bucket name, and `soocii-integration-table` by default.
* -d: specify date to export in format `YYYMMDD`, 20170323, for example.

## Register as cronjob in Ubuntu

The entry of cronjob has been prepared, therefore you may simply add `pepper-cron.sh`.

## Hive Table Creation

### posted status
```
CREATE EXTERNAL TABLE `soocii_pepper_posted_status`(
  `status_creator` string,
  `status_id` string,
  `status_create_at` bigint,
  `status_create_at_precise` string,
  `status_update_at_precise` string,
  `status_comment_update_at_precise` string,
  `status_type` string,
  `status_visibility` string,
  `tag_name` string)
PARTITIONED BY (
  `day` string)
ROW FORMAT SERDE
  'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'field.delim'='\t',
  'line.delim'='\n',
  'serialization.format'='\t')
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://soocii-table/soocii_pepper/posted_status_table.tsv/'
TBLPROPERTIES (
  'transient_lastDdlTime'='1490352775');

MSCK REPAIR TABLE `soocii_pepper_posted_status`;
```

### commented status
```
CREATE EXTERNAL TABLE `soocii_pepper_commented_status`(
  `comment_creator` string,
  `comment_id` string,
  `comment_create_at` bigint,
  `comment_create_at_precise` string,
  `comment_update_at_precise` string,
  `status_creator` string,
  `status_id` string)
PARTITIONED BY (
  `day` string)
ROW FORMAT SERDE
  'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'field.delim'='\t',
  'line.delim'='\n',
  'serialization.format'='\t')
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://soocii-table/soocii_pepper/commented_status_table.tsv/'
TBLPROPERTIES (
  'transient_lastDdlTime'='1490352775');
  
MSCK REPAIR TABLE `soocii_pepper_commented_status`;
```

### liked status
```
CREATE EXTERNAL TABLE `soocii_pepper_liked_status`(
  `status_liker` string,
  `like_status_at` bigint,
  `like_status_at_precise` string,
  `status_id` string,
  `status_creator` string)
PARTITIONED BY (
  `day` string)
ROW FORMAT SERDE
  'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'field.delim'='\t',
  'line.delim'='\n',
  'serialization.format'='\t')
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://soocii-table/soocii_pepper/liked_status_table.tsv/'
TBLPROPERTIES (
  'transient_lastDdlTime'='1490352775');

MSCK REPAIR TABLE `soocii_pepper_liked_status`;
```

### friendship
```
CREATE EXTERNAL TABLE `soocii_pepper_friendship`(
  `fan` string,
  `follow_at` bigint,
  `follow_at_precise` string,
  `celebrity` string)
PARTITIONED BY (
  `day` string)
ROW FORMAT SERDE
  'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'field.delim'='\t',
  'line.delim'='\n',
  'serialization.format'='\t')
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://soocii-table/soocii_pepper/friendship_table.tsv/'
TBLPROPERTIES (
  'transient_lastDdlTime'='1490352775');

MSCK REPAIR TABLE `soocii_pepper_friendship`;
```

### game achievements
```
CREATE EXTERNAL TABLE `soocii_pepper_played_gameapp`(
  `player` string,
  `play_duration` bigint,
  `play_count` bigint,
  `play_at` bigint,
  `gameapp_pkg_name` string)
PARTITIONED BY (
  `day` string)
ROW FORMAT SERDE
  'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'field.delim'='\t',
  'line.delim'='\n',
  'serialization.format'='\t')
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://soocii-table/soocii_pepper/played_gameapp_table.tsv/'
TBLPROPERTIES (
  'transient_lastDdlTime'='1490352775');

MSCK REPAIR TABLE `soocii_pepper_played_gameapp`;
```

### reload table
```
MSCK REPAIR TABLE <tablename>;
```
## Detailed Processing Flow

* start up titan service in backgroud.
* export all of accounts from graph DB.
* replace `_LIST_ACCOUNT_ID_`and `_QUERY_SINCE_` in all groovy script files.
* execute each groovy script file except list_account_id.groovy and list_status_id.groovy.
* remove last line of returned map from groovy script file.
* convert map to tab separated file.
* copy outfiles to S3.

Please be noted, you have to retain the order of exported data even you'd like to export more information. Otherwise you have to clean up and export previous dates again.
