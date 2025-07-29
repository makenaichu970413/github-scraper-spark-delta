# Library
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from delta import configure_spark_with_delta_pip
import getpass
import os

# Utils
from utils.constant import FOLDER_SPARK_TEMP


def init() -> SparkSession:

    os.environ["HADOOP_USER_NAME"] = getpass.getuser()
    os.environ["HADOOP_SECURITY_AUTHENTICATION"] = "simple"
    os.environ["JAVA_HOME"] = "C:\\Program Files\\Java\\jdk-17"
    os.environ["HADOOP_HOME"] = "C:\\Program Files\\Hadoop\\hadoop-3.3.6"
    print(f"Using JAVA_HOME: {os.environ['JAVA_HOME']}")
    print(f"Using HADOOP_HOME: {os.environ['HADOOP_HOME']}")

    # Configuration
    spark_builder = (
        SparkSession.builder.appName("GitHubSpark")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        .config("spark.cleaner.referenceTracking.cleanCheckpoints", "true")
        .config("spark.local.dir", FOLDER_SPARK_TEMP)
    )

    spark = configure_spark_with_delta_pip(spark_builder).getOrCreate()

    print(f"SPARK_VERSION: {spark.version}")

    return spark
