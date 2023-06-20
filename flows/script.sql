CREATE TABLE IF NOT EXISTS ph_raw
(    
id serial PRIMARY KEY, 
timestamp INTEGER NOT NULL, --  [0]
type TEXT NOT NULL,--  [1]
domain TEXT NOT NULL, --  [2]
client TEXT NOT NULL, --  [3]
forward TEXT NOT NULL, -- [4] need transform int to text
replyType INTEGER NOT NULL, -- [5]
duration REAL NOT NULL, -- [6]
UNIQUE (timestamp, type, domain, client, forward, replyType, duration)
);


CREATE TABLE IF NOT EXISTS ph_domain
(    
id serial PRIMARY KEY, 
domain TEXT NOT NULL, --  [2]
isProcessYN BOOLEAN NOT NULL,
UNIQUE (domain)
);


CREATE TABLE IF NOT EXISTS ph_domain_response
(    
id serial PRIMARY KEY, 
ph_domain_id INT NOT NULL,
method TEXT, -- either POST / GET
response TEXT,
status TEXT,

CONSTRAINT fk_domain
      FOREIGN KEY(ph_domain_id) 
	  REFERENCES ph_domain(id)
);

