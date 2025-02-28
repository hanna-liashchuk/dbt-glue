## v1.6.2
- support Hudi, Delta, Iceberg natively supported in Glue through datalake_format parameter
- upgrade default Glue version to 4.0
- Support delta tables in Athena managed by Lake Formation

## v1.6.1
- adding support for database AWS Lake Formation tag management
- fix the boto3 version to use lakeformation tags 
- Fixed msck repair call for Delta non-partitioned tables
- re-use the glue-session to run multiple dbt run commands

## v1.6.0
- adding support for AWS Lake Formation tag management
- adding support for AWS Lake Formation data filtering and row, column, cell level security
- add compatibility with dbt 1.6
- fix Snapshot for Hudi

## v1.5.3
- use session to build client
- enable data skipping using hudi metadata in read path
- enable models to substitute sql with pyspark variables

## v1.5.2
- fix the naming for query execution timeout
- add assumeRole feature for AWS API Call
- fix get response for insert_overwrite issue

## v1.5.1
- Replace delete session per stop session

## v1.5.0
- add compatibility with dbt 1.5
- add multithreading
- add hudi bulk insert shuffle parallelism
- fix hudi snapshots without parameters

## v1.4.23
- run pre_hooks before create tmp table

## v1.4.22
- fix typos in sample_profiles.yml and README.md

## v1.4.21
- add Hudi related extensions #167 
- add  add execute_pyspark capability for registering python/pyspark UDFs #163 

## v1.4.1
- add compatibility with dbt 1.4.1

## v1.4.0
- add compatibility with dbt 1.4.0

## v1.3.14
- Fix HUDI merge strategy

## v1.3.13
- Fix exception handling for correct DBT report
- Update READEME.md to use Apache Iceberg Connector for AWS Glue v0.14.0

## v1.3.12
- add ability to override any hudi option

## v1.3.11
- add details on Iceberg documentation (provide details on commit locking, catalog alias. Provide least privilege IAM Permission for DynamoDB Commit Locking. Correct typos)
- add customizable DynamoDB table name for Iceberg Commit Locking.
- Refactoring of unused --conf parameter for Iceberg file format (warehouse_path)

## v1.3.10
- Fix error catching for seed feature


## v1.3.9
- implementation of Iceberg append, merge, and insert_overwrite operation and refacto of the existing create and create or replace implementation.
- add method to create dbt snapshots from Iceberg tables
- update README.md


## v1.3.8
- add __version__.py to fix `dbt --version`


## v0.3.7
- improve support for Boto backoff and retry logic

## v0.3.6
- improvement of seed
- add seed_format and seed_mode to configuration

## v0.3.5
- Add error checking for HUDI incremental materializations
- Specify location for tmp table

## v0.3.4

- Add method to create a default location for Iceberg without using final trailing slash.
  The fix will make Iceberg tables readable from query engines like Trino.

## v0.3.3

- Add support for Iceberg table materializion, and iceberg_table_replace materializion

## v0.3.2

- Added default_arguments param for Glue to add custom Glue configuration options. 

## v0.3.1 

- Include config `full_refresh` flag when materialization is incremental

## v0.3.0
- Updated dependencies to support dbt-core 1.3.0


## v0.2.15

- Force database parameter must be omitted or have the same value as schema  [Github Issue Link](https://github.com/aws-samples/dbt-glue/issues/93)

## v0.2.14

- Fix duplicates when using partitions changes with Hudi/Merge incremental materialization  [Github Issue Link](https://github.com/aws-samples/dbt-glue/issues/90)

## v0.2.12

- Added a function to add an end space in case of single quote at the end of a query. Ex: WHERE column='foo' [Github Issue Link](https://github.com/aws-samples/dbt-glue/issues/87)

## v0.2.11

- [#80](https://github.com/aws-samples/dbt-glue/pull/80): Fix default glue version on documentation
  - Changing default glue version and fixing a typo. [Github Issue Link](https://github.com/aws-samples/dbt-glue/issues/80)
  - Changing on Readme file the pip and python commands by python3 and pip3. This resolves potential issues when python2 is installed too.

## v0.2.1

- [#45](https://github.com/aws-samples/dbt-glue/pull/45): Modified Connection argument for Glue Session and table relation information for incremental mode
  - Modified Connection argument for Glue Session
  - Updated get_relation method to return relation as dict instead of list. [Github Issue Link](https://github.com/aws-samples/dbt-glue/issues/52)
  - Added Conf param for Glue to add custom spark configuration options.
  - Updated glue.sql.sources.partitionOverwriteMode to spark.sql.sources.partitionOverwriteMode to work partition overwrite properly.
- Override default types for STRING from TEXT to STRING
