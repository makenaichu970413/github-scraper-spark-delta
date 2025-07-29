# Library
from pyspark.sql import DataFrame, SparkSession

# Utils
from utils.constant import FOLDER_DELTA_REPO


def create_dataframe(df: DataFrame) -> DataFrame:

    new_df = df.select(
        "repo_url",
        "repo_name",
        "description",
        "website",
        "topics",
        "license",
        "code_of_conduct",
        "security_policy",
        "stars",
        "watchers",
        "forks",
        "contributors_total",
    ).distinct()

    print(f"\n\nrepo_df")
    new_df.show()

    return new_df


def export_delta_table(df: DataFrame) -> DataFrame:

    # Write repositories
    # or 'append'
    df.write.format("delta").mode("overwrite").save(FOLDER_DELTA_REPO)
    print(f'DELTA_EXPORTED "{FOLDER_DELTA_REPO}"')

    return df


def import_delta_table(spark: SparkSession) -> DataFrame:

    df = spark.read.format("delta").load(FOLDER_DELTA_REPO)
    print(f'\nDELTA_IMPORTED "delta_repo_df" from "{FOLDER_DELTA_REPO}"')
    df.show()

    return df
