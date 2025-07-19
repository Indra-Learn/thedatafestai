DROP TABLE IF EXISTS user;
CREATE TABLE user (
    id INTEGER PRIMARY KEY auto_increment,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    created_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS acronyms;
CREATE TABLE acronyms (
    id INTEGER NOT NULL PRIMARY KEY auto_increment,
    category VARCHAR(100) NULL,
    sub_category VARCHAR(100) NULL,
    abbreviation_name VARCHAR(20) NULL,
    full_name VARCHAR(100) NULL,
    description VARCHAR(300) NULL,
    created_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS daily_market_at_a_glance;
CREATE TABLE daily_market_at_a_glance (
    id INTEGER NOT NULL PRIMARY KEY auto_increment,
    item VARCHAR(100) NOT NULL,
    sub_item VARCHAR(100) NULL,
    category VARCHAR(100) NULL,
    sub_category VARCHAR(100) NULL,
    as_of_date VARCHAR(100) NOT NULL,
    ltp FLOAT NULL, 
    prev_price FLOAT NULL, 
    open_price FLOAT NULL, 
    high_price FLOAT NULL, 
    low_price FLOAT NULL,  
    trade_quantity FLOAT NULL,
    market_type varchar(30),
    perChange FLOAT NULL, 
    from_prevday_gapup_percent FLOAT NULL,
    from_prevday_gain_percent FLOAT NULL,
    created_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
