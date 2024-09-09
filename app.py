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

def get_items():
    # Make connection to the database
    conn = get_db_connection();
    # Grab the cursor
    cur = conn.cursor();
    items = cur.execute('SELECT * FROM tbl_items').fetchall()
    # Close database connection
    cur.close(); 
    print ("[LOG] - Returning tables")
    # Return both datasets to the calling function
    return items; 

def search(search_data):
    conn = get_db_connection();
    print(f"Looking for deez {search_data}. Hasn't been found tho" )
    
    conn.execute('SELECT * FROM tbl_items WHERE item_name LIKE "%" ||?|| "%"')
    conn.commit()
    conn.close()

def filter_table(column, filter_contents):
    print(f"[LOG] - filtering table by {column} LIKE {filter_contents}")
    conn = get_db_connection();
    cur = conn.cursor();
    print(f"[LOG] - running sql: SELECT * FROM tbl_items WHERE {column} LIKE '%{filter_contents}%'")
    filtered_table = cur.execute(f"SELECT * FROM tbl_items WHERE {column} LIKE '%{filter_contents}%'").fetchall()
    return filtered_table


app = Flask(__name__, static_url_path='/assets', static_folder='assets')

@app.route("/", methods=['GET', 'POST'])
def index():
    # Default page view load all items for the user.    
    data = {};

    data = get_items();

    # Listen for data returning from the front end.
    if request.method == 'POST':
        action = request.form.get("action")
        
        
        if action == 'search':
            print("[LOG] - Processing POST request for filter")
            column = request.form.get("column")
            filter_contents = request.form.get("contents")
            filtered_table = filter_table(column, filter_contents)
            return render_template("base.html", items=filtered_table)

        
        if action == 'sort':
            print("[LOG] - Processing POST request for sort")
            
    
    return render_template("base.html", items=data)


# names is tags, tags is tbl tags

# running
if __name__ == "__main__":
    app.run(debug=True)
