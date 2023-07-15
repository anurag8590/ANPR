from tkinter import *
from PIL import Image,ImageTk
from tkinter import filedialog as tkFileDialog
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr

def select_image():
    global panelA,panelB

    path = tkFileDialog.askopenfilename()

    if len(path)>0 :
        
        image = cv2.imread(path)
        image_copy = np.copy(image)
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

        bfilter = cv2.bilateralFilter(gray,11,17,17)
        edged = cv2.Canny(bfilter,35,250)

        keypoints = cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours,key=cv2.contourArea,reverse=True)[:10]


        location = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour,10,True)
            if len(approx)==4:
                location = approx
                break

        mask = np.zeros(gray.shape,np.uint8)
        new_image = cv2.drawContours(mask,[location],0,255,-1)
        new_image = cv2.bitwise_and(image,image,mask=mask)


        (x,y) = np.where(mask==255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2+1, y1:y2+1]


        reader = easyocr.Reader(['en'])
        result = reader.readtext(cropped_image)

        print(result)

        text = ""

        for i in result:
            for j in i:
                if type(j)==str and len(j)>=10:
                    text = j

        state = text[:2]

        states = {'CG' : 'Chattisgarh','AN':'Andaman and Nicobar','AP':'Andhra Pradesh','AS':'Assam','AR':'Arunachal Pradesh','BR':'Bihar','CH':'Chandigarh','DD':'Daman and Diu','DL':'Delhi','GA':'Goa',
        'GJ':'Gujrat','HR':'Haryana','HP':'Himachal Pradesh','JK':'Jammu and Kashmir','JH':'Jharkhand','KA':'Karnataka','KL':'Kerala','LA':'Lakshadweep','MP':'Madhya Pradesh','MH':'Maharastra','MN':'Manipur',
        'ML':'Meghalaya','MZ':'Mizoram','NL':'Nagaland','OD':'Odisha','PY':'Puducherry','PB':'Punjab',
        'RJ':'Rajasthan','SK':'Sikkim','TN':'Tamil Nadu','TS':'Telangana','TR':'Tripura',
        'UP':'Uttar Pradesh','UK':'Uttarakhand','WB':'West Bengal'}

        new_text = ""
        if state in states:
            new_text = states[state]
        else :
            new_text = "Nothing"

        font = cv2.FONT_HERSHEY_SIMPLEX
        res = cv2.putText(image, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
        res = cv2.rectangle(image, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
        res = cv2.putText(image,text='Vehicle belongs to '+ new_text,org=(approx[0][0][0]-80, approx[1][0][1]-100), fontFace=font, fontScale=0.8, color=(0,255,0), thickness=1, lineType=cv2.LINE_AA)
        
        image_copy = cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)

        image_copy = Image.fromarray(image_copy) 
        res = Image.fromarray(res)

        image_copy = ImageTk.PhotoImage(image_copy)
        res = ImageTk.PhotoImage(res)

        

        if panelA is None or panelB is None:
                
            panelA = Label(image=image_copy)
            panelA.image = image_copy
            panelA.pack(side="left", padx=50, pady=50)
                
            panelB = Label(image=res)
            panelB.image = res
            panelB.pack(side="right", padx=50, pady=50)
            
        else:
                
            panelA.configure(image=image_copy)
            panelB.configure(image=res)
            panelA.image = image_copy
            panelB.image = res

root = Tk()
root.state('zoomed')
root.title('ANPR')
panelA = None
panelB = None

text = Label(root,text='Automatic Number Plate Recognition',font = ('Times New Roman',30),height = 2, width = 50 ,fg = "#FF0000" )
text.pack()

org_text = Label(root,text = 'Original Image',font =('Times New Roman',15),width = 15)
org_text.pack(side = "left")

result_text = Label(root,text='Result Image',font=('Times New Roman',15),width = 15)
result_text.pack(side = "right")

btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom",padx="10", pady="10")

root.mainloop()

