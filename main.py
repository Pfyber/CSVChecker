import os
import csv
import codecs
import pandas as pd
import chardet
from flask import Flask, flash, request, redirect, url_for, render_template
from helper import vsiRazredi,dijakiPoRazredu,najdiRazred
from werkzeug.utils import secure_filename

#na linuxu spremeni v os.cwd()
UPLOAD_FOLDER = r'C:\Users\Luka\PycharmProjects\upload'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/test" , methods=['GET', 'POST'])
def test():
    select = request.form.get('razredi')
    print(str(select)) # just to see what select is
#glavni route
#očitno edini uporabljen route
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    #select = request.form.get('razredi')
   # print(str(select))  # just to see what select is



    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #začasno shrani .csv file
            path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #CSV odpkairanje
            data_initial = open(path, "r", encoding="utf-16")
            prisotni=[]
            odsotni=[]

            for i, d in enumerate(data_initial):
                if i==0:
                    pass
                else:
                    prisotni.append(d.split("\t")[0])
                    status=(d.split("\t")[1])
                    timestamp = (d.split("\t")[2])
                    print(timestamp)
            vsiDijaki = (dijakiPoRazredu(najdiRazred(prisotni)))
            for v in vsiDijaki:
                if v not in prisotni:
                    odsotni.append(v)

            #(print(intersection(vsiDijaki, prisotni)) )
            #tole ni potrebno
            data_initial.close()
            #zbriši osnovni CSV file
            os.remove(path)
            return render_template("odsotni.html", odsotni=odsotni)

    return render_template("index.html", razredi=vsiRazredi())

app.run()