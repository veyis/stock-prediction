CREATE DATABASE stock_app;

\c stock_app;

-- Users Table
CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    Username VARCHAR(50) UNIQUE,
    Password VARCHAR(50), -- Note: It's recommended to store hashed & salted passwords, not plain text.
    Email VARCHAR(50),
    DateRegistered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    LastLoginDate TIMESTAMP
);

-- Stocks Table
CREATE TABLE Stocks (
    Symbol VARCHAR(10) PRIMARY KEY,
    Name TEXT,
    MarketCap BIGINT,
    Country VARCHAR(50),
    IPOYear INTEGER,
    Sector VARCHAR(50),
    Industry VARCHAR(100)
);

-- StockPrices Table
CREATE TABLE StockPrices (
    Symbol VARCHAR(10) REFERENCES Stocks(Symbol),
    Date TIMESTAMP NOT NULL,
    OpeningPrice NUMERIC,
    ClosingPrice NUMERIC,
    High NUMERIC,
    Low NUMERIC,
    Volume BIGINT,
    PRIMARY KEY (Symbol, Date)
);

-- Suggestions Table
CREATE TABLE Suggestions (
    SuggestionID SERIAL PRIMARY KEY,
    Symbol VARCHAR(10) REFERENCES Stocks(Symbol),
    Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    SuggestedPrice NUMERIC,
    Recommendation VARCHAR(10),
    Rationale TEXT
);

-- UserPreferences Table
CREATE TABLE UserPreferences (
    PreferenceID SERIAL PRIMARY KEY,
    UserID INTEGER REFERENCES Users(UserID),
    PreferenceType VARCHAR(50),
    PreferenceValue VARCHAR(50)
);

-- UserStockWatchlist Table
CREATE TABLE UserStockWatchlist (
    WatchlistID SERIAL PRIMARY KEY,
    UserID INTEGER REFERENCES Users(UserID),
    Symbol VARCHAR(10) REFERENCES Stocks(Symbol),
    DateAdded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
