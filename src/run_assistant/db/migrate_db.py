from run_assistant.db.initialize_db import create_db, drop_tables

if __name__ == "__main__":
    tables_list = input("Enter the list of tables you want to migrate:\n").split(", ")
    print(tables_list)
    drop_tables(tables_list)
    create_db(tables_list)
