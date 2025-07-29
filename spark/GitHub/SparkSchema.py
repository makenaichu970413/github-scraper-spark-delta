from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    ArrayType,
    IntegerType,
)


def schema_repo() -> StructType:

    # Define schema for GitHub JSON structure
    schema = StructType(
        [
            StructField("repo_name", StringType(), True),
            StructField("repo_url", StringType(), True),
            StructField("description", StringType(), True),
            StructField("website", StringType(), True),
            StructField("topics", ArrayType(StringType()), True),
            StructField("license", StringType(), True),
            StructField("code_of_conduct", StringType(), True),
            StructField("security_policy", StringType(), True),
            StructField("stars", StringType(), True),
            StructField("watchers", StringType(), True),
            StructField("forks", StringType(), True),
            StructField("contributors", ArrayType(schema_contributor()), True),
            StructField("contributors_total", IntegerType(), True),
        ]
    )

    return schema


def schema_contributor() -> StructType:

    schema = StructType(
        [
            StructField("profile_url", StringType(), True),
            StructField("username", StringType(), True),
            StructField("email", StringType(), True),
            StructField("bio", StringType(), True),
            StructField("organizations", ArrayType(StringType()), True),
        ]
    )

    return schema
