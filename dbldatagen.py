# Databricks notebook source
# DBTITLE 1,Install necessary Libraries
# MAGIC %pip install dbldatagen Faker

# COMMAND ----------

# DBTITLE 1,Import Libraries
from dbldatagen import DataGenerator
from faker import Faker
from pyspark.sql.types import StringType, IntegerType
import pyspark.sql.functions as F

# COMMAND ----------

# DBTITLE 1,First Data Generation
dataGen = (DataGenerator(spark, rows=100, partitions=4)
           .withIdOutput()
           .withColumn("name", StringType(), values=["Vikram", "Tamanna", "Rani", "Sita", "Suresh"])
           .withColumn("country", StringType(), values=["India", "Canada", "USA"])
           .withColumn("age", IntegerType(), minValue=18, maxValue=65, random=True)
           )

df = dataGen.build()
display(df)


# COMMAND ----------

# DBTITLE 1,Generating Weighted Data
dataGen = (DataGenerator(spark, rows=100, partitions=4)
           .withIdOutput()
           .withColumn("name", "string", 
                       values=["Vikram", "Tamanna", "Rani", "Sita", "Suresh"], 
                       weights=[5, 4, 9, 1, 8], random=True))
df = dataGen.build()
display(df)


# COMMAND ----------

# DBTITLE 1,Data Spread
display(df.groupBy('name').count())

# COMMAND ----------

# DBTITLE 1,Using Third-Party Library (Faker)
faker = Faker()
row_num = 100
dataGen = (DataGenerator(spark, rows=row_num, partitions=4)
           .withIdOutput()
           .withColumn("name", StringType(), values=[faker.name() for _ in range(row_num)], random=True)
           .withColumn("company", StringType(), values=[faker.company() for _ in range(row_num)], random=True))

df = dataGen.build()
display(df)


# COMMAND ----------

# DBTITLE 1,wrong way of generating faker
row_num = 100
dataGen = (DataGenerator(spark, rows=row_num, partitions=4)
           .withIdOutput()
           .withColumn("name", expr=f"'{fake.name()}'")
           .withColumn("company", expr=f"'{fake.company()}'"))

df = dataGen.build()
display(df)

# COMMAND ----------

# DBTITLE 1,Generating using SQL Expression
dataGen = (DataGenerator(spark, rows=100, partitions=4)
           .withIdOutput()
           .withColumn("transaction_id", "string", expr="uuid()")
           .withColumn("original_price", "float", minValue=10.0, maxValue=500.0, random=True)
           .withColumn("discount_rate", "float", values=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5], random=True)
           .withColumn("discounted_price", "float", expr="original_price * (1 - discount_rate)"))
df = dataGen.build()
display(df)
