import psycopg2
import time

def postgres_connect():
    try:
        return psycopg2.connect(
            host="localhost",
            port= 5432,
            database="postgresdb",
            user="admin",
            password="password"
        )
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


def postgres_create_table(sql):
    with postgres_connect() as conn:
        conn.autocommit = True
        with conn.cursor() as curs:
            curs.execute(sql)


def data_insert(tbl, raw_dict):
    # add timer from start to finish
    tic = time.perf_counter()
    row = 0
    rows = len(raw_dict)
    print(f"number of rows to add: {rows}")
    # insert data into postgres
    with postgres_connect() as conn:
        conn.autocommit = True
        with conn.cursor() as curs:
            while row < rows:
                for d in raw_dict:
                    # create a list of values from the dictionary
                    values = list(d.values())
                    # create a list of column names from the dictionary
                    columns = list(d.keys())
                    # create a string of %s for the number of columns
                    s = ','.join(['%s' for _ in range(len(columns))])
                    # create a string of column names
                    cols = ','.join(columns)
                    # create the sql statement
                    sql = f'insert into cfb.{tbl} ({cols}) values ({s})'
                    # execute the sql statement
                    curs.execute(sql, values)
                    row += 1
            toc = time.perf_counter()
            print(f"inserted {row} rows in {toc - tic:0.4f} seconds")


def data_pull(tbl):
    with postgres_connect() as conn:
        conn.autocommit = True
        with conn.cursor() as curs:
            curs.execute(f'select * from cfb.{tbl}')
            dt = curs.fetchall()
            dt = [dict(zip([c[0] for c in curs.description], g)) for g in dt]
    return dt

