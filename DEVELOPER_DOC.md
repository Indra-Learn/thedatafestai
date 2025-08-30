# Developer Guide - Handbook

Welcome to the `Developer Guide`

## How to use this application (Windows Machine):

1. Clone the Git Repo:
    ```shell
    git clone https://github.com/Indra-Learn/thedatafestai.git
    cd thedatafestai
    ```
2. Set the Github-Remote url:
    ```shell
    git remote set-url origin https://easycloudapi:<personal_access_token_start_with_ghp>@github.com/Indra-Learn/thedatafestai.git
    git config --global user.email "you@example.com"
    git config --global user.name "Your Name"
    ```
2. Create & Activate the Python Virtual Environment:
    ```shell
    python -m venv .venv
    .venv\Scripts\activate
    ```
3. Change the scope
    ```shell
    # open windows Powershell with "Run as administrator"
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

    # or
    # Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
    ```
3. Install the packages:
    ```shell
    python -m ensurepip
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    ```
4. Run the app
    ```shell
    flask --app apps run --debug
    ```


## Support Document Links:

1. Web Application:
    1. Flask Official Doc: https://flask.palletsprojects.com/en/stable/
2. Storage & Database:
    1. TiDB:
        1. https://docs.pingcap.com/tidb/stable/dev-guide-sample-application-python-sqlalchemy/
        2. https://www.pingcap.com/blog/getting-started-with-tidb-cloud-using-python-and-flask/
    2. Backblaze:
    3. db4free:
3. GCP:
    1. Secret Manager: https://cloud.google.com/secret-manager/docs/authentication