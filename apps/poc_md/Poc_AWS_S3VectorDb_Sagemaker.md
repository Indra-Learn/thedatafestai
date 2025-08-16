# Learn

# Reference:
1. Amazon S3 Vectors: The Game-Changer in AI Storage: https://builder.aws.com/content/310Be9aAICFTNEReeBYhfhVTmeF/amazon-s3-vectors-the-game-changer-in-ai-storage-you-cant-ignore

# AWS Services:

1. Amazon S3 Vectors:  
    1. the first cloud storage solution with native vector support at scale
    2. S3 Vectors lets you store, query, and manage vector embeddings directly in S3, cutting costs by up to 90% while keeping performance blazing fast.
2. Amazon Sagemaker:
    1. **SageMaker workflow:**
        1. `Label data:` Set up and manage labeling jobs for highly accurate training datasets within Amazon SageMaker, using active learning and human labeling
        2. `Build:` Connect to other AWS services and transform data in Amazon SageMaker notebooks.
        3. `Train:` Use Amazon SageMaker's algorithms and frameworks, or bring your own, for distributed training.
        4. `Tune:` Amazon SageMaker automatically tunes your model by adjusting multiple combinations of algorithm parameters.
        5. `Deploy:` After training is completed, models can be deployed to Amazon SageMaker endpoints, for real-time predictions.
        6. `Discover:` Find, buy, and deploy ready-to-use model packages, algorithms, and data products in AWS Marketplace.
    2. Benefits and features:
        1. Labeling raw data with active learning: Amazon SageMaker Ground Truth uses a machine learning model to automatically attempt to label training data. 
        2. Highly accurate training datasets: Active learning models from Amazon SageMaker Ground Truth provide a very high level of consistency and accuracy for training datasets
        3. Fully-managed notebook instances
        4. Highly-optimized machine learning algorithms
        5. One-click training
        6: Deployment without engineering effort



# Steps by steps:
1. **Cretae Bucket:**
    1. bucket name: `poc-sagemaker-vectordb`
    1. aws region: `us-east-1`
    2. bucket type: `General purpose`
    3. Object Ownership: `ACLs disabled`
    4. Block Public Access settings for this bucket: `check` for "Block all public access"
    5. Bucket Versioning: `Disable`
    6. Default encryption 

2. Create sub-folders in above created bucket:
    1. sub-folder name: `temp-poc-sagemaker-glue-db`, Required by AWS Glue for managed tables and Zero-ETL integrations.
    2. sub-folder name" `vector-data`, 

2. **Prepare AWS Glue:**
    1. Create Database: Visit `Data Catalog`
        1. database name: `poc-sagemaker-db`
        2. database settings -> location: `s3://poc-sagemaker-vectordb/temp-poc-sagemaker-glue-db/`

    1. Create Table: Visit `Data Catalog -> Tables`
        1. table name: `sagemaker_meta_table`
        2. database name (previously created): `poc-sagemaker-db`
        3. table format: `Standard AWS Glue table (default)` 
        4. data store: `S3`
        5. data location is specified in: `my account`
        6. include path: `s3://poc-sagemaker-vectordb/vector-data/`
        7. data format: `json`
        8. (step 2) schema: `Define or upload schema`

3. **Create Role:**
    1. (Step 1) enter role name: `role_sagemaker_datascientist`
    2. (Step 1) Select Persona: Data Scientist
    3. (Step 2) ML activities: Run Studion, Manage ML Jobs, Manage Models, Manage Glue Tables, Canvas
    4. (step 2)

