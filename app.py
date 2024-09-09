from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error

def get_db_connection():
    """ Create conection to database """
    conn = None; 

    try:
        # Create connection to database
        conn = sqlite3.connect("assets/shop_data.db"); 
        print("[LOG] Connected"); 
        print("[LOG]", sqlite3.version); 
    except Error as er:
        print(er);

    # Enable row factory
    conn.row_factory = sqlite3.Row; 
    
    # Enforce referential Integrity
    sql = """
            PRAGMA foreign_keys = ON
            """
    conn.execute(sql);

    return conn;

def get_items(filter_column, filter_type):
    # Make connection to the database
    conn = get_db_connection();
    # Grab the cursor
    filter_column = filter_column
    filter_type = filter_type
    cur = conn.cursor();
    sql = """ SELECT * FROM tbl_items ORDER BY item_id ASC"""
    items = cur.execute(sql)
    # Close database connection
    cur.close(); 
    print ("[LOG] - Returning tables")
    # Return both datasets to the calling function
    return items; 

def search(search_data):
    conn = get_db_connection();
    print(f"Looking for deez {search_data}. Hasn't been found tho" )
    cur = conn.cursor();
    conn.execute('SELECT * FROM tbl_items WHERE item_name LIKE "%" ||?|| "%"')
    conn.commit()
    conn.close()


app = Flask(__name__, static_url_path='/assets', static_folder='assets')

@app.route("/", methods=['GET', 'POST'])
def index():
    # Default page view load all items for the user.   '
    filter_column = request.form.get(f"filter_column", "item_id") 
    filter_type = request.form.get(f"filter_column", "ASC") 

   
    # Listen for data returning from the front end.
    if request.method == 'POST':
        action = request.form.get("action")
        
        # 
        if action == 'search':
            print("[LOG] -  Processing POST request for search form")
            search_data = request.form.get("searchQuerry")
            print("[LOG] - ")
            search(search_data)
            return
        
        if action == 'filter':
            print("[LOG] - Processing POST request for filter")
        
        if action == 'sort':
            print("[LOG] - Processing POST request for sort")
            
    data = {};

    data = get_items(filter_column, filter_type);

    
    return render_template("base.html", items=data)


# names is tags, tags is tbl tags

# running
if __name__ == "__main__":
    app.run(debug=True)
