from app import app
from flask import request
from PIL import Image
from PIL import ImageOps
from io import BytesIO

import mysql.connector
import base64


connector = mysql.connector.connect(
    host='127.0.0.1',
    database='image-processing',
    user='root',
    password='1234'
)



# admin upload image
@app.route('/image-process/upload', methods=['GET', 'POST'])
def processing():
    fileRequest = request.files['image']
    imageRequest = Image.open(fileRequest.stream)
    imageCropped = cropImage(imageRequest)

    buffer = BytesIO()
    imageCropped.save(buffer, format="PNG")

    myCursor = connector.cursor()
    sqlQuery = "INSERT INTO photo(image_encoded) VALUES(%s)"
    imageEncoded = base64.b64encode(buffer.getvalue())
    listParameter = [imageEncoded]
    myCursor.execute(sqlQuery, listParameter)
    connector.commit()
    
    return imageEncoded




@app.route('/image-process/searching', methods=['GET', 'POST'])
def searchingImage():
    fileRequest = request.files["image"]
    imageRequest = Image.open(fileRequest.stream)
    
    

    myCursor = connector.cursor()
    
    sqlQuery = "select * from photo"
    myCursor.execute(sqlQuery)
    result = myCursor.fetchall()
    
    response = []
    for imageData in result:
        imageDecoded = base64.b64decode(str(imageData[1]))
        fileName = 'Decoded_' + str(imageData[0]) + '.png'
        compareResult = None
        with open(fileName, 'wb') as f:
            f.write(imageDecoded)
            imageArchive = Image.open(fileName)
            print("Trigger request " + str(imageData[0]) + str(imageRequest.size))
            print("Trigger archive " + str(imageData[0]) + str(imageArchive.size))

            imageCropped = cropImage(imageRequest)
            compareResult = compareImages(imageCropped, imageArchive)
            
            if compareResult == None:
                print("keepping error!")
                response.append("Vui lòng chọn ảnh màu và đúng định dạng '.png'")
            elif compareResult <= 10.0:
                response.append(imageData)

        
        # os.remove(fileName)
    print(len(response))
    return response



def compareImages(img1, img2):

    # Don't compare if images are different sizes.
    if (img1.size != img2.size) \
            or (img1.mode != img2.mode) \
            or (img1.getbands() != img2.getbands()):
        return None

    pairs = zip(img1.getdata(), img2.getdata())
    if len(img1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1 - p2) for p1, p2 in pairs)
    else:
        dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

    ncomponents = img1.size[0] * img1.size[1] * 3
    return (dif / 255.0 * 100) / ncomponents  # Difference (percentage)

def cropImage(imageSrouce):

    width, height = imageSrouce.size
    top = (height - 400) / 2
    bottom = (height - 400) / 2
    left = (width - 750) / 2
    right = (width - 750) / 2

    border = (left, top, right, bottom)
    return ImageOps.crop(imageSrouce, border)


if __name__ == "__main__":
    app.run()