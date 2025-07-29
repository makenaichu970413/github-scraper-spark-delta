# Spark
from spark.GitHub import SparkRepo, SparkContributor, SparkInit, SparkData


def run():

    spark = SparkInit.init()
    df = SparkData.create_dataframe(spark)

    df_repo = SparkRepo.create_dataframe(df)
    SparkRepo.export_delta_table(df_repo)
    df_delta_repo = SparkRepo.import_delta_table(spark)

    df_contributor = SparkContributor.create_dataframe(df)
    SparkContributor.export_delta_table(df_contributor)
    df_delta_contributor = SparkContributor.import_delta_table(spark)

    spark.stop()


# In Power Shell, force the use of the system `JAVA_HOME` by:
# JAVA
# $env:JAVA_HOME = [System.Environment]::GetEnvironmentVariable('JAVA_HOME', 'Machine')
# $env:Path = "$($env:JAVA_HOME)\bin;" + $env:Path
# java --version
# $env:Path += ';C:\Program Files\Java\jdk-17'

# Hadoop
# Test-Path "C:\Program Files\Hadoop\hadoop-3.3.6\bin\winutils.exe"
# $env:Path += ';C:\Program Files\Hadoop\hadoop-3.3.6\bin'
# winutils version

#! RESTART COMPUTER


"""
Security Restrictions: Java 24 introduced stronger security restrictions. 
The method Subject.getSubject() is now considered a restricted method that 
requires explicit permission (--enable-native-access=ALL-UNNAMED) which 
wasn't enabled.

https://github.com/cdarlint/winutils/tree/master
"""
