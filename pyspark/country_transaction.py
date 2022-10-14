#!/usr/bin/python3

from pyspark.sql import SparkSession
import sqlparse

spark = SparkSession \
    .builder \
    .master('spark://Yevadrian.localdomain:7077') \
    .appName('project') \
    .config('spark.jars', '/etc/postgresql/14/main/postgresql-42.5.0.jar') \
    .getOrCreate()

df_transaction = spark.read \
    .format('jdbc') \
    .option('url', 'jdbc:postgresql://localhost:5432/postgres') \
    .option('dbtable', 'transaction') \
    .option('user', 'postgres') \
    .option('password', 'postgres') \
    .option('driver', 'org.postgresql.Driver') \
    .load()

df_customer = spark.read \
    .format('jdbc') \
    .option('url', 'jdbc:postgresql://localhost:5432/postgres') \
    .option('dbtable', 'customer') \
    .option('user', 'postgres') \
    .option('password', 'postgres') \
    .option('driver', 'org.postgresql.Driver') \
    .load()

query = sqlparse.format(open('/mnt/c/etl_project/queries/country_transaction.sql', 'r'))

df_transaction.createOrReplaceTempView('transaction')
df_customer.createOrReplaceTempView('customer')
results = spark.sql(f'{query}')
results.show(20)
results.toPandas().to_csv('/mnt/c/etl_project/output/pyspark/country_transaction.csv', index=False)