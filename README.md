# Star Schema Implementation in Redshift Cluster

## Summary
This is a simple project to demonstrate how to implement a star schema model into a Redshift cluster on AWS. It was developed as a condition for approval in the Data Engineer nanodegree at [Udacity](https://www.udacity.com/course/data-engineer-nanodegree--nd027). 


### ETL Explained
This ETL job is meant to extract song data from two S3 buckets owned by Udacity, move it to 2 staging tables and load it into 5 tables arranged in star schema model. All the tables will be created in a AWS Redshift database.


## Hands-on

**Pre-requisites**
- AWS Reshift Cluster available and running with IAM Role to access S3 Bucket (ReadOnly)
- Python 3.x installed

### Environment Setup

1. Clone the repository (if not done already)
    ```shell
    git clone https://github.com/rc301/redshift-cluster-etl-demo.git
    cd redshift-cluster-etl-demo
    ```
2. Using a virtual environment (Optional)

    > Make sure `virtualenv` package is installed. For that, just run `pip install virtualenv` in a terminal window.

    To set up the python environment: 
    - Create and activate a virtual environment
        - In a terminal window (on Windows) run the following commands
            ```shell
            virtualenv <env_name>
            .\<env_name>\Scripts\activate
            ```

3. Install python packages
    ```shell
    pip install -r requirements.txt
    ```

4. Fill configuration file `dwh.cfg` with Redshift cluster information.
    ```conf
    [CLUSTER]
    HOST=<Your_Redshift_Cluster_Host>
    DB_NAME=<Your_Database_Name>
    DB_USER=<Your_Database_User>
    DB_PASSWORD=<Your_Database_Users_Password>
    DB_PORT=<Your_Database_Access_Port>

    [IAM_ROLE]
    ARN=<Your_Redshift_Role_with_ReadOnly_Access_to_S3_Bucket>

    [S3]
    LOG_DATA='s3://udacity-dend/log_data'
    LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
    SONG_DATA='s3://udacity-dend/song_data'
    ```

### Creating tables
Once the configuration file is completed, just run the `create_tables.py` file to create all tables needed for this demo.
```shell
python create_tables.py
```

### Loading data into Redshift cluster tables
Then run `etl.py` file to extract data from 2 data sources and load them into staging tables before finally loading them into 5 final tables.
```shell
python etl.py
```

## Delete 
After finished processing, the tables will contain all the data processed.
Don't forget to deactivate the virtual environment
```shell
deactivate
```

> Important to stop and delete Redshift cluster if it will not be used in this demo anymore.

This is just a demo to help users with datapipelines on AWS RedShift. It is not meant for production environments.