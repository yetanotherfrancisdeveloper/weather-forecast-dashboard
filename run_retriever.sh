#!/usr/bin/env bash

# Running script to create necessary tables in DB
if [ "$OSTYPE" == "msys" ]; then
  python create_tables.py
else
  python3 create_tables.py
fi

# Running the script to retrieve data and update the DB
if [ "$OSTYPE" == "msys" ]; then
  python retriever.py
else
  python3 retriever.py
fi