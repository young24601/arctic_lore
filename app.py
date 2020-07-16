import os
import sqlite3
import re
from flask import request
#from flask import g
from flask import Flask
from flask import render_template

app = Flask(__name__)
db_path = os.path.dirname(__file__) + '/arctic.db'

def sql_execute(sql, conn=None, as_dictionary=False):
    if not conn:
        try:
            conn = sqlite3.connect(db_path)
        except sqlite3.Error:
            return
    try:
        cur = conn.cursor()
        cur.execute(sql)
        if as_dictionary:
            cols = [i[0] for i in cur.description]
            rows = [dict(zip(cols,row)) for row in cur]
        else:
            rows = cur.fetchall()
    finally:
        conn.close()
    return rows

@app.route('/')
def index():
    result = sql_execute("select count(*) from Lore")
    ct = list(result[0])[0]
    print(f'Total number of items is {ct}')
    return render_template("index.html")

@app.route('/get_lores')
def get_lores():
    text = request.args.get('keywords')
    spl = re.split("[\.\s]", text.replace("'", "''"))
    sql = "select * from Lore where " + "object_name like '%" + "%' and object_name like '%".join(spl)
    sql += "%'"

    results = sql_execute(sql, as_dictionary=True)

    results_string = ""
    result_count = 0
    for row in results:
        line = f'<pre id="pre_{result_count}" onClick=moveItem(pre_{result_count})>'
        result_count+=1
        line += f'Object {str(row["OBJECT_NAME"])} <br />'

        if row["ITEM_TYPE"] is not None:
            line += f'Item Type: {str(row["ITEM_TYPE"])} <br />'
        if row["MAT_CLASS"] is not None and row["MATERIAL"] is not None:
            line += f'Mat Class: {str(row["MAT_CLASS"]):<10} Material: {str(row["MATERIAL"])} <br />'
        if row["WEIGHT"] is not None and row["ITEM_VALUE"] is not None:
            line += f'Weight   : {str(row["WEIGHT"]):<10} Value   : {str(row["ITEM_VALUE"])} <br />'
        if row["CAPACITY"] is not None:
            line += f'Capacity : {str(row["CAPACITY"])} <br />'
        if row["AFFECTS"] is not None:
            for affect in re.split(",", row["AFFECTS"]):
                line += f'Affects  : {str(affect.strip())} <br />'
        if row["EFFECTS"] is not None:
            for effect in re.split(",", row["EFFECTS"]):
                line += f'Effects : {str(effect.strip())} <br />'
        if row["ITEM_IS"] is not None:
            line += f'Item is  : '
            for item_is in re.split(" ", row["ITEM_IS"]):
                line += f'{item_is} '
            line += f'<br />'
        if row["CHARGES"] is not None:
            line += f'Charges  : {str(row["CHARGES"])} <br />'
        if row["ITEM_LEVEL"] is not None:
            line += f'Level    : {row["ITEM_LEVEL"]} <br />'
        if row["APPLY"] is not None:
            line += f'Apply    : {str(row["APPLY"])} <br />'
        if row["RESTRICTS"] is not None:
            line += f'Restricts: '
            for restrition in re.split(" ", row["RESTRICTS"]):
                line += f'!{restrition} '
            line += f'<br />'
        if row["CLASS"] is not None:
            line += f'Class    : {row["CLASS"]} <br />'
        if row["IMMUNE"] is not None:
            line += f'Immune   : '
            for immunity in re.split(" ", row["IMMUNE"]):
                line += f'{immunity} '
            line += f'<br />'
        if row["DAMAGE"] is not None:
            line += f'Damage   : {str(row["DAMAGE"])} <br />'
        line += "<br />***************<br />"

        results_string += line + "</pre>"

    return results_string
