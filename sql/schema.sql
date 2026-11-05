-- GuardianAI v2: raw ingestion schema
DROP TABLE IF EXISTS transactions;
CREATE TABLE transactions (
    txn_id            BIGSERIAL PRIMARY KEY,
    txn_timestamp     TIMESTAMP NOT NULL,
    from_bank         TEXT NOT NULL,
    from_account      TEXT NOT NULL,
    to_bank           TEXT NOT NULL,
    to_account        TEXT NOT NULL,
    amount_received   NUMERIC(18,2) NOT NULL,
    receiving_currency TEXT NOT NULL,
    amount_paid       NUMERIC(18,2) NOT NULL,
    payment_currency  TEXT NOT NULL,
    payment_format    TEXT NOT NULL,
    is_laundering     SMALLINT NOT NULL
);

DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts (
    account_id_pk   BIGSERIAL PRIMARY KEY,
    bank_name       TEXT NOT NULL,
    bank_id         TEXT NOT NULL,
    account_number  TEXT NOT NULL,
    entity_id       TEXT NOT NULL,
    entity_name     TEXT NOT NULL
);

CREATE INDEX idx_txn_from_account ON transactions(from_account);
CREATE INDEX idx_txn_to_account ON transactions(to_account);
CREATE INDEX idx_txn_timestamp ON transactions(txn_timestamp);
CREATE INDEX idx_txn_is_laundering ON transactions(is_laundering);
CREATE INDEX idx_accounts_account_number ON accounts(account_number);
