import pymysql
from app import app
from config import mySQL
from flask import jsonify
from flask import Flask, flash, request

import base64
import cv2



@app.route('/image-process', methods=['GET', 'POST'])
def processing():
    file = request.files['image']

    connection = mySQL.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    sqlQuery = "INSERT INTO photo1(image_file) VALUES(%s)"
    imageEncoded = base64.b64encode(file.read())
    bindData = (imageEncoded)
    cursor.execute(sqlQuery, bindData)
    connection.commit()
    response = jsonify({'base64Format': str(imageEncoded)[2:-1]})

    cursor.close()
    connection.close()

    return response



@app.route('/image-process/<id>')
def photo_show(id):
    try:
        conn = mySQL.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT image_file FROM photo1 WHERE id =%s", id)
        imgString = cursor.fetchone()

        response = jsonify(imgString)
        print("triggerr")
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
        

if __name__ == "__main__":
    app.run()