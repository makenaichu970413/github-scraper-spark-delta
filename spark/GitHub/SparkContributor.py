# Library
from pyspark.sql import DataFrame, SparkSession

# Utils
from utils.constant import FOLDER_DELTA_CONTRIBUTOR, FOLDER_DELTA_REPO


def create_dataframe(df: DataFrame) -> DataFrame:

    # Contributors table
    new_df = (
        df.selectExpr("repo_url", "explode(contributors) AS contributor")
        .select(
            "repo_url",
            "contributor.username",
            "contributor.profile_url",
            "contributor.email",
            "contributor.bio",
            "contributor.organizations",
        )
        .distinct()
    )

    print(f"\n\ncontributors_df")
    new_df.show()

    return new_df


def export_delta_table(df: DataFrame) -> DataFrame:

    # Write repositories
    # or 'append'
    df.write.format("delta").mode("overwrite").save(FOLDER_DELTA_CONTRIBUTOR)
    print(f'DELTA_EXPORTED "{FOLDER_DELTA_CONTRIBUTOR}"')

    return df


def import_delta_table(spark: SparkSession) -> DataFrame:

    df = spark.read.format("delta").load(FOLDER_DELTA_CONTRIBUTOR)
    print(f'\nDELTA_IMPORTED "delta_contributor_df" from "{FOLDER_DELTA_CONTRIBUTOR}"')
    df.show()

    return df
