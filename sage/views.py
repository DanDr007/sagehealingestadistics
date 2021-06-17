from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template,Context
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import cursor
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model
def home(request,id_usu):
    miconexion = mysql.connector.connect(user="b00e281ad2b01d",password="51b1bd74",host="us-cdbr-east-04.cleardb.com",database="heroku_a8c9e3b6160e545")
    cursor = miconexion.cursor()
    q = "select * from usuarios where id_usu = "+id_usu+""
    cursor.execute(q)
    rs=cursor.fetchone()
    nombre=rs[1]
    edad=rs[2]
    correo=rs[3]
    peso=rs[12]
    altura=rs[13]
    peso=rs[12]
    porcentaje1=rs[5]
    porcentaje2=rs[6]
    porcentaje3=rs[7]
    enf1=rs[8]
    enf2=rs[9]
    enf3=rs[10]
    try:
        imc=peso/altura**2
        mensaje="Tu IMC es de: "+str("{0:.2f}".format(imc))+""
    except:
        mensaje="Modifica tus datos para obtener el imc"
    q = "select probab from estad where id_usu = "+id_usu+" order by id_pro desc limit 5"
    cursor.execute(q)
    rz=cursor.fetchall()
    try :
        dato1=rz[0][0]
        dato2=rz[1][0]
        dato3=rz[2][0]
        dato4=rz[3][0]
        dato5=rz[4][0]
        dfEnfermedadY = pd.DataFrame()
        dfEnfermedadX = pd.DataFrame()
        dfEnfermedadY["Tiempo"] = [1,9,11,15,20]
        dfEnfermedadX["Enfermedades"] = [dato5,dato4,dato3,dato2,dato1]
        lr_multipleCG = linear_model.LinearRegression()
        lr_multipleCG.fit(dfEnfermedadX,dfEnfermedadY)

        dfPrediccionEnf = pd.DataFrame()
        dfPrediccionEnf["Enfermedades"] = [10]
        Y_predictEnf = lr_multipleCG.predict(dfPrediccionEnf)
        mens="Usted se enfermara en : "+str("{0:.2f}".format(Y_predictEnf[0][0]))+" dias"
    except:
        mens="Tiene que realizar 5 questionarios como minimo para ver su prediccion"
    doc_externo=open("plantilla\miPerfil.html")
    plt=Template(doc_externo.read())
    doc_externo.close()
    ctx=Context({"id_usu":id_usu,"nombre":nombre,"edad":edad,"correo":correo,"peso":peso,"altura":altura,"porcentaje1":porcentaje1,"porcentaje2":porcentaje2,"porcentaje3":porcentaje3,"enf1":enf1,"enf2":enf2,"enf3":enf3,"imcM":mensaje,"mens":mens})
    documento=plt.render(ctx)
    return HttpResponse(documento)