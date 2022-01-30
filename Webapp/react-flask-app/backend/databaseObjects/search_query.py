def save_search_query(db, data):
    data.to_sql('search_query', con=db.engine, if_exists='append', chunksize=1000, index=False)
