# Library
from pyspark.sql import DataFrame, SparkSession

# Utils
from spark.GitHub.SparkSchema import schema_repo
from utils.constant import FOLDER_OUTPUT


def create_dataframe(spark: SparkSession) -> DataFrame:
    json_file = f"*.json"  # Load all scraped data
    json_path = f"{FOLDER_OUTPUT}/{json_file}"

    schema = schema_repo()

    df = spark.read.option("multiLine", True).schema(schema).json(json_path)

    print(f'DATAFRAME_LOAD Load all scraped data from "{json_path}"')
    df.show()

    print(f"DATAFRAME_SCHEMA")
    df.printSchema()

    return df


def data_unification():
    # df_clean = (df
    #     .withColumn("stars",
    #         F.when(
    #             F.col("stars").endswith("k"),
    #             (F.regexp_replace("stars", "k", "").cast("float") * 1000).cast("int")
    #         ).otherwise(F.col("stars").cast("int"))
    #     )
    #     .withColumn("forks",
    #         F.when(
    #             F.col("forks").endswith("k"),
    #             (F.regexp_replace("forks", "k", "").cast("float") * 1000).cast("int")
    #         ).otherwise(F.col("forks").cast("int"))
    #     )
    # )
    pass
