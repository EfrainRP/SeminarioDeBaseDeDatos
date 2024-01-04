'''
------------------------------------------------------------------------------
Proyecto: Odontologia 
Materia: SSPBD

//Tabla que controla quien puede hacer login en la BD
create table login_datos(
   iduser serial,
   usuario varchar(30),
   pass varchar(30),
   primary key(iduser)
);
'''
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import scrolledtext as st
from tkinter import  Tk, Button, Entry, Label, ttk, PhotoImage
from tkinter import  StringVar,END,HORIZONTAL,Frame,Toplevel
import time
from datetime import datetime
import sys
import psycopg2
from tkinter import *


class Paciente:

    def abrir(self):
        conexion = psycopg2.connect(database="proyecto", user="postgres", password='yourpassw')
        return conexion

    def alta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="insert into paciente(nombre, apellidoP, apellidoM, sexo, edad, domicilio, telefono, correo, ocupacion, residencia, origen, estado_civil, nombreSC, parentesco, domicilioSC, telefonoSC, cedula, tipo_sangre) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, datos)
        cone.commit()

    def consulta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select nombre, apellidoP, apellidoM, sexo, edad, domicilio, telefono, correo, ocupacion, residencia, origen, estado_civil, nombreSC, parentesco, domicilioSC, telefonoSC, cedula, tipo_sangre from paciente where IDpaciente=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()
    
    def consultaDoc(self,datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select nombre from doctor where cedula=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()


    def recuperar_todos(self):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select IDpaciente, nombre, apellidoP, apellidoM, sexo, edad, domicilio, telefono, correo, ocupacion, residencia, origen, estado_civil, nombreSC, parentesco, domicilioSC, telefonoSC, cedula, tipo_sangre from paciente"
        cursor.execute(sql)
        sql2 = "select * from paciente order by IDpaciente"
        cursor.execute(sql2)
        return cursor.fetchall()

    def baja(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="delete from paciente where IDpaciente=%s"
        cursor.execute(sql, datos)
        cone.commit()
        return cursor.rowcount # retornamos la cantidad de filas borradas

    def modificacion(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="update paciente set nombre=%s, apellidoP=%s, apellidoM=%s, sexo=%s, edad=%s, domicilio=%s, telefono=%s, correo=%s, ocupacion=%s, residencia=%s, origen=%s, estado_civil=%s, nombreSC=%s, parentesco=%s, domicilioSC=%s, telefonoSC=%s, cedula=%s, tipo_sangre=%s where IDpaciente=%s"
        cursor.execute(sql, datos)
        cone.commit()
        return cursor.rowcount # retornamos la cantidad de filas modificadas

class Formulario:
    def __init__(self):
        self.paciente1=Paciente() #Se llama a la clase declarada
        self.ventana1=tk.Tk()  #Se crea una ventana 
        self.ventana1.config(bg="dodger blue")
        self.ventana1.title("Clinica Odontologica")  #Titulo de la ventana
        self.ventana1.iconbitmap('odont.ico')
        self.cuaderno1 = ttk.Notebook(self.ventana1)   #Se crea un cuaderno en la ventana 
        
        img = PhotoImage(file='odt.png') 
        newimg=img.subsample(4)
        lbl_img = Label(self.ventana1, image=newimg).place(x=687,y=360)
        img2 = PhotoImage(file='odont2.png')
        newimg2=img2.subsample(5)
        lbl_img = Label(self.ventana1, image=newimg2).place(x=663,y=120)
        img1 = PhotoImage(file='odont1.png')
        newimg1=img1.subsample(2)
        lbl_img = Label(self.ventana1, image=newimg1).place(x=721,y=463)
        img3 = PhotoImage(file='dentalclinic.png')
        newimg3=img3.subsample(6)
        lbl_img = Label(self.ventana1, image=newimg3).place(x=797,y=10)
        
        etiq = Label(self.ventana1, text='Dra. Scarlett Valeria',bg='lawn green').place(x=690,y=55) 
        
        self.carga_Paciente()  #Metodos base
        self.consulta_por_codigo()
        self.listado_completo()
        self.borrado()
        self.modificar()

        style = ttk.Style()
        style.theme_use("classic")
        style.configure("TNotebook.Tab", background="green", font="helvetica 10")
        
        self.cuaderno1.grid(column=0, row=0, padx=60, pady=10) #Default 10x, 10y dimension del cuaderno
        self.ventana1.mainloop() #Ejecuta la ventana principal 
        

    def carga_Paciente(self):
        self.pagina1 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina1, text="Agregar pacientes")
        self.labelframe1=ttk.LabelFrame(self.pagina1, text="Paciente")        
        self.labelframe1.grid(column=0, row=0, padx=45, pady=10) #Default 5x, 10y
        self.label1=ttk.Label(self.labelframe1, text="-Nombre:") #Inicio nombre
        self.label1.grid(column=0, row=0, padx=4, pady=4) #Default 4x, 4y
        self.nombrepaciente=tk.StringVar()
        self.entrynombrepaciente=ttk.Entry(self.labelframe1, textvariable=self.nombrepaciente) 
        self.entrynombrepaciente.grid(column=1, row=0, padx=4, pady=4) #Default 4x, 4y -Fin nombre
        self.label2=ttk.Label(self.labelframe1, text="Apellido paterno:") #Inicio apellido paterno
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.apellidopaterno=tk.StringVar()
        self.entryapellidopaterno=ttk.Entry(self.labelframe1, textvariable=self.apellidopaterno)
        self.entryapellidopaterno.grid(column=1, row=1, padx=4, pady=4) #Default 4x, 4y -Fin apellidoP
        self.label3=ttk.Label(self.labelframe1, text="Apellido materno:") #Inicio apellido materno
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.apellidomaterno=tk.StringVar()
        self.entryapellidomaterno=ttk.Entry(self.labelframe1, textvariable=self.apellidomaterno)
        self.entryapellidomaterno.grid(column=1, row=2, padx=4, pady=4) #Default 4x, 4y -Fin apellidoM
        self.label4=ttk.Label(self.labelframe1, text="Sexo (H/M):") #Inicio sexo
        self.label4.grid(column=0, row=3, padx=4, pady=4)
        self.sexo=tk.StringVar()
        self.entrysexo=ttk.Entry(self.labelframe1, textvariable=self.sexo)
        self.entrysexo.grid(column=1, row=3, padx=4, pady=4) #Default 4x, 4y -Fin sexo
        self.label5=ttk.Label(self.labelframe1, text="Edad:") #Inicio edad
        self.label5.grid(column=0, row=4, padx=4, pady=4)
        self.edad=tk.StringVar()
        self.entryedad=ttk.Entry(self.labelframe1, textvariable=self.edad)
        self.entryedad.grid(column=1, row=4, padx=4, pady=4) #Default 4x, 4y -Fin edad
        self.label6=ttk.Label(self.labelframe1, text="Domicilio:") #Inicio domicilio
        self.label6.grid(column=0, row=5, padx=4, pady=4)
        self.domicilio=tk.StringVar()
        self.entrydomicilio=ttk.Entry(self.labelframe1, textvariable=self.domicilio)
        self.entrydomicilio.grid(column=1, row=5, padx=4, pady=4) #Default 4x, 4y -Fin domicilio
        self.label7=ttk.Label(self.labelframe1, text="Telefono:") #Inicio telefono
        self.label7.grid(column=0, row=6, padx=4, pady=4)
        self.telefono=tk.StringVar()
        self.entrytelefono=ttk.Entry(self.labelframe1, textvariable=self.telefono)
        self.entrytelefono.grid(column=1, row=6, padx=4, pady=4) #Default 4x, 4y -Fin telefono
        self.label8=ttk.Label(self.labelframe1, text="Correo:") #Inicio correo
        self.label8.grid(column=0, row=7, padx=4, pady=4)
        self.correo=tk.StringVar()
        self.entrycorreo=ttk.Entry(self.labelframe1, textvariable=self.correo)
        self.entrycorreo.grid(column=1, row=7, padx=4, pady=4) #Default 4x, 4y -Fin correo
        self.label9=ttk.Label(self.labelframe1, text="Ocupacion:") #Inicio ocupacion
        self.label9.grid(column=0, row=8, padx=4, pady=4)
        self.ocupacion=tk.StringVar()
        self.entryocupacion=ttk.Entry(self.labelframe1, textvariable=self.ocupacion)
        self.entryocupacion.grid(column=1, row=8, padx=4, pady=4) #Default 4x, 4y -Fin ocupacion
        self.label10=ttk.Label(self.labelframe1, text="Residencia:") #Inicio residencia
        self.label10.grid(column=0, row=9, padx=4, pady=4)
        self.residencia=tk.StringVar()
        self.entryresidencia=ttk.Entry(self.labelframe1, textvariable=self.residencia)
        self.entryresidencia.grid(column=1, row=9, padx=4, pady=4) #Default 4x, 4y -Fin residencia
        self.label11=ttk.Label(self.labelframe1, text="Origen:") #Inicio origen
        self.label11.grid(column=0, row=10, padx=4, pady=4)
        self.origen=tk.StringVar()
        self.entryorigen=ttk.Entry(self.labelframe1, textvariable=self.origen)
        self.entryorigen.grid(column=1, row=10, padx=4, pady=4) #Default 4x, 4y -Fin origen
        self.label12=ttk.Label(self.labelframe1, text="Estado civil:") #Inicio estadocivil
        self.label12.grid(column=0, row=11, padx=4, pady=4)
        self.estadocivil=tk.StringVar()
        self.entryestadocivil=ttk.Entry(self.labelframe1, textvariable=self.estadocivil)
        self.entryestadocivil.grid(column=1, row=11, padx=4, pady=4) #Default 4x, 4y -Fin estadocivil
        self.label13=ttk.Label(self.labelframe1, text="-Nombre segundo contacto:") #Inicio nombreSC
        self.label13.grid(column=0, row=12, padx=4, pady=4)
        self.nombreSC=tk.StringVar()
        self.entrynombreSC=ttk.Entry(self.labelframe1, textvariable=self.nombreSC)
        self.entrynombreSC.grid(column=1, row=12, padx=4, pady=4) #Default 4x, 4y -Fin nombreSC
        self.label14=ttk.Label(self.labelframe1, text="Parentesco:") #Inicio parentesco
        self.label14.grid(column=0, row=13, padx=4, pady=4)
        self.parentesco=tk.StringVar()
        self.entryparentesco=ttk.Entry(self.labelframe1, textvariable=self.parentesco)
        self.entryparentesco.grid(column=1, row=13, padx=4, pady=4) #Default 4x, 4y -Fin parentesco
        self.label15=ttk.Label(self.labelframe1, text="Domicilio segundo contacto:") #Inicio domicilioSC
        self.label15.grid(column=0, row=14, padx=4, pady=4)
        self.domicilioSC=tk.StringVar()
        self.entrydomicilioSC=ttk.Entry(self.labelframe1, textvariable=self.domicilioSC)
        self.entrydomicilioSC.grid(column=1, row=14, padx=4, pady=4) #Default 4x, 4y -Fin domicilioSC
        self.label16=ttk.Label(self.labelframe1, text="Telefono segundo contacto:") #Inicio telefonoSC
        self.label16.grid(column=0, row=15, padx=4, pady=4)
        self.telefonoSC=tk.StringVar()
        self.entrytelefonoSC=ttk.Entry(self.labelframe1, textvariable=self.telefonoSC)
        self.entrytelefonoSC.grid(column=1, row=15, padx=4, pady=4) #Default 4x, 4y -Fin telefonoSC
        self.label17=ttk.Label(self.labelframe1, text="-Cedula Dr:") #Inicio cedula
        self.label17.grid(column=0, row=16, padx=4, pady=4)
        self.cedula=tk.StringVar()
        self.entrycedula=ttk.Entry(self.labelframe1, textvariable=self.cedula)
        self.entrycedula.grid(column=1, row=16, padx=4, pady=4) #Default 4x, 4y -Fin cedula
        self.label18=ttk.Label(self.labelframe1, text="Tipo/sangre del paciente:\n            (A,B,O,AB)") #Inicio tipoSangre
        self.label18.grid(column=0, row=17, padx=4, pady=4)
        self.tiposangre=tk.StringVar()
        self.entrytiposangre=ttk.Entry(self.labelframe1, textvariable=self.tiposangre)
        self.entrytiposangre.grid(column=1, row=17, padx=4, pady=4) #Default 4x, 4y -Fin tipoSangre

        self.boton1=Button(self.labelframe1, text="Confirmar", bg="red", command=self.agregar) #Inicio boton agregar
        self.boton1.grid(column=1, row=18, padx=4, pady=4) #Default 4x, 4y -Fin boton
        self.boton2=Button(self.labelframe1, text="----> Informacion del doctor ", bg="deep sky blue",command=self.doctor) #Inicio boton doctor
        self.boton2.grid(column=4, row=18, padx=4, pady=4) #Default 4x, 4y -Fin boton
        self.boton3=Button(self.labelframe1, text="----> Informacion de citas ",  bg="deep sky blue", command=self.cita) #Inicio boton cita
        self.boton3.grid(column=4, row=19, padx=4, pady=4) #Default 4x, 4y -Fin boton
        self.boton4=Button(self.labelframe1, text="----> Informacion de tratamientos ", bg="deep sky blue", command=self.tratamiento) #Inicio boton cita
        self.boton4.grid(column=5, row=18, padx=4, pady=4) #Default 4x, 4y -Fin boton
        self.boton5=Button(self.labelframe1, text="----> Informacion de pagos ", bg="deep sky blue", command=self.pago) #Inicio boton cita
        self.boton5.grid(column=5, row=19, padx=4, pady=4) #Default 4x, 4y -Fin boton
        self.boton6=Button(self.labelframe1, text=" -Vacunas ",  bg="deep sky blue",command=self.vacunas) #Inicio boton cita
        self.boton6.grid(column=4, row=17, padx=4, pady=4) #Default 4x, 4y -Fin boton
        self.boton7=Button(self.labelframe1, text=" -Problemas cronicos ", bg="deep sky blue", command=self.problemas_cronicos) #Inicio boton cita
        self.boton7.grid(column=5, row=17, padx=4, pady=4) #Default 4x, 4y -Fin boton
        self.boton8=Button(self.labelframe1, text=" -Alergias ", bg="deep sky blue", command=self.alergias) #Inicio boton cita
        self.boton8.grid(column=6, row=17, padx=4, pady=4) #Default 4x, 4y -Fin boton


    def doctor(self):
        self.ventana1.destroy()
        aplicacion2=FormularioDoc() #Llama a la clase principal
    
    def cita(self):
        self.ventana1.destroy()
        aplicacion3=FormularioCita() #Llama a la clase principal

    def tratamiento(self):
        self.ventana1.destroy()
        aplicacion4=FormularioTratamiento() #Llama a la clase principal
    
    def pago(self):
        self.ventana1.destroy()
        aplicacion5=FormularioPago() #Llama a la clase principal
    
    def vacunas(self):
        self.ventana1.destroy()
        aplicacion6=FormularioVacunas() #Llama a la clase principal
    
    def problemas_cronicos(self):
        self.ventana1.destroy()
        aplicacion7=FormularioProblemas_cronicos() #Llama a la clase principal
    
    def alergias(self):
        self.ventana1.destroy()
        aplicacion8=FormularioAlergias() #Llama a la clase principal

    def agregar(self):
        if self.nombrepaciente.get() == '':
            mb.showinfo("Información", "Falta añadir el nombre del paciente.")
        elif self.apellidopaterno.get() == '' and self.apellidomaterno.get() == '':
            mb.showinfo("Información", "Debe añadir por lo menos un apellido.")
        elif len(self.sexo.get()) > 1 or self.sexo.get() == '':
            mb.showinfo("Información", "El sexo solo puede ser H o M.")
        elif self.edad.get() == '':
            mb.showinfo("Información", "Falta añadir la edad del paciente.")
        elif self.domicilio.get() == '':
            mb.showinfo("Información", "Falta añadir el domicilio del paciente.")
        elif self.telefono.get() == '':
            mb.showinfo("Información", "Debe añadir algun telefono del paciente.")
        elif self.nombreSC.get() == '':
            mb.showinfo("Información", "Debe añadir algun nombre de segundo contacto, o en su defecto poner ninguno.")
        elif self.parentesco.get() == '':
            mb.showinfo("Información", "Debe añadir algun parentesco, o en su defecto poner ninguno.")
        elif self.telefonoSC.get() == '':
            mb.showinfo("Información", "Debe añadir algun telefono del segundo contacto, o en su defecto poner ninguno.")
        elif self.tiposangre.get() == '' or (self.tiposangre.get() != 'O' and self.tiposangre.get() != 'o' and self.tiposangre.get() != 'A' and self.tiposangre.get() != 'a' and self.tiposangre.get() != 'AB'and self.tiposangre.get() != 'ab'and self.tiposangre.get() != 'b'and self.tiposangre.get() != 'B'):
            mb.showinfo("Información", "Sangre NO aceptada.")
        elif len(self.cedula.get()) > 0 or self.cedula.get() == '':
            datos=(self.cedula.get(), )
            respuesta=self.paciente1.consultaDoc(datos)
            if len(respuesta)>0:
                datos=(self.nombrepaciente.get(), self.apellidopaterno.get(),self.apellidomaterno.get(),self.sexo.get(),self.edad.get(),self.domicilio.get(),self.telefono.get(),self.correo.get(),self.ocupacion.get(),self.residencia.get(),self.origen.get(),self.estadocivil.get(),self.nombreSC.get(),self.parentesco.get(),self.domicilioSC.get(),self.telefonoSC.get(),self.cedula.get(),self.tiposangre.get())                 
                self.paciente1.alta(datos)
                mb.showinfo("Información", "Los datos fueron cargados con exito.")
                self.nombrepaciente.set("")
                self.apellidopaterno.set("")
                self.apellidomaterno.set("")
                self.sexo.set("")
                self.edad.set("")
                self.domicilio.set("")
                self.telefono.set("")
                self.correo.set("")
                self.ocupacion.set("")
                self.residencia.set("")
                self.origen.set("")
                self.estadocivil.set("")
                self.nombreSC.set("")
                self.parentesco.set("")
                self.domicilioSC.set("")
                self.telefonoSC.set("")
                self.cedula.set("")
                self.tiposangre.set("")
            else:
                mb.showinfo("Información", "Cedula invalida.")
        

    def consulta_por_codigo(self):
        self.pagina2 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina2, text="Consulta por código")
        self.labelframe1=ttk.LabelFrame(self.pagina2, text="Paciente")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe1, text="Código o ID:") #Inicio ID del paciente
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.codigo=tk.StringVar()
        self.entrycodigo=ttk.Entry(self.labelframe1, textvariable=self.codigo) 
        self.entrycodigo.grid(column=1, row=0, padx=4, pady=4)  #Fin ID paciente
        self.label2=ttk.Label(self.labelframe1, text="Nombre:") #Inicio nombre   
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.nombrepaciente1=tk.StringVar()
        self.entrynombrepaciente1=ttk.Entry(self.labelframe1, textvariable=self.nombrepaciente1, state="readonly")
        self.entrynombrepaciente1.grid(column=1, row=1, padx=4, pady=4) #Default: 4x,4y -Fin nombre
        self.label3=ttk.Label(self.labelframe1, text="Apellido Paterno:") #Inicio apellidoP  
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.apellidopaterno1=tk.StringVar()
        self.entryapellidopaterno1=ttk.Entry(self.labelframe1, textvariable=self.apellidopaterno1, state="readonly")
        self.entryapellidopaterno1.grid(column=1, row=2, padx=4, pady=4) #Default: 4x,4y -Fin apellidoP
        self.label4=ttk.Label(self.labelframe1, text="Apellido materno:") #Inicio apellido materno
        self.label4.grid(column=0, row=3, padx=4, pady=4)
        self.apellidomaterno1=tk.StringVar()
        self.entryapellidomaterno1=ttk.Entry(self.labelframe1, textvariable=self.apellidomaterno1, state="readonly")
        self.entryapellidomaterno1.grid(column=1, row=3, padx=4, pady=4) #Default 4x, 4y -Fin apellidoM
        self.label5=ttk.Label(self.labelframe1, text="Sexo (H/M):") #Inicio sexo
        self.label5.grid(column=0, row=4, padx=4, pady=4)
        self.sexo1=tk.StringVar()
        self.entrysexo1=ttk.Entry(self.labelframe1, textvariable=self.sexo1, state="readonly")
        self.entrysexo1.grid(column=1, row=4, padx=4, pady=4) #Default 4x, 4y -Fin sexo
        self.label6=ttk.Label(self.labelframe1, text="Edad:") #Inicio edad
        self.label6.grid(column=0, row=5, padx=4, pady=4)
        self.edad1=tk.StringVar()
        self.entryedad1=ttk.Entry(self.labelframe1, textvariable=self.edad1, state="readonly")
        self.entryedad1.grid(column=1, row=5, padx=4, pady=4) #Default 4x, 4y -Fin edad
        self.label7=ttk.Label(self.labelframe1, text="Domicilio:") #Inicio domicilio
        self.label7.grid(column=0, row=6, padx=4, pady=4)
        self.domicilio1=tk.StringVar()
        self.entrydomicilio1=ttk.Entry(self.labelframe1, textvariable=self.domicilio1, state="readonly")
        self.entrydomicilio1.grid(column=1, row=6, padx=4, pady=4) #Default 4x, 4y -Fin domicilio
        self.label8=ttk.Label(self.labelframe1, text="Telefono:") #Inicio telefono
        self.label8.grid(column=0, row=7, padx=4, pady=4)
        self.telefono1=tk.StringVar()
        self.entrytelefono1=ttk.Entry(self.labelframe1, textvariable=self.telefono1, state="readonly")
        self.entrytelefono1.grid(column=1, row=7, padx=4, pady=4) #Default 4x, 4y -Fin telefono
        self.label9=ttk.Label(self.labelframe1, text="Correo:") #Inicio correo
        self.label9.grid(column=0, row=8, padx=4, pady=4)
        self.correo1=tk.StringVar()
        self.entrycorreo1=ttk.Entry(self.labelframe1, textvariable=self.correo1, state="readonly")
        self.entrycorreo1.grid(column=1, row=8, padx=4, pady=4) #Default 4x, 4y -Fin correo
        self.label10=ttk.Label(self.labelframe1, text="Ocupacion:") #Inicio ocupacion
        self.label10.grid(column=0, row=9, padx=4, pady=4)
        self.ocupacion1=tk.StringVar()
        self.entryocupacion1=ttk.Entry(self.labelframe1, textvariable=self.ocupacion1, state="readonly")
        self.entryocupacion1.grid(column=1, row=9, padx=4, pady=4) #Default 4x, 4y -Fin ocupacion
        self.label11=ttk.Label(self.labelframe1, text="Residencia:") #Inicio residencia
        self.label11.grid(column=0, row=10, padx=4, pady=4)
        self.residencia1=tk.StringVar()
        self.entryresidencia1=ttk.Entry(self.labelframe1, textvariable=self.residencia1, state="readonly")
        self.entryresidencia1.grid(column=1, row=10, padx=4, pady=4) #Default 4x, 4y -Fin residencia
        self.label12=ttk.Label(self.labelframe1, text="Origen:") #Inicio origen
        self.label12.grid(column=0, row=11, padx=4, pady=4)
        self.origen1=tk.StringVar()
        self.entryorigen1=ttk.Entry(self.labelframe1, textvariable=self.origen1, state="readonly")
        self.entryorigen1.grid(column=1, row=11, padx=4, pady=4) #Default 4x, 4y -Fin origen
        self.label13=ttk.Label(self.labelframe1, text="Estado civil:") #Inicio estadocivil
        self.label13.grid(column=0, row=12, padx=4, pady=4)
        self.estadocivil1=tk.StringVar()
        self.entryestadocivil1=ttk.Entry(self.labelframe1, textvariable=self.estadocivil1, state="readonly")
        self.entryestadocivil1.grid(column=1, row=12, padx=4, pady=4) #Default 4x, 4y -Fin estadocivil
        self.label14=ttk.Label(self.labelframe1, text="-Nombre segundo contacto:") #Inicio nombreSC
        self.label14.grid(column=0, row=13, padx=4, pady=4)
        self.nombreSC1=tk.StringVar()
        self.entrynombreSC1=ttk.Entry(self.labelframe1, textvariable=self.nombreSC1, state="readonly")
        self.entrynombreSC1.grid(column=1, row=13, padx=4, pady=4) #Default 4x, 4y -Fin nombreSC
        self.label15=ttk.Label(self.labelframe1, text="Parentesco:") #Inicio parentesco
        self.label15.grid(column=0, row=14, padx=4, pady=4)
        self.parentesco1=tk.StringVar()
        self.entryparentesco1=ttk.Entry(self.labelframe1, textvariable=self.parentesco1, state="readonly")
        self.entryparentesco1.grid(column=1, row=14, padx=4, pady=4) #Default 4x, 4y -Fin parentesco
        self.label16=ttk.Label(self.labelframe1, text="Domicilio segundo contacto:") #Inicio domicilioSC
        self.label16.grid(column=0, row=15, padx=4, pady=4)
        self.domicilioSC1=tk.StringVar()
        self.entrydomicilioSC1=ttk.Entry(self.labelframe1, textvariable=self.domicilioSC1, state="readonly")
        self.entrydomicilioSC1.grid(column=1, row=15, padx=4, pady=4) #Default 4x, 4y -Fin domicilioSC
        self.label17=ttk.Label(self.labelframe1, text="Telefono segundo contacto:") #Inicio telefonoSC
        self.label17.grid(column=0, row=16, padx=4, pady=4)
        self.telefonoSC1=tk.StringVar()
        self.entrytelefonoSC1=ttk.Entry(self.labelframe1, textvariable=self.telefonoSC1, state="readonly")
        self.entrytelefonoSC1.grid(column=1, row=16, padx=4, pady=4) #Default 4x, 4y -Fin telefonoSC
        self.label18=ttk.Label(self.labelframe1, text="-Cedula Dr:") #Inicio cedula
        self.label18.grid(column=0, row=17, padx=4, pady=4)
        self.cedula1=tk.StringVar()
        self.entrycedula1=ttk.Entry(self.labelframe1, textvariable=self.cedula1, state="readonly")
        self.entrycedula1.grid(column=1, row=17, padx=4, pady=4) #Default 4x, 4y -Fin cedula
        self.label19=ttk.Label(self.labelframe1, text="Tipo/sangre del paciente:") #Inicio tipoSangre
        self.label19.grid(column=0, row=18, padx=4, pady=4)
        self.tiposangre1=tk.StringVar()
        self.entrytiposangre1=ttk.Entry(self.labelframe1, textvariable=self.tiposangre1, state="readonly")
        self.entrytiposangre1.grid(column=1, row=18, padx=4, pady=4) #Default 4x, 4y -Fin tipoSangre
        self.boton1=Button(self.labelframe1, text="Consultar", bg="deep sky blue",command=self.consultar) #Inicio boton consultar
        self.boton1.grid(column=1, row=19, padx=4, pady=4) #Fin boton consultar

    def consultar(self):
        datos=(self.codigo.get(), )
        respuesta=self.paciente1.consulta(datos)
        if len(respuesta)>0:
            self.nombrepaciente1.set(respuesta[0][0])
            self.apellidopaterno1.set(respuesta[0][1])
            self.apellidomaterno1.set(respuesta[0][2])
            self.sexo1.set(respuesta[0][3])
            self.edad1.set(respuesta[0][4])
            self.domicilio1.set(respuesta[0][5])
            self.telefono1.set(respuesta[0][6])
            self.correo1.set(respuesta[0][7])
            self.ocupacion1.set(respuesta[0][8])
            self.residencia1.set(respuesta[0][9])
            self.origen1.set(respuesta[0][10])
            self.estadocivil1.set(respuesta[0][11])
            self.nombreSC1.set(respuesta[0][12])
            self.parentesco1.set(respuesta[0][13])
            self.domicilioSC1.set(respuesta[0][14])
            self.telefonoSC1.set(respuesta[0][15])
            self.cedula1.set(respuesta[0][16])
            self.tiposangre1.set(respuesta[0][17])
        else:
            self.nombrepaciente.set('')
            self.apellidopaterno.set('')
            self.apellidomaterno.set('')
            self.sexo.set('')
            self.edad.set('')
            self.domicilio.set('')
            self.telefono.set('')
            self.correo.set('')
            self.ocupacion.set('')
            self.residencia.set('')
            self.origen.set('')
            self.estadocivil.set('')
            self.nombreSC.set('')
            self.parentesco.set('')
            self.domicilioSC.set('')
            self.telefonoSC.set('')
            self.cedula.set('')
            self.tiposangre.set('')
            mb.showinfo("Información", "No existe algun paciente con dicho código o ID")

    def listado_completo(self):
        self.pagina3 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina3, text="Listado de pacientes")
        self.labelframe1=ttk.LabelFrame(self.pagina3, text="Paciente")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.boton1=Button(self.labelframe1, text="Listado completo",bg="spring green", command=self.listar) #Inicio boton listar
       
        self.boton1.grid(column=0, row=0, padx=4, pady=4) #Fin boton listar
        self.scrolledtext1=st.ScrolledText(self.labelframe1, width=70, height=30) #Default width=30, height=10
        self.scrolledtext1.grid(column=0,row=1, padx=10, pady=10) #Default 10x, 10y

    def listar(self):
        respuesta=self.paciente1.recuperar_todos()
        self.scrolledtext1.delete("1.0", tk.END)        
        for fila in respuesta:
            self.scrolledtext1.insert(tk.END, ">Código o ID: "+str(fila[0])+
                                              "\n-Nombre: "+fila[1]+
                                              "\nApellido Paterno: "+fila[2]+
                                              "\nApellido Materno: "+fila[3]+
                                              "\nSexo: "+fila[4]+
                                              "\nEdad: "+fila[5]+
                                              "\nDomicilio: "+fila[6]+
                                              "\nTelefono: "+fila[7]+
                                              "\nCorreo: "+fila[8]+
                                              "\nOcupacion: "+fila[9]+
                                              "\nResidencia: "+fila[10]+
                                              "\nOrigen: "+fila[11]+
                                              "\nEstado civil: "+fila[12]+
                                              "\n-Nombre segundo contacto: "+fila[13]+
                                              "\nParentesco: "+fila[14]+
                                              "\nDomicilio segundo contacto: "+fila[15]+
                                              "\nTelefono segundo contacto: "+fila[16]+
                                              "\n-Cedula Dr: "+fila[17]+
                                              "\nTipo/sangre del paciente: "+fila[18]+"\n\n")
                                              

    def borrado(self):
        self.pagina4 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina4, text="Eliminar paciente")
        self.labelframe1=ttk.LabelFrame(self.pagina4, text="Paciente")    
        self.labelframe1.grid(column=0, row=0, padx=20, pady=20) #Default: 5x,10y
        self.label1=ttk.Label(self.labelframe1, text="Código o ID:\nNota: No es posible\neliminar a los pacientes\nque tengan una cita o\nun tratamiento activo.") #Inicio de IDpaciente
        self.label1.grid(column=0, row=0, padx=50, pady=100) #Default: 4x,4y
        self.codigoborra=tk.StringVar()
        self.entryborra=ttk.Entry(self.labelframe1, textvariable=self.codigoborra)
        self.entryborra.grid(column=1, row=0, padx=50, pady=107) #Default: 4x,4y -Fin IDpaciente
        self.boton1=Button(self.labelframe1, text="Borrar", bg="red",command=self.borrar) #Inicio boton borrar
        self.boton1.grid(column=1, row=1, padx=4, pady=4) #Fin boton borrar

    def borrar(self):    
        datos=(self.codigoborra.get(), )
        cantidad=self.paciente1.baja(datos)
        if cantidad==1:
            mb.showinfo("Información", "Se borró al paciente con dicho código o ID")
        else:
            mb.showinfo("Información", "No existe algun paciente con dicho código o ID")

    def modificar(self):
        self.pagina5 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina5, text="Modificar paciente")
        self.labelframe1=ttk.LabelFrame(self.pagina5, text="Paciente")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe1, text="Código:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.codigomod=tk.StringVar()
        self.entrycodigo=ttk.Entry(self.labelframe1, textvariable=self.codigomod)
        self.entrycodigo.grid(column=1, row=0, padx=4, pady=4) #Fin IDpaciente
        self.label2=ttk.Label(self.labelframe1, text="Nombre:") #Inicio nombre   
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.nombrepaciente2=tk.StringVar()
        self.entrynombrepaciente2=ttk.Entry(self.labelframe1, textvariable=self.nombrepaciente2)
        self.entrynombrepaciente2.grid(column=1, row=1, padx=4, pady=4) #Default: 4x,4y -Fin nombre
        self.label3=ttk.Label(self.labelframe1, text="Apellido Paterno:") #Inicio apellidoP  
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.apellidopaterno2=tk.StringVar()
        self.entryapellidopaterno2=ttk.Entry(self.labelframe1, textvariable=self.apellidopaterno2)
        self.entryapellidopaterno2.grid(column=1, row=2, padx=4, pady=4) #Default: 4x,4y -Fin apellidoP
        self.label4=ttk.Label(self.labelframe1, text="Apellido materno:") #Inicio apellido materno
        self.label4.grid(column=0, row=3, padx=4, pady=4)
        self.apellidomaterno2=tk.StringVar()
        self.entryapellidomaterno2=ttk.Entry(self.labelframe1, textvariable=self.apellidomaterno2)
        self.entryapellidomaterno2.grid(column=1, row=3, padx=4, pady=4) #Default 4x, 4y -Fin apellidoM
        self.label5=ttk.Label(self.labelframe1, text="Sexo (H/M):") #Inicio sexo
        self.label5.grid(column=0, row=4, padx=4, pady=4)
        self.sexo2=tk.StringVar()
        self.entrysexo2=ttk.Entry(self.labelframe1, textvariable=self.sexo2)
        self.entrysexo2.grid(column=1, row=4, padx=4, pady=4) #Default 4x, 4y -Fin sexo
        self.label6=ttk.Label(self.labelframe1, text="Edad:") #Inicio edad
        self.label6.grid(column=0, row=5, padx=4, pady=4)
        self.edad2=tk.StringVar()
        self.entryedad2=ttk.Entry(self.labelframe1, textvariable=self.edad2)
        self.entryedad2.grid(column=1, row=5, padx=4, pady=4) #Default 4x, 4y -Fin edad
        self.label7=ttk.Label(self.labelframe1, text="Domicilio:") #Inicio domicilio
        self.label7.grid(column=0, row=6, padx=4, pady=4)
        self.domicilio2=tk.StringVar()
        self.entrydomicilio2=ttk.Entry(self.labelframe1, textvariable=self.domicilio2)
        self.entrydomicilio2.grid(column=1, row=6, padx=4, pady=4) #Default 4x, 4y -Fin domicilio
        self.label8=ttk.Label(self.labelframe1, text="Telefono:") #Inicio telefono
        self.label8.grid(column=0, row=7, padx=4, pady=4)
        self.telefono2=tk.StringVar()
        self.entrytelefono2=ttk.Entry(self.labelframe1, textvariable=self.telefono2)
        self.entrytelefono2.grid(column=1, row=7, padx=4, pady=4) #Default 4x, 4y -Fin telefono
        self.label9=ttk.Label(self.labelframe1, text="Correo:") #Inicio correo
        self.label9.grid(column=0, row=8, padx=4, pady=4)
        self.correo2=tk.StringVar()
        self.entrycorreo2=ttk.Entry(self.labelframe1, textvariable=self.correo2)
        self.entrycorreo2.grid(column=1, row=8, padx=4, pady=4) #Default 4x, 4y -Fin correo
        self.label10=ttk.Label(self.labelframe1, text="Ocupacion:") #Inicio ocupacion
        self.label10.grid(column=0, row=9, padx=4, pady=4)
        self.ocupacion2=tk.StringVar()
        self.entryocupacion2=ttk.Entry(self.labelframe1, textvariable=self.ocupacion2)
        self.entryocupacion2.grid(column=1, row=9, padx=4, pady=4) #Default 4x, 4y -Fin ocupacion
        self.label11=ttk.Label(self.labelframe1, text="Residencia:") #Inicio residencia
        self.label11.grid(column=0, row=10, padx=4, pady=4)
        self.residencia2=tk.StringVar()
        self.entryresidencia2=ttk.Entry(self.labelframe1, textvariable=self.residencia2)
        self.entryresidencia2.grid(column=1, row=10, padx=4, pady=4) #Default 4x, 4y -Fin residencia
        self.label12=ttk.Label(self.labelframe1, text="Origen:") #Inicio origen
        self.label12.grid(column=0, row=11, padx=4, pady=4)
        self.origen2=tk.StringVar()
        self.entryorigen2=ttk.Entry(self.labelframe1, textvariable=self.origen2)
        self.entryorigen2.grid(column=1, row=11, padx=4, pady=4) #Default 4x, 4y -Fin origen
        self.label13=ttk.Label(self.labelframe1, text="Estado civil:") #Inicio estadocivil
        self.label13.grid(column=0, row=12, padx=4, pady=4)
        self.estadocivil2=tk.StringVar()
        self.entryestadocivil2=ttk.Entry(self.labelframe1, textvariable=self.estadocivil2)
        self.entryestadocivil2.grid(column=1, row=12, padx=4, pady=4) #Default 4x, 4y -Fin estadocivil
        self.label14=ttk.Label(self.labelframe1, text="-Nombre segundo contacto:") #Inicio nombreSC
        self.label14.grid(column=0, row=13, padx=4, pady=4)
        self.nombreSC2=tk.StringVar()
        self.entrynombreSC2=ttk.Entry(self.labelframe1, textvariable=self.nombreSC2)
        self.entrynombreSC2.grid(column=1, row=13, padx=4, pady=4) #Default 4x, 4y -Fin nombreSC
        self.label15=ttk.Label(self.labelframe1, text="Parentesco:") #Inicio parentesco
        self.label15.grid(column=0, row=14, padx=4, pady=4)
        self.parentesco2=tk.StringVar()
        self.entryparentesco2=ttk.Entry(self.labelframe1, textvariable=self.parentesco2)
        self.entryparentesco2.grid(column=1, row=14, padx=4, pady=4) #Default 4x, 4y -Fin parentesco
        self.label16=ttk.Label(self.labelframe1, text="Domicilio segundo contacto:") #Inicio domicilioSC
        self.label16.grid(column=0, row=15, padx=4, pady=4)
        self.domicilioSC2=tk.StringVar()
        self.entrydomicilioSC2=ttk.Entry(self.labelframe1, textvariable=self.domicilioSC2)
        self.entrydomicilioSC2.grid(column=1, row=15, padx=4, pady=4) #Default 4x, 4y -Fin domicilioSC
        self.label17=ttk.Label(self.labelframe1, text="Telefono segundo contacto:") #Inicio telefonoSC
        self.label17.grid(column=0, row=16, padx=4, pady=4)
        self.telefonoSC2=tk.StringVar()
        self.entrytelefonoSC2=ttk.Entry(self.labelframe1, textvariable=self.telefonoSC2)
        self.entrytelefonoSC2.grid(column=1, row=16, padx=4, pady=4) #Default 4x, 4y -Fin telefonoSC
        self.label18=ttk.Label(self.labelframe1, text="-Cedula Dr:") #Inicio cedula
        self.label18.grid(column=0, row=17, padx=4, pady=4)
        self.cedula2=tk.StringVar()
        self.entrycedula2=ttk.Entry(self.labelframe1, textvariable=self.cedula2)
        self.entrycedula2.grid(column=1, row=17, padx=4, pady=4) #Default 4x, 4y -Fin cedula
        self.label19=ttk.Label(self.labelframe1, text="Tipo/sangre del paciente:") #Inicio tipoSangre
        self.label19.grid(column=0, row=18, padx=4, pady=4)
        self.tiposangre2=tk.StringVar()
        self.entrytiposangre2=ttk.Entry(self.labelframe1, textvariable=self.tiposangre2)
        self.entrytiposangre2.grid(column=1, row=18, padx=4, pady=4) #Default 4x, 4y -Fin tipoSangre
        self.boton1=Button(self.labelframe1, text="Consultar",bg="deep sky blue", command=self.consultar_mod) #Inicio boton consultar
        self.boton1.grid(column=1, row=19, padx=4, pady=4) #Fin boton consultar
        self.boton1=Button(self.labelframe1, text="Modificar", bg="orange",command=self.modifica) #Inicio boton modificar
        self.boton1.grid(column=1, row=20, padx=4, pady=4) #Fin boton modificar

    def modifica(self):
        if self.nombrepaciente2.get() == '':
            mb.showinfo("Información", "Falta añadir el nombre del paciente.")
        elif self.apellidopaterno2.get() == '' and self.apellidomaterno2.get() == '':
            mb.showinfo("Información", "Debe añadir por lo menos un apellido.")
        elif len(self.sexo2.get()) > 1 or self.sexo2.get() == '':
            mb.showinfo("Información", "Sexo invalido.")
        elif self.edad2.get() == '':
            mb.showinfo("Información", "Falta añadir la edad del paciente.")
        elif self.domicilio2.get() == '':
            mb.showinfo("Información", "Falta añadir el domicilio del paciente.")
        elif self.telefono2.get() == '':
            mb.showinfo("Información", "Debe añadir algun telefono del paciente.")
        elif self.nombreSC2.get() == '':
            mb.showinfo("Información", "Debe añadir algun nombre de segundo contacto, o en su defecto poner ninguno.")
        elif self.parentesco2.get() == '':
            mb.showinfo("Información", "Debe añadir algun parentesco, o en su defecto poner ninguno.")
        elif self.telefonoSC2.get() == '':
            mb.showinfo("Información", "Debe añadir algun telefono del segundo contacto, o en su defecto poner ninguno.")
        elif self.tiposangre2.get() == '' or (self.tiposangre2.get() != 'O' and self.tiposangre2.get() != 'o' and self.tiposangre2.get() != 'A' and self.tiposangre2.get() != 'a' and self.tiposangre2.get() != 'AB'and self.tiposangre2.get() != 'ab'and self.tiposangre2.get() != 'b'and self.tiposangre2.get() != 'B'):
            mb.showinfo("Información", "Sangre NO aceptada.")
        elif len(self.cedula2.get()) > 0 or self.cedula2.get() == '':
            datos=(self.cedula2.get(), )
            respuesta=self.paciente1.consultaDoc(datos)
            if len(respuesta)>0:
                datos=(self.nombrepaciente2.get(), self.apellidopaterno2.get(),self.apellidomaterno2.get(),self.sexo2.get(),self.edad2.get(),self.domicilio2.get(),self.telefono2.get(),self.correo2.get(),self.ocupacion2.get(),self.residencia2.get(),self.origen2.get(),self.estadocivil2.get(),self.nombreSC2.get(),self.parentesco2.get(),self.domicilioSC2.get(),self.telefonoSC2.get(),self.cedula2.get(),self.tiposangre2.get(),self.codigomod.get())
                cantidad=self.paciente1.modificacion(datos)
                if cantidad==1:
                    mb.showinfo("Información", "Se modificó al paciente")
                else:
                    mb.showinfo("Información", "No existe algun paciente con dicho código o ID")
            else:
                mb.showinfo("Información", "Cedula invalida.")

    def consultar_mod(self):
        datos=(self.codigomod.get(), )
        respuesta=self.paciente1.consulta(datos)
        if len(respuesta)>0:
            self.nombrepaciente2.set(respuesta[0][0])
            self.apellidopaterno2.set(respuesta[0][1])
            self.apellidomaterno2.set(respuesta[0][2])
            self.sexo2.set(respuesta[0][3])
            self.edad2.set(respuesta[0][4])
            self.domicilio2.set(respuesta[0][5])
            self.telefono2.set(respuesta[0][6])
            self.correo2.set(respuesta[0][7])
            self.ocupacion2.set(respuesta[0][8])
            self.residencia2.set(respuesta[0][9])
            self.origen2.set(respuesta[0][10])
            self.estadocivil2.set(respuesta[0][11])
            self.nombreSC2.set(respuesta[0][12])
            self.parentesco2.set(respuesta[0][13])
            self.domicilioSC2.set(respuesta[0][14])
            self.telefonoSC2.set(respuesta[0][15])
            self.cedula2.set(respuesta[0][16])
            self.tiposangre2.set(respuesta[0][17])
        else:
            self.nombrepaciente2.set('')
            self.apellidopaterno2.set('')
            self.apellidomaterno2.set('')
            self.sexo2.set('')
            self.edad2.set('')
            self.domicilio2.set('')
            self.telefono2.set('')
            self.correo2.set('')
            self.ocupacion2.set('')
            self.residencia2.set('')
            self.origen2.set('')
            self.estadocivil2.set('')
            self.nombreSC2.set('')
            self.parentesco2.set('')
            self.domicilioSC2.set('')
            self.telefonoSC2.set('')
            self.cedula2.set('')
            self.tiposangre2.set('')
            mb.showinfo("Información", "No existe algun paciente con dicho código o ID")

#----------------------------------------------------------------------------------------------
class Doctor:
    def abrir(self):
        conexion1 = psycopg2.connect(database="proyecto", user="postgres", password='yourpassw')
        return conexion1

    def alta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="insert into doctor(cedula, nombre, apellidoP, apellidoM, sexo, telefono) values (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, datos)
        cone.commit()

    def consulta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select nombre, apellidoP, apellidoM, sexo, telefono from doctor where cedula=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()
    
    def consultaDoc(self,datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select nombre from doctor where cedula=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()
            
    def recuperar_todos(self):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select cedula, nombre, apellidoP, apellidoM, sexo, telefono from doctor"
        cursor.execute(sql)
        sql2 = "select * from doctor order by cedula"
        cursor.execute(sql2)
        return cursor.fetchall()
    
    def baja(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="delete from doctor where cedula=%s"
        cursor.execute(sql, datos)
        cone.commit()
        return cursor.rowcount # retornamos la cantidad de filas borradas
            
    def modificacion(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="update doctor set nombre=%s, apellidoP=%s, apellidoM=%s, sexo=%s, telefono=%s where cedula=%s"
        cursor.execute(sql, datos)
        cone.commit()
        return cursor.rowcount # retornamos la cantidad de filas modificadas

class FormularioDoc:
    def __init__(self):
        mb.showinfo("Información general", "-La cedula del paciente debe coincidir con la de algun doctor al agregarse.")
        self.doctor1=Doctor() #Se llama a la clase declarada
        self.ventanadoc=tk.Tk()  #Se crea una ventana 
        self.ventanadoc.config(bg="dodger blue")
        self.ventanadoc.title("Clinica Odontologica")  #Titulo de la ventana
        self.cuadernodoc1 = ttk.Notebook(self.ventanadoc)   #Se crea un cuaderno en la ventana 
        self.carga_Doctor()  #Metodos base
        self.consulta_por_cedula()
        self.listado_completo()
        self.borrado()
        self.modificar()
        style = ttk.Style()
        style.theme_use("classic")
        style.configure("TNotebook.Tab", background="green", font="helvetica 10")
        self.cuadernodoc1.grid(column=0, row=0, padx=60, pady=10) #Default 10x, 10y dimension del cuaderno
        self.ventanadoc.mainloop() #Ejecuta la ventana principal 
                
            
    def carga_Doctor(self):
        self.paginadoc1 = ttk.Frame(self.cuadernodoc1)
        self.cuadernodoc1.add(self.paginadoc1, text="Agregar doctor")
        self.labelframe1=ttk.LabelFrame(self.paginadoc1, text="Doctor")        
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10) #Default 5x, 10y
        self.label1=ttk.Label(self.labelframe1, text="-Cedula:") #Inicio cedula
        self.label1.grid(column=0, row=0, padx=4, pady=4) #Default 4x, 4y
        self.ceduladoc=tk.StringVar()
        self.entryceduladoc=ttk.Entry(self.labelframe1, textvariable=self.ceduladoc) 
        self.entryceduladoc.grid(column=1, row=0, padx=4, pady=4) #Default 4x, 4y -Fin cedula
        self.label2=ttk.Label(self.labelframe1, text="Nombre:") #Inicio nombre
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.nombredoc=tk.StringVar()
        self.entrynombredoc=ttk.Entry(self.labelframe1, textvariable=self.nombredoc)
        self.entrynombredoc.grid(column=1, row=1, padx=4, pady=4) #Default 4x, 4y -Fin nombre
        self.label3=ttk.Label(self.labelframe1, text="Apellido paterno:") #Inicio apellido paterno
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.apellidopaternodoc=tk.StringVar()
        self.entryapellidopaternodoc=ttk.Entry(self.labelframe1, textvariable=self.apellidopaternodoc)
        self.entryapellidopaternodoc.grid(column=1, row=2, padx=4, pady=4) #Default 4x, 4y -Fin apellidoP
        self.label4=ttk.Label(self.labelframe1, text="Apellido materno:") #Inicio apellidoM
        self.label4.grid(column=0, row=3, padx=4, pady=4)
        self.apellidomaternodoc=tk.StringVar()
        self.entryapellidomaternodoc=ttk.Entry(self.labelframe1, textvariable=self.apellidomaternodoc)
        self.entryapellidomaternodoc.grid(column=1, row=3, padx=4, pady=4) #Default 4x, 4y -Fin apellidoM
        self.label5=ttk.Label(self.labelframe1, text="Sexo (H/M):") #Inicio sexo
        self.label5.grid(column=0, row=4, padx=4, pady=4)
        self.sexodoc=tk.StringVar()
        self.entrysexodoc=ttk.Entry(self.labelframe1, textvariable=self.sexodoc)
        self.entrysexodoc.grid(column=1, row=4, padx=4, pady=4) #Default 4x, 4y -Fin sexo
        self.label6=ttk.Label(self.labelframe1, text="Telefono:") #Inicio telefono
        self.label6.grid(column=0, row=5, padx=4, pady=4)
        self.telefonodoc=tk.StringVar()
        self.entrytelefonodoc=ttk.Entry(self.labelframe1, textvariable=self.telefonodoc)
        self.entrytelefonodoc.grid(column=1, row=5, padx=4, pady=4) #Default 4x, 4y -Fin telefono

        self.botondoc1=Button(self.labelframe1, text="Confirmar", bg="red",command=self.agregarDoc) #Inicio boton agregarDoc
        self.botondoc1.grid(column=1, row=6, padx=4, pady=4) #Default 4x, 4y -Fin boton
        self.botondoc2=Button(self.labelframe1, text="----> Regresar ", bg="deep sky blue", command=self.regresar) #Inicio boton agregarDoc
        self.botondoc2.grid(column=4, row=7, padx=4, pady=4) #Default 4x, 4y -Fin boton
            
    def agregarDoc(self):
        if self.nombredoc.get() == '':
            mb.showinfo("Información", "Falta añadir el nombre del doctor.")
        elif self.apellidopaternodoc.get() == '' and self.apellidomaternodoc.get() == '':
            mb.showinfo("Información", "Debe añadir por lo menos un apellido.")
        elif len(self.sexodoc.get()) > 1 or self.sexodoc.get() == '':
            mb.showinfo("Información", "Sexo invalido.")
        elif self.telefonodoc.get() == '':
            mb.showinfo("Información", "Debe añadir algun telefono del doctor.")
        elif len(self.ceduladoc.get()) > 0 or self.ceduladoc.get() == '':
            datos=(self.ceduladoc.get(), )
            respuesta=self.doctor1.consultaDoc(datos)
            if len(respuesta)>0 or self.ceduladoc.get() == '':
                mb.showinfo("Información", "Cedula invalida.")
            else:
                datos=(self.ceduladoc.get(), self.nombredoc.get(),self.apellidopaternodoc.get(),self.apellidomaternodoc.get(),self.sexodoc.get(),self.telefonodoc.get())                 
                self.doctor1.alta(datos)
                mb.showinfo("Información", "Los datos fueron cargados con exito.")
                self.ceduladoc.set("")
                self.nombredoc.set("")
                self.apellidopaternodoc.set("")
                self.apellidomaternodoc.set("")
                self.sexodoc.set("")
                self.telefonodoc.set("")
                
    
    def consulta_por_cedula(self):
        self.pagina2 = ttk.Frame(self.cuadernodoc1)
        self.cuadernodoc1.add(self.pagina2, text="Consulta por cedula")
        self.labelframe1=ttk.LabelFrame(self.pagina2, text="Doctor")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe1, text="-Cedula:") #Inicio cedula
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.ceduladoc1=tk.StringVar()
        self.entryceduladoc1=ttk.Entry(self.labelframe1, textvariable=self.ceduladoc1) 
        self.entryceduladoc1.grid(column=1, row=0, padx=4, pady=4)  #Fin cedula
        self.label2=ttk.Label(self.labelframe1, text="Nombre:") #Inicio nombre   
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.nombredoc1=tk.StringVar()
        self.entrynombredoc1=ttk.Entry(self.labelframe1, textvariable=self.nombredoc1, state="readonly")
        self.entrynombredoc1.grid(column=1, row=1, padx=4, pady=4) #Default: 4x,4y -Fin nombre
        self.label3=ttk.Label(self.labelframe1, text="Apellido paterno:") #Inicio apellidoP  
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.apellidopaternodoc1=tk.StringVar()
        self.entryapellidopaternodoc1=ttk.Entry(self.labelframe1, textvariable=self.apellidopaternodoc1, state="readonly")
        self.entryapellidopaternodoc1.grid(column=1, row=2, padx=4, pady=4) #Default: 4x,4y -Fin apellidoP
        self.label4=ttk.Label(self.labelframe1, text="Apellido materno:") #Inicio apellido materno
        self.label4.grid(column=0, row=3, padx=4, pady=4)
        self.apellidomaternodoc1=tk.StringVar()
        self.entryapellidomaternodoc1=ttk.Entry(self.labelframe1, textvariable=self.apellidomaternodoc1, state="readonly")
        self.entryapellidomaternodoc1.grid(column=1, row=3, padx=4, pady=4) #Default 4x, 4y -Fin apellidoM
        self.label5=ttk.Label(self.labelframe1, text="Sexo (H/M):") #Inicio sexo
        self.label5.grid(column=0, row=4, padx=4, pady=4)
        self.sexodoc1=tk.StringVar()
        self.entrysexodoc1=ttk.Entry(self.labelframe1, textvariable=self.sexodoc1, state="readonly")
        self.entrysexodoc1.grid(column=1, row=4, padx=4, pady=4) #Default 4x, 4y -Fin sexo
        self.label6=ttk.Label(self.labelframe1, text="Telefono:") #Inicio edad
        self.label6.grid(column=0, row=5, padx=4, pady=4)
        self.telefonodoc1=tk.StringVar()
        self.entrytelefonodoc1=ttk.Entry(self.labelframe1, textvariable=self.telefonodoc1, state="readonly")
        self.entrytelefonodoc1.grid(column=1, row=5, padx=4, pady=4) #Default 4x, 4y -Fin edad

        self.boton1=Button(self.labelframe1, text="Consultar",bg="deep sky blue", command=self.consultar) #Inicio boton consultar
        self.boton1.grid(column=1, row=18, padx=4, pady=4) #Fin boton consultar

    def consultar(self):
        datos=(self.ceduladoc1.get(), )
        respuesta=self.doctor1.consulta(datos)
        if len(respuesta)>0:
            self.nombredoc1.set(respuesta[0][0])
            self.apellidopaternodoc1.set(respuesta[0][1])
            self.apellidomaternodoc1.set(respuesta[0][2])
            self.sexodoc1.set(respuesta[0][3])
            self.telefonodoc1.set(respuesta[0][4])
        else:
            self.nombredoc.set('')
            self.apellidopaternodoc.set('')
            self.apellidomaternodoc.set('')
            self.sexodoc.set('')
            self.telefonodoc.set('')
            mb.showinfo("Información", "No existe algun doctor con dicha cedula.")

    def listado_completo(self):
        self.pagina3 = ttk.Frame(self.cuadernodoc1)
        self.cuadernodoc1.add(self.pagina3, text="Listado de doctores")
        self.labelframe1=ttk.LabelFrame(self.pagina3, text="Doctor")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.boton1=Button(self.labelframe1, text="Listado completo", bg="spring green", command=self.listar) #Inicio boton listar
        self.boton1.grid(column=0, row=0, padx=4, pady=4) #Fin boton listar
        self.scrolledtext1=st.ScrolledText(self.labelframe1, width=70, height=30) #Default width=30, height=10
        self.scrolledtext1.grid(column=0,row=1, padx=10, pady=10) #Default 10x, 10y
    
    def listar(self):
        respuesta=self.doctor1.recuperar_todos()
        self.scrolledtext1.delete("1.0", tk.END)        
        for fila in respuesta:
            self.scrolledtext1.insert(tk.END, ">Cedula: "+fila[0]+
                                              "\nNombre: "+fila[1]+
                                              "\nApellido Paterno: "+fila[2]+
                                              "\nApellido Materno: "+fila[3]+
                                              "\nSexo: "+fila[4]+
                                              "\nTelefono: "+fila[5]+"\n\n")
    
    def borrado(self):
        self.pagina4 = ttk.Frame(self.cuadernodoc1)
        self.cuadernodoc1.add(self.pagina4, text="Eliminar doctor")
        self.labelframe1=ttk.LabelFrame(self.pagina4, text="Doctor")        
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10) #Default: 5x,10y
        self.label1=ttk.Label(self.labelframe1, text="-Cedula:\nNota: No es posible eliminar\na un doctor que\ntenga a un\npaciente activo.") #Inicio de cedula
        self.label1.grid(column=0, row=0, padx=50, pady=100) #Default: 4x,4y
        self.cedulaborra=tk.StringVar()
        self.entryborra=ttk.Entry(self.labelframe1, textvariable=self.cedulaborra)
        self.entryborra.grid(column=1, row=0, padx=50, pady=107) #Default: 4x,4y -Fin cedula
        self.boton1=Button(self.labelframe1, text="Borrar", bg="red",command=self.borrar) #Inicio boton borrar
        self.boton1.grid(column=1, row=1, padx=4, pady=4) #Fin boton borrar
    
    def borrar(self):
        datos=(self.cedulaborra.get(), )
        cantidad=self.doctor1.baja(datos)
        if cantidad==1:
            mb.showinfo("Información", "Se borró al doctor con dicha cedula.")
        else:
            mb.showinfo("Información", "No existe algun doctor con dicha cedula.")
    
    def modificar(self):
        self.pagina5 = ttk.Frame(self.cuadernodoc1)
        self.cuadernodoc1.add(self.pagina5, text="Modificar doctor")
        self.labelframe1=ttk.LabelFrame(self.pagina5, text="Doctor")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe1, text="Cedula:") #Inicio cedula
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.cedulamod=tk.StringVar()
        self.entrycedulamod=ttk.Entry(self.labelframe1, textvariable=self.cedulamod)
        self.entrycedulamod.grid(column=1, row=0, padx=4, pady=4) #Fin cedula
        self.label2=ttk.Label(self.labelframe1, text="Nombre:") #Inicio nombre   
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.nombredoc2=tk.StringVar()
        self.entrynombredoc2=ttk.Entry(self.labelframe1, textvariable=self.nombredoc2)
        self.entrynombredoc2.grid(column=1, row=1, padx=4, pady=4) #Default: 4x,4y -Fin nombre
        self.label3=ttk.Label(self.labelframe1, text="Apellido paterno:") #Inicio apellidoP  
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.apellidopaternodoc2=tk.StringVar()
        self.entryapellidopaternodoc2=ttk.Entry(self.labelframe1, textvariable=self.apellidopaternodoc2)
        self.entryapellidopaternodoc2.grid(column=1, row=2, padx=4, pady=4) #Default: 4x,4y -Fin apellidoP
        self.label4=ttk.Label(self.labelframe1, text="Apellido materno:") #Inicio apellido materno
        self.label4.grid(column=0, row=3, padx=4, pady=4)
        self.apellidomaternodoc2=tk.StringVar()
        self.entryapellidomaternodoc2=ttk.Entry(self.labelframe1, textvariable=self.apellidomaternodoc2)
        self.entryapellidomaternodoc2.grid(column=1, row=3, padx=4, pady=4) #Default 4x, 4y -Fin apellidoM
        self.label5=ttk.Label(self.labelframe1, text="Sexo (H/M):") #Inicio sexo
        self.label5.grid(column=0, row=4, padx=4, pady=4)
        self.sexodoc2=tk.StringVar()
        self.entrysexodoc2=ttk.Entry(self.labelframe1, textvariable=self.sexodoc2)
        self.entrysexodoc2.grid(column=1, row=4, padx=4, pady=4) #Default 4x, 4y -Fin sexo
        self.label6=ttk.Label(self.labelframe1, text="Telefono:") #Inicio telefono
        self.label6.grid(column=0, row=5, padx=4, pady=4)
        self.telefonodoc2=tk.StringVar()
        self.entrytelefonodoc2=ttk.Entry(self.labelframe1, textvariable=self.telefonodoc2)
        self.entrytelefonodoc2.grid(column=1, row=5, padx=4, pady=4) #Default 4x, 4y -Fin telefono

        self.boton1=Button(self.labelframe1, text="Consultar", bg="deep sky blue",command=self.consultar_mod) #Inicio boton consultar
        self.boton1.grid(column=1, row=6, padx=4, pady=4) #Fin boton consultar
        self.boton1=Button(self.labelframe1, text="Modificar", bg="orange",command=self.modifica) #Inicio boton modificar
        self.boton1.grid(column=1, row=7, padx=4, pady=4) #Fin boton modificar

    def modifica(self):
        if self.nombredoc2.get() == '':
            mb.showinfo("Información", "Falta añadir el nombre del doctor.")
        elif self.apellidopaternodoc2.get() == '' and self.apellidomaternodoc2.get() == '':
            mb.showinfo("Información", "Debe añadir por lo menos un apellido.")
        elif len(self.sexodoc2.get()) > 1 or self.sexodoc2.get() == '':
            mb.showinfo("Información", "Sexo invalido.")
        elif self.telefonodoc2.get() == '':
            mb.showinfo("Información", "Debe añadir algun telefono del doctor.")
        elif len(self.cedulamod.get()) > 0 or self.cedulamod.get() == '':
            datos=(self.cedulamod.get(), )
            respuesta=self.doctor1.consultaDoc(datos)
            if len(respuesta)>0 or self.cedulamod.get() == '':
                datos=(self.nombredoc2.get(), self.apellidopaternodoc2.get(),self.apellidomaternodoc2.get(),self.sexodoc2.get(),self.telefonodoc2.get(),self.cedulamod.get())
                cantidad=self.doctor1.modificacion(datos)
                if cantidad==1:
                    mb.showinfo("Información", "Se modificó al doctor.")
                else:
                    mb.showinfo("Información", "No existe algun doctor con dicha cedula.")
            else:
                mb.showinfo("Información", "Cedula invalida.")

    def consultar_mod(self):
        datos=(self.cedulamod.get(), )
        respuesta=self.doctor1.consulta(datos)
        if len(respuesta)>0:
            self.nombredoc2.set(respuesta[0][0])
            self.apellidopaternodoc2.set(respuesta[0][1])
            self.apellidomaternodoc2.set(respuesta[0][2])
            self.sexodoc2.set(respuesta[0][3])
            self.telefonodoc2.set(respuesta[0][4])
        else:
            self.nombredoc2.set('')
            self.apellidopaternodoc2.set('')
            self.apellidomaternodoc2.set('')
            self.sexodoc2.set('')
            self.telefonodoc2.set('')
            mb.showinfo("Información", "No existe algun doctor con dicha cedula.")


    def regresar(self):
        self.ventanadoc.destroy()
        aplicacion1=Formulario() #Llama a la clase principal 

#---------------------------------------------------------------------------------------------

class Cita:
    def abrir(self):
        conexion2 = psycopg2.connect(database="proyecto", user="postgres", password='yourpassw')
        return conexion2

    def alta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="insert into cita (IDpaciente, cedula, fechahoracita) values (%s,%s,%s)"
        cursor.execute(sql, datos)
        cone.commit()

    def consulta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select fechahoracita from cita where IDpaciente=%s and cedula =%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()
    
    def consultaPac(self,datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select nombre from paciente where IDpaciente=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()

    def consultaDoc(self,datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select nombre from doctor where cedula=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()
            
    def recuperar_todos(self):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select IDpaciente, cedula, fechahoracita from cita"
        cursor.execute(sql)
        sql2 = "select * from cita order by IDpaciente"
        cursor.execute(sql2)
        return cursor.fetchall()
    
    def baja(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="delete from cita where IDpaciente=%s and cedula=%s"
        cursor.execute(sql, datos)
        cone.commit()
        return cursor.rowcount # retornamos la cantidad de filas borradas
            
    def modificacion(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="update cita set fechahoracita=%s where IDpaciente=%s and cedula=%s"
        cursor.execute(sql, datos)
        cone.commit()
        return cursor.rowcount # retornamos la cantidad de filas modificadas

class FormularioCita:
    def __init__(self):
        mb.showinfo("Información sobre citas", "-Las citas del paciente se agregan mediante su ID.")
        self.cita1=Cita() #Se llama a la clase declarada
        self.ventanacita=tk.Tk()  #Se crea una ventana 
        self.ventanacita.config(bg="dodger blue")
        self.ventanacita.title("Clinica Odontologica")  #Titulo de la ventana
        self.cuadernocita1 = ttk.Notebook(self.ventanacita)   #Se crea un cuaderno en la ventana 
        self.carga_Cita()  #Metodos base
        self.consulta_por_codigo()
        self.listado_completo()
        self.borrado()
        self.modificar()
        style = ttk.Style()
        style.theme_use("classic")
        style.configure("TNotebook.Tab", background="green", font="helvetica 10")
        self.cuadernocita1.grid(column=0, row=0, padx=60, pady=10) #Default 10x, 10y dimension del cuaderno
        self.ventanacita.mainloop() #Ejecuta la ventana principal 
                
            
    def carga_Cita(self):
        self.paginacita1 = ttk.Frame(self.cuadernocita1)
        self.cuadernocita1.add(self.paginacita1, text="Agregar cita")
        self.labelframe1=ttk.LabelFrame(self.paginacita1, text="Cita")        
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10) #Default 5x, 10y
        self.label1=ttk.Label(self.labelframe1, text="-ID de paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=4, pady=4) #Default 4x, 4y
        self.idpacientecita=tk.StringVar()
        self.entryidpacientecita=ttk.Entry(self.labelframe1, textvariable=self.idpacientecita) 
        self.entryidpacientecita.grid(column=1, row=0, padx=4, pady=4) #Default 4x, 4y -Fin IDpaciente
        self.label2=ttk.Label(self.labelframe1, text="-Cedula Dr:") #Inicio cedula
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.cedulacita=tk.StringVar()
        self.entrycedulacita=ttk.Entry(self.labelframe1, textvariable=self.cedulacita)
        self.entrycedulacita.grid(column=1, row=1, padx=4, pady=4) #Default 4x, 4y -Fin cedula
        self.label3=ttk.Label(self.labelframe1, text="Fecha/Hora cita (DD/MM/AA HH:MM:SS):\nNota: La fecha de la cita debe ser mayor a la actual.") #Inicio fecha hora
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.fechacita=tk.StringVar()
        self.entryfechacita=ttk.Entry(self.labelframe1, textvariable=self.fechacita)
        self.entryfechacita.grid(column=1, row=2, padx=4, pady=4) #Default 4x, 4y -Fin fecha/hora

        self.botoncita1=Button(self.labelframe1, text="Confirmar", bg="red", command=self.agregarCita) #Inicio boton agregarCita
        self.botoncita1.grid(column=1, row=6, padx=4, pady=4) #Default 4x, 4y -Fin boton
        self.botoncita2=Button(self.labelframe1, text="----> Regresar ", bg="deep sky blue",command=self.regresar) #Inicio boton agregarCita
        self.botoncita2.grid(column=4, row=7, padx=4, pady=4) #Default 4x, 4y -Fin boton
            
    def agregarCita(self):
        newcita = ''
        for caracter in self.fechacita.get():
            if caracter != ' ':
                newcita = newcita+caracter
            else:
                break
        now = datetime.now()
        newnow = str(now.day)+'-'+str(now.month)+'-'+str(now.year)
        newnow1 = str(now.day)+'/'+str(now.month)+'/'+str(now.year)
        if self.fechacita.get() == '' or (newcita <= newnow and newcita <= newnow1):
            mb.showinfo("Información", "Fecha de cita NO aceptada.")
        elif self.idpacientecita.get() == '':
            mb.showinfo("Información", "ID paciente invalido.")
        elif self.cedulacita.get() == '':
            mb.showinfo("Información", "Cedula invalida.")
        elif len(self.idpacientecita.get()) > 0 or self.idpacientecita.get() == '':
            datos=(self.idpacientecita.get(), )
            respuesta=self.cita1.consultaPac(datos)
            if len(respuesta)>0:
                if len(self.cedulacita.get()) > 0 or self.cedulacita.get() == '':
                    datos=(self.cedulacita.get(), )
                    respuesta=self.cita1.consultaDoc(datos)
                if len(respuesta)>0:
                    datos=(self.idpacientecita.get(), self.cedulacita.get(),self.fechacita.get())              
                    self.cita1.alta(datos)
                    mb.showinfo("Información", "Los datos fueron cargados con exito.")
                    self.idpacientecita.set("")
                    self.cedulacita.set("")
                    self.fechacita.set("")
                else:
                    mb.showinfo("Información", "Cedula invalida.")
            else:
                mb.showinfo("Información", "ID paciente invalido.")
            
    
    def consulta_por_codigo(self):
        self.pagina2 = ttk.Frame(self.cuadernocita1)
        self.cuadernocita1.add(self.pagina2, text="Consultar cita")
        self.labelframe1=ttk.LabelFrame(self.pagina2, text="Cita")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe1, text="-ID paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.idpacientecita1=tk.StringVar()
        self.entryidpacientecita1=ttk.Entry(self.labelframe1, textvariable=self.idpacientecita1) 
        self.entryidpacientecita1.grid(column=1, row=0, padx=4, pady=4)  #Fin IDpaciente
        self.label2=ttk.Label(self.labelframe1, text="-Cedula:") #Inicio cedula
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.cedulacita1=tk.StringVar()
        self.entrycedulacita1=ttk.Entry(self.labelframe1, textvariable=self.cedulacita1)
        self.entrycedulacita1.grid(column=1, row=1, padx=4, pady=4) #Default: 4x,4y -Fin cedula
        self.label3=ttk.Label(self.labelframe1, text="Fecha/hora cita:") #Inicio fecha/h 
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.fechacita1=tk.StringVar()
        self.entryfechacita1=ttk.Entry(self.labelframe1, textvariable=self.fechacita1, state="readonly")
        self.entryfechacita1.grid(column=1, row=2, padx=4, pady=4) #Default: 4x,4y -Fin fecha/h
        
        self.boton1=Button(self.labelframe1, text="Consultar",bg="deep sky blue", command=self.consultar) #Inicio boton consultar
        self.boton1.grid(column=1, row=18, padx=4, pady=4) #Fin boton consultar

    def consultar(self):
        datos=(self.idpacientecita1.get(),self.cedulacita1.get(), )
        respuesta=self.cita1.consulta(datos)
        if len(respuesta)>0:
            self.fechacita1.set(respuesta[0][0])
        else:
            self.fechacita.set('')
            mb.showinfo("Información", "No existe algun cita con dicha cedula o ID.")

    def listado_completo(self):
        self.pagina3 = ttk.Frame(self.cuadernocita1)
        self.cuadernocita1.add(self.pagina3, text="Listado de citas")
        self.labelframe1=ttk.LabelFrame(self.pagina3, text="Cita")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.boton1=Button(self.labelframe1, text="Listado completo",bg="spring green", command=self.listar) #Inicio boton listar
        self.boton1.grid(column=0, row=0, padx=4, pady=4) #Fin boton listar
        self.scrolledtext1=st.ScrolledText(self.labelframe1, width=70, height=30) #Default width=30, height=10
        self.scrolledtext1.grid(column=0,row=1, padx=10, pady=10) #Default 10x, 10y
    
    def listar(self):
        respuesta=self.cita1.recuperar_todos()
        self.scrolledtext1.delete("1.0", tk.END)        
        for fila in respuesta:
            self.scrolledtext1.insert(tk.END, ">ID de paciente: "+str(fila[0])+
                                              "\n-Cedula Dr: "+fila[1]+
                                              "\nFecha/hora cita: "+str(fila[2])+"\n\n")
    
    def borrado(self):
        self.pagina4 = ttk.Frame(self.cuadernocita1)
        self.cuadernocita1.add(self.pagina4, text="Eliminar cita")
        self.labelframe1=ttk.LabelFrame(self.pagina4, text="Cita")        
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10) #Default: 5x,10y
        self.label1=ttk.Label(self.labelframe1, text="-ID paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=50, pady=100) #Default: 4x,4y
        self.idborra=tk.IntVar()
        self.entryborra=ttk.Entry(self.labelframe1, textvariable=self.idborra)
        self.entryborra.grid(column=1, row=0, padx=50, pady=107) #Default: 4x,4y -Fin IDpaciente
        self.label1=ttk.Label(self.labelframe1, text="-Cedula:") #Inicio cedula
        self.label1.grid(column=0, row=1, padx=4, pady=4) #Default: 4x,4y
        self.cedulaborra=tk.StringVar()
        self.entryborra1=ttk.Entry(self.labelframe1, textvariable=self.cedulaborra)
        self.entryborra1.grid(column=1, row=1, padx=4, pady=4) #Default: 4x,4y -Fin cedula
        self.boton1=Button(self.labelframe1, text="Borrar", bg="red",command=self.borrar) #Inicio boton borrar
        self.boton1.grid(column=1, row=2, padx=4, pady=4) #Fin boton borrar
    
    def borrar(self):
        datos=(self.idborra.get(),self.cedulaborra.get(), )
        cantidad=self.cita1.baja(datos)
        if cantidad==1:
            mb.showinfo("Información", "Se borró la cita con dicha cedula e ID.")
        else:
            mb.showinfo("Información", "No existe algun cita con dicha cedula e ID.")
    
    def modificar(self):
        self.pagina5 = ttk.Frame(self.cuadernocita1)
        self.cuadernocita1.add(self.pagina5, text="Modificar cita")
        self.labelframe1=ttk.LabelFrame(self.pagina5, text="Cita")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe1, text="-ID paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.idmod=tk.StringVar()
        self.entryidmod=ttk.Entry(self.labelframe1, textvariable=self.idmod)
        self.entryidmod.grid(column=1, row=0, padx=4, pady=4) #Fin IDpaciente
        self.label2=ttk.Label(self.labelframe1, text="-Cedula:") #Inicio cedula
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.cedulamod=tk.StringVar()
        self.entrycedulamod=ttk.Entry(self.labelframe1, textvariable=self.cedulamod)
        self.entrycedulamod.grid(column=1, row=1, padx=4, pady=4) #Default: 4x,4y -Fin cedula
        self.label3=ttk.Label(self.labelframe1, text="Fecha/hora cita (DD/MM/AA HH:MM:SS):") #Inicio fecha/h 
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.fechacita2=tk.StringVar()
        self.entryfechacita2=ttk.Entry(self.labelframe1, textvariable=self.fechacita2)
        self.entryfechacita2.grid(column=1, row=2, padx=4, pady=4) #Default: 4x,4y -Fin apellidoP
        self.boton1=Button(self.labelframe1, text="Consultar", bg="deep sky blue",command=self.consultar_mod) #Inicio boton consultar
        self.boton1.grid(column=1, row=6, padx=4, pady=4) #Fin boton consultar
        self.boton1=Button(self.labelframe1, text="Modificar",bg="orange", command=self.modifica) #Inicio boton modificar
        self.boton1.grid(column=1, row=7, padx=4, pady=4) #Fin boton modificar

    def modifica(self):
        newcita = ''
        for caracter in self.fechacita2.get():
            if caracter != ' ':
                newcita = newcita+caracter
            else:
                break
        now = datetime.now()
        newnow = str(now.day)+'-'+str(now.month)+'-'+str(now.year)
        newnow1 = str(now.day)+'/'+str(now.month)+'/'+str(now.year)
        if self.fechacita2.get() == '' or (newcita <= newnow and newcita <= newnow1):
            mb.showinfo("Información", "Fecha de cita NO aceptada.")
        elif self.idmod.get() == '':
            mb.showinfo("Información", "ID paciente invalido.")
        elif self.cedulamod.get() == '':
            mb.showinfo("Información", "Cedula invalida.")
        elif len(self.idmod.get()) > 0 or self.idmod.get() == '':
            datos=(self.idmod.get(), )
            respuesta=self.cita1.consultaPac(datos)
            if len(respuesta)>0:
                if len(self.cedulamod.get()) > 0 or self.cedulamod.get() == '':
                    datos=(self.cedulamod.get(), )
                    respuesta=self.cita1.consultaDoc(datos)
                if len(respuesta)>0:
                    datos=(self.fechacita2.get(),self.idmod.get(),self.cedulamod.get())
                    cantidad=self.cita1.modificacion(datos)
                    if cantidad==1:
                        mb.showinfo("Información", "Se modificó la cita.")
                    else:
                        mb.showinfo("Información", "No existe alguna cita con dicha cedula e ID.")
                else:
                    mb.showinfo("Información", "Cedula invalida.")
            else:
                mb.showinfo("Información", "ID paciente invalido.")

    def consultar_mod(self):
        datos=(self.idmod.get(),self.cedulamod.get(), )
        respuesta=self.cita1.consulta(datos)
        if len(respuesta)>0:
            self.fechacita2.set(respuesta[0][0])
        else:
            self.fechacita2.set('')
            mb.showinfo("Información", "No existe alguna cita con dicha cedula e ID.")

    def regresar(self):
        self.ventanacita.destroy()
        aplicacion1=Formulario() #Llama a la clase principal 
#----------------------------------------------------------------------------------------

class Tratamiento:
    def abrir(self):
        conexion3 = psycopg2.connect(database="proyecto", user="postgres", password='yourpassw')
        return conexion3

    def alta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="insert into tratamiento (IDpaciente, IDtratamiento, nombreT, costo, medicamentos, descripción, cedula, fechaTratamiento) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, datos)
        cone.commit()

    def consulta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select nombreT, costo, medicamentos, descripción, cedula, fechaTratamiento from tratamiento where IDpaciente=%s and IDtratamiento =%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()
    
    def consultaPac(self,datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select nombre from paciente where IDpaciente=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()

    def consultaDoc(self,datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select nombre from doctor where cedula=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()

    def consultaTrat(self,datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select nombreT from tratamiento where IDtratamiento=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()
            
    def recuperar_todos(self):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select IDpaciente, IDtratamiento, nombreT, costo, medicamentos, descripción, cedula, fechaTratamiento from tratamiento"
        cursor.execute(sql)
        sql2 = "select * from tratamiento order by IDpaciente"
        cursor.execute(sql2)
        return cursor.fetchall()
    
    def baja(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="delete from tratamiento where IDpaciente=%s and IDtratamiento=%s"
        cursor.execute(sql, datos)
        cone.commit()
        return cursor.rowcount # retornamos la cantidad de filas borradas
            
    def modificacion(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="update tratamiento set nombreT=%s, costo=%s, medicamentos=%s, descripción=%s, cedula=%s, fechaTratamiento=%s where IDpaciente=%s and IDtratamiento=%s"
        cursor.execute(sql, datos)
        cone.commit()
        return cursor.rowcount # retornamos la cantidad de filas modificadas

class FormularioTratamiento:
    def __init__(self):
        mb.showinfo("Información sobre tratamientos", "-Las tratamientos del paciente se agregan mediante su ID.")
        self.tratamiento1=Tratamiento() #Se llama a la clase declarada
        self.ventanatratamiento=tk.Tk()  #Se crea una ventana 
        self.ventanatratamiento.config(bg="dodger blue")
        self.ventanatratamiento.title("Clinica Odontologica")  #Titulo de la ventana
        self.cuadernotratamiento1 = ttk.Notebook(self.ventanatratamiento)   #Se crea un cuaderno en la ventana 
        self.carga_Tratamiento()  #Metodos base
        self.consulta_por_codigo()
        self.listado_completo()
        self.borrado()
        self.modificar()
        style = ttk.Style()
        style.theme_use("classic")
        style.configure("TNotebook.Tab", background="green", font="helvetica 10")
        self.cuadernotratamiento1.grid(column=0, row=0, padx=60, pady=10) #Default 10x, 10y dimension del cuaderno
        self.ventanatratamiento.mainloop() #Ejecuta la ventana principal 
                
            
    def carga_Tratamiento(self):
        self.paginatratamiento1 = ttk.Frame(self.cuadernotratamiento1)
        self.cuadernotratamiento1.add(self.paginatratamiento1, text="Agregar tratamiento")
        self.labelframe1=ttk.LabelFrame(self.paginatratamiento1, text="Tratamiento")        
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10) #Default 5x, 10y
        self.label1=ttk.Label(self.labelframe1, text="-ID de paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=4, pady=4) #Default 4x, 4y
        self.idpacientetrat=tk.StringVar()
        self.entryidpacientetrat=ttk.Entry(self.labelframe1, textvariable=self.idpacientetrat) 
        self.entryidpacientetrat.grid(column=1, row=0, padx=4, pady=4) #Default 4x, 4y -Fin IDpaciente
        self.label2=ttk.Label(self.labelframe1, text="-ID tratamiento:") #Inicio IDtratamiento
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.idtrat=tk.StringVar()
        self.entryidtrat=ttk.Entry(self.labelframe1, textvariable=self.idtrat)
        self.entryidtrat.grid(column=1, row=1, padx=4, pady=4) #Default 4x, 4y -Fin IDtrat
        self.label3=ttk.Label(self.labelframe1, text="Nombre de tratamiento:") #Inicio nombreT
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.nombretrat=tk.StringVar()
        self.entrynombretrat=ttk.Entry(self.labelframe1, textvariable=self.nombretrat)
        self.entrynombretrat.grid(column=1, row=2, padx=4, pady=4) #Default 4x, 4y -Fin nombreT
        self.label4=ttk.Label(self.labelframe1, text="Costo:") #Inicio costoT
        self.label4.grid(column=0, row=3, padx=4, pady=4)
        self.costotrat=tk.StringVar()
        self.entrycostotrat=ttk.Entry(self.labelframe1, textvariable=self.costotrat)
        self.entrycostotrat.grid(column=1, row=3, padx=4, pady=4) #Default 4x, 4y -Fin costoT
        self.label5=ttk.Label(self.labelframe1, text="Medicamento/s:") #Inicio medicamentoT
        self.label5.grid(column=0, row=4, padx=4, pady=4)
        self.medicamentotrat=tk.StringVar()
        self.entrymedicamentotrat=ttk.Entry(self.labelframe1, textvariable=self.medicamentotrat)
        self.entrymedicamentotrat.grid(column=1, row=4, padx=4, pady=4) #Default 4x, 4y -Fin medicamentoT
        self.label6=ttk.Label(self.labelframe1, text="Descripcion del tratamiento:") #Inicio descripcionT
        self.label6.grid(column=0, row=5, padx=4, pady=4)
        self.descripciontrat=tk.StringVar()
        self.entrydescripciontrat=ttk.Entry(self.labelframe1, textvariable=self.descripciontrat)
        self.entrydescripciontrat.grid(column=1, row=5, padx=4, pady=4) #Default 4x, 4y -Fin descripcionT
        self.label7=ttk.Label(self.labelframe1, text="-Cedula Dr:") #Inicio cedula
        self.label7.grid(column=0, row=6, padx=4, pady=4)
        self.cedulatrat=tk.StringVar()
        self.entrycedulatrat=ttk.Entry(self.labelframe1, textvariable=self.cedulatrat)
        self.entrycedulatrat.grid(column=1, row=6, padx=4, pady=4) #Default 4x, 4y -Fin cedula
        self.label7=ttk.Label(self.labelframe1, text="Fecha tratamiento (DD/MM/AA):") #Inicio fechaT
        self.label7.grid(column=0, row=7, padx=4, pady=4)
        self.fechatrat=tk.StringVar()
        self.entryfechatrat=ttk.Entry(self.labelframe1, textvariable=self.fechatrat)
        self.entryfechatrat.grid(column=1, row=7, padx=4, pady=4) #Default 4x, 4y -Fin fechat
        self.botontratamiento1=Button(self.labelframe1, text="Confirmar", bg="red",command=self.agregarTratamiento) #Inicio boton agregarTratamiento
        self.botontratamiento1.grid(column=1, row=8, padx=4, pady=4) #Default 4x, 4y -Fin boton
        self.botonTratamiento2=Button(self.labelframe1, text="----> Regresar ", bg="deep sky blue",command=self.regresar) #Inicio boton agregarTratamiento
        self.botonTratamiento2.grid(column=4, row=9, padx=4, pady=4) #Default 4x, 4y -Fin boton
            
    def agregarTratamiento(self):
        if self.idpacientetrat.get() == '':
            mb.showinfo("Información", "ID paciente invalido.")
        elif self.idtrat.get() == '':
            mb.showinfo("Información", "ID tratamiento invalido.")
        elif self.cedulatrat.get() == '':
            mb.showinfo("Información", "Cedula invalida.")
        elif self.nombretrat.get() == '':
            mb.showinfo("Información", "Nombre invalido.")
        elif self.costotrat.get() == '':
            mb.showinfo("Información", "Costo invalido.")
        elif self.medicamentotrat.get() == '':
            mb.showinfo("Información", "Medicamento invalido.")
        elif self.descripciontrat.get() == '':
            mb.showinfo("Información", "Descripcion invalida.")
        elif self.fechatrat.get() == '':
            mb.showinfo("Información", "Fecha invalida.")
        elif len(self.idpacientetrat.get()) > 0 or self.idpacientetrat.get() == '':
            datos=(self.idpacientetrat.get(), )
            respuesta=self.tratamiento1.consultaPac(datos)
            if len(respuesta)>0:
                if len(self.cedulatrat.get()) > 0 or self.cedulatrat.get() == '':
                    datos=(self.cedulatrat.get(), )
                    respuesta=self.tratamiento1.consultaDoc(datos)
                if len(respuesta)>0:
                    if len(self.idtrat.get()) > 0 or self.idtrat.get() == '':
                        datos=(self.idtrat.get(), )
                        respuesta=self.tratamiento1.consultaTrat(datos)
                        if len(respuesta)>0 or self.idtrat.get() == '':
                            mb.showinfo("Información", "ID tratamiento invalido.")
                        else:
                            datos=(self.idpacientetrat.get(), self.idtrat.get(),self.nombretrat.get(),self.costotrat.get(),self.medicamentotrat.get(),self.descripciontrat.get(),self.cedulatrat.get(),self.fechatrat.get())              
                            self.tratamiento1.alta(datos)
                            mb.showinfo("Información", "Los datos fueron cargados con exito.")
                            self.idpacientetrat.set("")
                            self.idtrat.set("")
                            self.nombretrat.set("")
                            self.costotrat.set("")
                            self.medicamentotrat.set("")
                            self.descripciontrat.set("")
                            self.cedulatrat.set("")
                            self.fechatrat.set("")
                else:
                    mb.showinfo("Información", "Cedula invalida.")
            else:
                mb.showinfo("Información", "ID paciente invalido.")

    def consulta_por_codigo(self):
        self.pagina2 = ttk.Frame(self.cuadernotratamiento1)
        self.cuadernotratamiento1.add(self.pagina2, text="Consulta de tratamiento")
        self.labelframe1=ttk.LabelFrame(self.pagina2, text="Tratamiento")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe1, text="-ID paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.idpacientetrat1=tk.StringVar()
        self.entryidpacientetrat1=ttk.Entry(self.labelframe1, textvariable=self.idpacientetrat1) 
        self.entryidpacientetrat1.grid(column=1, row=0, padx=4, pady=4)  #Fin IDpaciente
        self.label2=ttk.Label(self.labelframe1, text="-ID tratamiento:") #Inicio IDtrat
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.idtrat1=tk.StringVar()
        self.entryidtrat1=ttk.Entry(self.labelframe1, textvariable=self.idtrat1)
        self.entryidtrat1.grid(column=1, row=1, padx=4, pady=4) #Default: 4x,4y -Fin IDtrat
        self.label3=ttk.Label(self.labelframe1, text="Nombre de tratamiento:") #Inicio nombreT
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.nombretrat1=tk.StringVar()
        self.entrynombretrat1=ttk.Entry(self.labelframe1, textvariable=self.nombretrat1, state="readonly")
        self.entrynombretrat1.grid(column=1, row=2, padx=4, pady=4) #Default: 4x,4y -Fin nombreT
        self.label4=ttk.Label(self.labelframe1, text="Nombre:") #Inicio costoT
        self.label4.grid(column=0, row=3, padx=4, pady=4)
        self.costotrat1=tk.StringVar()
        self.entrycostotrat1=ttk.Entry(self.labelframe1, textvariable=self.costotrat1, state="readonly")
        self.entrycostotrat1.grid(column=1, row=3, padx=4, pady=4) #Default: 4x,4y -Fin costoT
        self.label5=ttk.Label(self.labelframe1, text="Medicamento/s:") #Inicio medicamentoT
        self.label5.grid(column=0, row=4, padx=4, pady=4)
        self.medicamentotrat1=tk.StringVar()
        self.entrymedicamentotrat1=ttk.Entry(self.labelframe1, textvariable=self.medicamentotrat1, state="readonly")
        self.entrymedicamentotrat1.grid(column=1, row=4, padx=4, pady=4) #Default: 4x,4y -Fin medicamentoT
        self.label6=ttk.Label(self.labelframe1, text="Descripción de tratamiento:") #Inicio descripcionT
        self.label6.grid(column=0, row=5, padx=4, pady=4)
        self.descripciontrat1=tk.StringVar()
        self.entrydescripciontrat1=ttk.Entry(self.labelframe1, textvariable=self.descripciontrat1, state="readonly")
        self.entrydescripciontrat1.grid(column=1, row=5, padx=4, pady=4) #Default: 4x,4y -Fin descripcionT
        self.label7=ttk.Label(self.labelframe1, text="-Cedula Dr:") #Inicio cedula
        self.label7.grid(column=0, row=6, padx=4, pady=4)
        self.cedulatrat1=tk.StringVar()
        self.entrycedulatrat1=ttk.Entry(self.labelframe1, textvariable=self.cedulatrat1, state="readonly")
        self.entrycedulatrat1.grid(column=1, row=6, padx=4, pady=4) #Default: 4x,4y -Fin cedula
        self.label8=ttk.Label(self.labelframe1, text="Fecha de tratamiento:") #Inicio fechaT
        self.label8.grid(column=0, row=7, padx=4, pady=4)
        self.fechatrat1=tk.StringVar()
        self.entryfechatrat1=ttk.Entry(self.labelframe1, textvariable=self.fechatrat1, state="readonly")
        self.entryfechatrat1.grid(column=1, row=7, padx=4, pady=4) #Default: 4x,4y -Fin fechaT
        self.boton1=Button(self.labelframe1, text="Consultar", bg="deep sky blue",command=self.consultar) #Inicio boton consultar
        self.boton1.grid(column=1, row=18, padx=4, pady=4) #Fin boton consultar

    def consultar(self):
        datos=(self.idpacientetrat1.get(),self.idtrat1.get(), )
        respuesta=self.tratamiento1.consulta(datos)
        if len(respuesta)>0:
            self.nombretrat1.set(respuesta[0][0])
            self.costotrat1.set(respuesta[0][1])
            self.medicamentotrat1.set(respuesta[0][2])
            self.descripciontrat1.set(respuesta[0][3])
            self.cedulatrat1.set(respuesta[0][4])
            self.fechatrat1.set(respuesta[0][5])
        else:
            self.nombretrat.set('')
            self.costotrat.set('')
            self.medicamentotrat.set('')
            self.descripciontrat.set('')
            self.cedulatrat.set('')
            self.fechatrat.set('')
            mb.showinfo("Información", "No existe algun tratamiento con dicho ID paciente o ID tratamiento.")

    def listado_completo(self):
        self.pagina3 = ttk.Frame(self.cuadernotratamiento1)
        self.cuadernotratamiento1.add(self.pagina3, text="Listado de tratamientos")
        self.labelframe1=ttk.LabelFrame(self.pagina3, text="Tratamiento")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.boton1=Button(self.labelframe1, text="Listado completo",bg="spring green", command=self.listar) #Inicio boton listar
        self.boton1.grid(column=0, row=0, padx=4, pady=4) #Fin boton listar
        self.scrolledtext1=st.ScrolledText(self.labelframe1, width=70, height=30) #Default width=30, height=10
        self.scrolledtext1.grid(column=0,row=1, padx=10, pady=10) #Default 10x, 10y
    
    def listar(self):
        respuesta=self.tratamiento1.recuperar_todos()
        self.scrolledtext1.delete("1.0", tk.END)        
        for fila in respuesta:
            self.scrolledtext1.insert(tk.END, ">Código o ID paciente: "+str(fila[0])+
                                              "\n-ID tratamiento: "+str(fila[1])+
                                              "\nNombre de tratamiento: "+fila[2]+
                                              "\nCosto: "+str(fila[3])+
                                              "\nMedicamento/s: "+fila[4]+
                                              "\nDescripción del tratamiento: "+fila[5]+
                                              "\n-Cedula Dr: "+fila[6]+
                                              "\nFecha de tratamiento: "+str(fila[7])+"\n\n")

    def borrado(self):
        self.pagina4 = ttk.Frame(self.cuadernotratamiento1)
        self.cuadernotratamiento1.add(self.pagina4, text="Eliminar tratamiento")
        self.labelframe1=ttk.LabelFrame(self.pagina4, text="Tratamiento")        
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10) #Default: 5x,10y
        self.label1=ttk.Label(self.labelframe1, text="-ID paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=50, pady=100) #Default: 4x,4y
        self.idborra=tk.IntVar()
        self.entryborra=ttk.Entry(self.labelframe1, textvariable=self.idborra)
        self.entryborra.grid(column=1, row=0, padx=50, pady=107) #Default: 4x,4y -Fin IDpaciente
        self.label1=ttk.Label(self.labelframe1, text="-ID tratamiento:") #Inicio IDtrat
        self.label1.grid(column=0, row=1, padx=4, pady=4) #Default: 4x,4y
        self.idtratborra=tk.StringVar()
        self.entryidtratborra1=ttk.Entry(self.labelframe1, textvariable=self.idtratborra)
        self.entryidtratborra1.grid(column=1, row=1, padx=4, pady=4) #Default: 4x,4y -Fin IDtrat

        self.boton1=Button(self.labelframe1, text="Borrar",bg="red", command=self.borrar) #Inicio boton borrar
        self.boton1.grid(column=1, row=2, padx=4, pady=4) #Fin boton borrar
    
    def borrar(self):
        datos=(self.idborra.get(),self.idtratborra.get(), )
        cantidad=self.tratamiento1.baja(datos)
        if cantidad==1:
            mb.showinfo("Información", "Se borró el tratamiento con dichos ID.")
        else:
            mb.showinfo("Información", "No existe algun tratamiento con dichos ID.")
    
    def modificar(self):
        self.pagina5 = ttk.Frame(self.cuadernotratamiento1)
        self.cuadernotratamiento1.add(self.pagina5, text="Modificar tratamiento")
        self.labelframe1=ttk.LabelFrame(self.pagina5, text="Tratamiento")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe1, text="-ID paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.idmod=tk.StringVar()
        self.entryidmod=ttk.Entry(self.labelframe1, textvariable=self.idmod)
        self.entryidmod.grid(column=1, row=0, padx=4, pady=4) #Fin IDpaciente
        self.label2=ttk.Label(self.labelframe1, text="-ID tratamiento:") #Inicio IDtrat
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.idtratmod=tk.StringVar()
        self.entryidtratmod=ttk.Entry(self.labelframe1, textvariable=self.idtratmod)
        self.entryidtratmod.grid(column=1, row=1, padx=4, pady=4) #Default: 4x,4y -Fin IDtrat
        self.label3=ttk.Label(self.labelframe1, text="Nombre de tratamiento:") #Inicio nombreT
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.nombretrat2=tk.StringVar()
        self.entrynombretrat2=ttk.Entry(self.labelframe1, textvariable=self.nombretrat2)
        self.entrynombretrat2.grid(column=1, row=2, padx=4, pady=4) #Default: 4x,4y -Fin nombreT
        self.label4=ttk.Label(self.labelframe1, text="Costo:") #Inicio costoT
        self.label4.grid(column=0, row=3, padx=4, pady=4)
        self.costotrat2=tk.StringVar()
        self.entrycostotrat2=ttk.Entry(self.labelframe1, textvariable=self.costotrat2)
        self.entrycostotrat2.grid(column=1, row=3, padx=4, pady=4) #Default: 4x,4y -Fin costoT
        self.label5=ttk.Label(self.labelframe1, text="Medicamento/s:") #Inicio medicamentoT
        self.label5.grid(column=0, row=4, padx=4, pady=4)
        self.medicamentotrat2=tk.StringVar()
        self.entrymedicamentotrat2=ttk.Entry(self.labelframe1, textvariable=self.medicamentotrat2)
        self.entrymedicamentotrat2.grid(column=1, row=4, padx=4, pady=4) #Default: 4x,4y -Fin medicamentoT
        self.label6=ttk.Label(self.labelframe1, text="Descripción de tratamiento:") #Inicio descripcionT
        self.label6.grid(column=0, row=5, padx=4, pady=4)
        self.descripciontrat2=tk.StringVar()
        self.entrydescripciontrat2=ttk.Entry(self.labelframe1, textvariable=self.descripciontrat2)
        self.entrydescripciontrat2.grid(column=1, row=5, padx=4, pady=4) #Default: 4x,4y -Fin descripcionT
        self.label7=ttk.Label(self.labelframe1, text="Cedula Dr:") #Inicio cedula
        self.label7.grid(column=0, row=6, padx=4, pady=4)
        self.cedulatrat2=tk.StringVar()
        self.entrycedulatrat2=ttk.Entry(self.labelframe1, textvariable=self.cedulatrat2)
        self.entrycedulatrat2.grid(column=1, row=6, padx=4, pady=4) #Default: 4x,4y -Fin cedula
        self.label8=ttk.Label(self.labelframe1, text="Fecha de tratamiento (DD/MM/AA):") #Inicio fechaT
        self.label8.grid(column=0, row=7, padx=4, pady=4)
        self.fechatrat2=tk.StringVar()
        self.entryfechatrat2=ttk.Entry(self.labelframe1, textvariable=self.fechatrat2)
        self.entryfechatrat2.grid(column=1, row=7, padx=4, pady=4) #Default: 4x,4y -Fin fecha T

        self.boton1=Button(self.labelframe1, text="Consultar", bg="deep sky blue",command=self.consultar_mod) #Inicio boton consultar
        self.boton1.grid(column=1, row=8, padx=4, pady=4) #Fin boton consultar
        self.boton1=Button(self.labelframe1, text="Modificar", bg="orange",command=self.modifica) #Inicio boton modificar
        self.boton1.grid(column=1, row=9, padx=4, pady=4) #Fin boton modificar

    def modifica(self):
        if self.idmod.get() == '':
            mb.showinfo("Información", "ID paciente invalido.")
        elif self.idtratmod.get() == '':
            mb.showinfo("Información", "ID tratamiento invalido.")
        elif self.cedulatrat2.get() == '':
            mb.showinfo("Información", "Cedula invalida.")
        elif self.nombretrat2.get() == '':
            mb.showinfo("Información", "Nombre invalido.")
        elif self.costotrat2.get() == '':
            mb.showinfo("Información", "Costo invalido.")
        elif self.medicamentotrat2.get() == '':
            mb.showinfo("Información", "Medicamento invalido.")
        elif self.descripciontrat2.get() == '':
            mb.showinfo("Información", "Descripcion invalida.")
        elif self.fechatrat2.get() == '':
            mb.showinfo("Información", "Fecha invalida.")
        elif len(self.idmod.get()) > 0 or self.idmod.get() == '':
            datos=(self.idmod.get(), )
            respuesta=self.tratamiento1.consultaPac(datos)
            if len(respuesta)>0:
                if len(self.cedulatrat2.get()) > 0 or self.cedulatrat2.get() == '':
                    datos=(self.cedulatrat2.get(), )
                    respuesta=self.tratamiento1.consultaDoc(datos)
                    if len(respuesta)>0:
                        if len(self.idtratmod.get()) > 0 or self.idtratmod.get() == '':
                            datos=(self.idtratmod.get(), )
                            respuesta=self.tratamiento1.consultaTrat(datos)
                            if len(respuesta)>0:
                                datos=(self.nombretrat2.get(),self.costotrat2.get(),self.medicamentotrat2.get(),self.descripciontrat2.get(),self.cedulatrat2.get(),self.fechatrat2.get(),self.idmod.get(),self.idtratmod.get())
                                cantidad=self.tratamiento1.modificacion(datos)
                                if cantidad==1:
                                    mb.showinfo("Información", "Se modificó el tratamiento.")
                                else:
                                    mb.showinfo("Información", "No existe algun tratamiento con dichos ID.")
                            else:
                                mb.showinfo("Información", "ID tratamiento invalido.")
                    else:
                        mb.showinfo("Información", "Cedula invalida.")
            else:
                mb.showinfo("Información", "ID paciente invalido.")
                        

    def consultar_mod(self):
        datos=(self.idmod.get(),self.idtratmod.get(), )
        respuesta=self.tratamiento1.consulta(datos)
        if len(respuesta)>0:
            self.nombretrat2.set(respuesta[0][0])
            self.costotrat2.set(respuesta[0][1])
            self.medicamentotrat2.set(respuesta[0][2])
            self.descripciontrat2.set(respuesta[0][3])
            self.cedulatrat2.set(respuesta[0][4])
            self.fechatrat2.set(respuesta[0][5])
        else:
            self.nombretrat2.set('')
            self.costotrat2.set('')
            self.medicamentotrat2.set('')
            self.descripciontrat2.set('')
            self.cedulatrat2.set('')
            self.fechatrat2.set('')
            mb.showinfo("Información", "No existe algun tratamiento con dichos ID.")

    def regresar(self):
        self.ventanatratamiento.destroy()
        aplicacion1=Formulario() #Llama a la clase principal 

#---------------------------------------------------------------------------------------------

class Pago:
    def abrir(self):
        conexion4 = psycopg2.connect(database="proyecto", user="postgres", password='yourpassw')
        return conexion4

    def alta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="insert into pago (IDpaciente, IDtratamiento, cedula, fechaP, metodopago) values (%s,%s,%s,%s,%s)"
        cursor.execute(sql, datos)
        cone.commit()

    def consulta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select cedula, fechaP, metodopago from pago where IDpaciente=%s and IDtratamiento =%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()
    
    def consultaPac(self,datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select nombre from paciente where IDpaciente=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()

    def consultaDoc(self,datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select nombre from doctor where cedula=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()

    def consultaTrat(self,datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select nombreT from tratamiento where IDtratamiento=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()
            
    def recuperar_todos(self):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select IDpaciente, IDtratamiento, cedula, fechaP, metodopago from pago"
        cursor.execute(sql)
        sql2 = "select * from pago order by IDpaciente"
        cursor.execute(sql2)
        return cursor.fetchall()
    
    def baja(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="delete from pago where IDpaciente=%s and IDtratamiento=%s"
        cursor.execute(sql, datos)
        cone.commit()
        return cursor.rowcount # retornamos la cantidad de filas borradas
            
    def modificacion(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="update pago set cedula=%s, fechaP=%s, metodopago=%s where IDpaciente=%s and IDtratamiento=%s"
        cursor.execute(sql, datos)
        cone.commit()
        return cursor.rowcount # retornamos la cantidad de filas modificadas

class FormularioPago:
    def __init__(self):
        mb.showinfo("Información sobre pagos", "-Las pagos del paciente se agregan mediante su ID y su ID de tratamiento.")
        self.pago1=Pago() #Se llama a la clase declarada
        self.ventanapago=tk.Tk()  #Se crea una ventana 
        self.ventanapago.config(bg="dodger blue")
        self.ventanapago.title("Clinica Odontologica")  #Titulo de la ventana
        self.cuadernopago1 = ttk.Notebook(self.ventanapago)   #Se crea un cuaderno en la ventana 
        self.carga_Pago()  #Metodos base
        self.consulta_por_codigo()
        self.listado_completo()
        self.borrado()
        self.modificar()
        style = ttk.Style()
        style.theme_use("classic")
        style.configure("TNotebook.Tab", background="green", font="helvetica 10")
        self.cuadernopago1.grid(column=0, row=0, padx=60, pady=10) #Default 10x, 10y dimension del cuaderno
        self.ventanapago.mainloop() #Ejecuta la ventana principal 
                
            
    def carga_Pago(self):
        self.paginapago1 = ttk.Frame(self.cuadernopago1)
        self.cuadernopago1.add(self.paginapago1, text="Agregar Pago")
        self.labelframe1=ttk.LabelFrame(self.paginapago1, text="Pago")        
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10) #Default 5x, 10y
        self.label1=ttk.Label(self.labelframe1, text="-ID de paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=4, pady=4) #Default 4x, 4y
        self.idpacientepago=tk.StringVar()
        self.entryidpacientepago=ttk.Entry(self.labelframe1, textvariable=self.idpacientepago) 
        self.entryidpacientepago.grid(column=1, row=0, padx=4, pady=4) #Default 4x, 4y -Fin IDpaciente
        self.label2=ttk.Label(self.labelframe1, text="-ID tratamiento:") #Inicio IDtrat
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.idtratpago=tk.StringVar()
        self.entryidtratpago=ttk.Entry(self.labelframe1, textvariable=self.idtratpago)
        self.entryidtratpago.grid(column=1, row=1, padx=4, pady=4) #Default 4x, 4y -Fin IDtrat
        self.label3=ttk.Label(self.labelframe1, text="-Cedula Dr:") #Inicio cedula
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.cedulapago=tk.StringVar()
        self.entrycedulapago=ttk.Entry(self.labelframe1, textvariable=self.cedulapago)
        self.entrycedulapago.grid(column=1, row=2, padx=4, pady=4) #Default 4x, 4y -Fin cedula
        self.label4=ttk.Label(self.labelframe1, text="Fecha (DD/MM/AA):\nNota: La fecha debe ser actual.") #Inicio fechaP
        self.label4.grid(column=0, row=3, padx=4, pady=4)
        self.fechapago=tk.StringVar()
        self.entryfechapago=ttk.Entry(self.labelframe1, textvariable=self.fechapago)
        self.entryfechapago.grid(column=1, row=3, padx=4, pady=4) #Default 4x, 4y -Fin metodoP
        self.label5=ttk.Label(self.labelframe1, text="Metodo de pago:\n-Efectivo\n-Tarjeta\n-Servicio en linea") #Inicio fechaP
        self.label5.grid(column=0, row=4, padx=4, pady=4)
        self.metodopago=tk.StringVar()
        self.entrymetodopago=ttk.Entry(self.labelframe1, textvariable=self.metodopago)
        self.entrymetodopago.grid(column=1, row=4, padx=4, pady=4) #Default 4x, 4y -Fin metodoP

        self.botonpago1=Button(self.labelframe1, text="Confirmar",bg="red", command=self.agregarPago) #Inicio boton agregarPago
        self.botonpago1.grid(column=1, row=8, padx=4, pady=4) #Default 4x, 4y -Fin boton
        self.botonPago2=Button(self.labelframe1, text="----> Regresar ", bg="deep sky blue",command=self.regresar) #Inicio boton agregarPago
        self.botonPago2.grid(column=4, row=9, padx=4, pady=4) #Default 4x, 4y -Fin boton
            
    def agregarPago(self):
        now = datetime.now()
        newnow = str(now.day)+'-'+str(now.month)+'-'+str(now.year)
        newnow1 = str(now.day)+'/'+str(now.month)+'/'+str(now.year)
        if self.fechapago.get() == '' or (self.fechapago.get() != newnow and self.fechapago.get() != newnow1):
            mb.showinfo("Información", "Fecha NO aceptada.")
        elif self.metodopago.get() == '' or (self.metodopago.get() != 'efectivo' and self.metodopago.get() != 'Efectivo' and self.metodopago.get() != 'Tarjeta' and self.metodopago.get() != 'tarjeta' and self.metodopago.get() != 'Servicio en linea' and self.metodopago.get() != 'servicio en linea' and self.metodopago.get() != 'SERVICIO EN LINEA' and self.metodopago.get() != 'EFECTIVO' and self.metodopago.get() != 'TARJETA'):
            mb.showinfo("Información", "Metodo de pago no aceptado.")
        elif self.idpacientepago.get() == '':
            mb.showinfo("Información", "ID paciente invalido.")
        elif self.idtratpago.get() == '':
            mb.showinfo("Información", "ID tratamiento invalido.")
        elif self.cedulapago.get() == '':
            mb.showinfo("Información", "Cedula invalida.")
        elif len(self.idpacientepago.get()) > 0 or self.idpacientepago.get() == '':
            datos=(self.idpacientepago.get(), )
            respuesta=self.pago1.consultaPac(datos)
            if len(respuesta)>0:
                if len(self.cedulapago.get()) > 0 or self.cedulapago.get() == '':
                    datos=(self.cedulapago.get(), )
                    respuesta=self.pago1.consultaDoc(datos)
                    if len(respuesta)>0:
                        if len(self.idtratpago.get()) > 0 or self.idtratpago.get() == '':
                            datos=(self.idtratpago.get(), )
                            respuesta=self.pago1.consultaTrat(datos)
                            if len(respuesta)>0:
                                datos=(self.idpacientepago.get(), self.idtratpago.get(),self.cedulapago.get(),self.fechapago.get(),self.metodopago.get())              
                                self.pago1.alta(datos)
                                mb.showinfo("Información", "Los datos fueron cargados con exito.")
                                self.idpacientepago.set("")
                                self.idtratpago.set("")
                                self.cedulapago.set("")
                                self.fechapago.set("")
                                self.metodopago.set("")
                            else:
                                mb.showinfo("Información", "ID tratamiento invalido.")
                    else:
                        mb.showinfo("Información", "Cedula invalida.")
            else:
                mb.showinfo("Información", "ID paciente invalido.")
    
    def consulta_por_codigo(self):
        self.pagina2 = ttk.Frame(self.cuadernopago1)
        self.cuadernopago1.add(self.pagina2, text="Consulta de pagos")
        self.labelframe1=ttk.LabelFrame(self.pagina2, text="Pago")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe1, text="-ID paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.idpacientepago1=tk.StringVar()
        self.entryidpacientepago1=ttk.Entry(self.labelframe1, textvariable=self.idpacientepago1) 
        self.entryidpacientepago1.grid(column=1, row=0, padx=4, pady=4)  #Fin IDpaciente
        self.label2=ttk.Label(self.labelframe1, text="-ID tratamiento:") #Inicio IDtrat
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.idtratpago1=tk.StringVar()
        self.entryidtratpago1=ttk.Entry(self.labelframe1, textvariable=self.idtratpago1)
        self.entryidtratpago1.grid(column=1, row=1, padx=4, pady=4) #Default: 4x,4y -Fin IDtrat
        self.label3=ttk.Label(self.labelframe1, text="-Cedula Dr:") #Inicio cedula
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.cedulapago1=tk.StringVar()
        self.entrycedulapago1=ttk.Entry(self.labelframe1, textvariable=self.cedulapago1, state="readonly")
        self.entrycedulapago1.grid(column=1, row=2, padx=4, pady=4) #Default: 4x,4y -Fin cedula
        self.label4=ttk.Label(self.labelframe1, text="Fecha de pago:") #Inicio fechaP
        self.label4.grid(column=0, row=3, padx=4, pady=4)
        self.fechapago1=tk.StringVar()
        self.entryfechapago1=ttk.Entry(self.labelframe1, textvariable=self.fechapago1, state="readonly")
        self.entryfechapago1.grid(column=1, row=3, padx=4, pady=4) #Default: 4x,4y -Fin fechaP
        self.label5=ttk.Label(self.labelframe1, text="Metodo de pago:") #Inicio metodoP
        self.label5.grid(column=0, row=4, padx=4, pady=4)
        self.metodopago1=tk.StringVar()
        self.entrymetodopago1=ttk.Entry(self.labelframe1, textvariable=self.metodopago1, state="readonly")
        self.entrymetodopago1.grid(column=1, row=4, padx=4, pady=4) #Default: 4x,4y -Fin metodoP

        self.boton1=Button(self.labelframe1, text="Consultar",bg="deep sky blue", command=self.consultar) #Inicio boton consultar
        self.boton1.grid(column=1, row=18, padx=4, pady=4) #Fin boton consultar

    def consultar(self):
        datos=(self.idpacientepago1.get(),self.idtratpago1.get(), )
        respuesta=self.pago1.consulta(datos)
        if len(respuesta)>0:
            self.cedulapago1.set(respuesta[0][0])
            self.fechapago1.set(respuesta[0][1])
            self.metodopago1.set(respuesta[0][2])
        else:
            self.cedulapago.set('')
            self.fechapago.set('')
            self.metodopago.set('')
            mb.showinfo("Información", "No existe algun pago con dicho ID paciente o ID tratamiento.")

    def listado_completo(self):
        self.pagina3 = ttk.Frame(self.cuadernopago1)
        self.cuadernopago1.add(self.pagina3, text="Listado de Pagos")
        self.labelframe1=ttk.LabelFrame(self.pagina3, text="Pago")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.boton1=Button(self.labelframe1, text="Listado completo", bg="spring green",command=self.listar) #Inicio boton listar
        self.boton1.grid(column=0, row=0, padx=4, pady=4) #Fin boton listar
        self.scrolledtext1=st.ScrolledText(self.labelframe1, width=70, height=30) #Default width=30, height=10
        self.scrolledtext1.grid(column=0,row=1, padx=10, pady=10) #Default 10x, 10y
    
    def listar(self):
        respuesta=self.pago1.recuperar_todos()
        self.scrolledtext1.delete("1.0", tk.END)        
        for fila in respuesta:
            self.scrolledtext1.insert(tk.END, ">ID de paciente: "+str(fila[0])+
                                              "\n-ID tratamiento: "+str(fila[1])+
                                              "\n-Cedula: "+fila[2]+
                                              "\nFecha de pago: "+str(fila[3])+
                                              "\nMetodo de pago: "+fila[4]+"\n\n")
    
    def borrado(self):
        self.pagina4 = ttk.Frame(self.cuadernopago1)
        self.cuadernopago1.add(self.pagina4, text="Eliminar pago")
        self.labelframe1=ttk.LabelFrame(self.pagina4, text="Pago")        
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10) #Default: 5x,10y
        self.label1=ttk.Label(self.labelframe1, text="-ID paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=50, pady=100) #Default: 4x,4y
        self.idborra=tk.IntVar()
        self.entryborra=ttk.Entry(self.labelframe1, textvariable=self.idborra)
        self.entryborra.grid(column=1, row=0, padx=50, pady=107) #Default: 4x,4y -Fin IDpaciente
        self.label1=ttk.Label(self.labelframe1, text="-ID tratamiento:") #Inicio cedula
        self.label1.grid(column=0, row=1, padx=4, pady=4) #Default: 4x,4y
        self.idtratpagoborra=tk.StringVar()
        self.entryborra1=ttk.Entry(self.labelframe1, textvariable=self.idtratpagoborra)
        self.entryborra1.grid(column=1, row=1, padx=4, pady=4) #Default: 4x,4y -Fin cedula

        self.boton1=Button(self.labelframe1, text="Borrar", bg="red",command=self.borrar) #Inicio boton borrar
        self.boton1.grid(column=1, row=2, padx=4, pady=4) #Fin boton borrar
    
    def borrar(self):
        datos=(self.idborra.get(),self.idtratpagoborra.get(), )
        cantidad=self.pago1.baja(datos)
        if cantidad==1:
            mb.showinfo("Información", "Se borró el pago con dichos ID.")
        else:
            mb.showinfo("Información", "No existe algun pago con dichos ID.")
    
    def modificar(self):
        self.pagina5 = ttk.Frame(self.cuadernopago1)
        self.cuadernopago1.add(self.pagina5, text="Modificar pago")
        self.labelframe1=ttk.LabelFrame(self.pagina5, text="Pago")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe1, text="-ID paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.idmod=tk.StringVar()
        self.entryidmod=ttk.Entry(self.labelframe1, textvariable=self.idmod)
        self.entryidmod.grid(column=1, row=0, padx=4, pady=4) #Fin IDpaciente
        self.label2=ttk.Label(self.labelframe1, text="-ID tratamiento:") #Inicio IDtrat
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.idtratpagomod=tk.StringVar()
        self.entryidtratpagomod=ttk.Entry(self.labelframe1, textvariable=self.idtratpagomod)
        self.entryidtratpagomod.grid(column=1, row=1, padx=4, pady=4) #Default: 4x,4y -Fin IDtrat
        self.label3=ttk.Label(self.labelframe1, text="-Cedula:") #Inicio cedula
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.cedulapago2=tk.StringVar()
        self.entrycedulapago2=ttk.Entry(self.labelframe1, textvariable=self.cedulapago2)
        self.entrycedulapago2.grid(column=1, row=2, padx=4, pady=4) #Default: 4x,4y -Fin cedula
        self.label4=ttk.Label(self.labelframe1, text="Fecha (AA/M/DD):") #Inicio fechaP
        self.label4.grid(column=0, row=3, padx=4, pady=4)
        self.fechapago2=tk.StringVar()
        self.entryfechapago2=ttk.Entry(self.labelframe1, textvariable=self.fechapago2)
        self.entryfechapago2.grid(column=1, row=3, padx=4, pady=4) #Default: 4x,4y -Fin fechaP
        self.label4=ttk.Label(self.labelframe1, text="Metodo de pago:") #Inicio metodoP
        self.label4.grid(column=0, row=4, padx=4, pady=4)
        self.metodopago2=tk.StringVar()
        self.entrymetodopago2=ttk.Entry(self.labelframe1, textvariable=self.metodopago2)
        self.entrymetodopago2.grid(column=1, row=4, padx=4, pady=4) #Default: 4x,4y -Fin metodoP

        self.boton1=Button(self.labelframe1, text="Consultar",bg="deep sky blue", command=self.consultar_mod) #Inicio boton consultar
        self.boton1.grid(column=1, row=6, padx=4, pady=4) #Fin boton consultar
        self.boton1=Button(self.labelframe1, text="Modificar",bg="orange", command=self.modifica) #Inicio boton modificar
        self.boton1.grid(column=1, row=7, padx=4, pady=4) #Fin boton modificar

    def modifica(self):
        now = datetime.now()
        newnow = str(now.day)+'-'+str(now.month)+'-'+str(now.year)
        newnow1 = str(now.day)+'/'+str(now.month)+'/'+str(now.year)
        if self.fechapago2.get() == '' or (self.fechapago2.get() != newnow and self.fechapago2.get() != newnow1):
            mb.showinfo("Información", "Fecha NO aceptada.")
        elif self.metodopago2.get() == '' or (self.metodopago2.get() != 'efectivo' and self.metodopago2.get() != 'Efectivo' and self.metodopago2.get() != 'Tarjeta' and self.metodopago2.get() != 'tarjeta' and self.metodopago2.get() != 'Servicio en linea' and self.metodopago2.get() != 'servicio en linea' and self.metodopago2.get() != 'SERVICIO EN LINEA' and self.metodopago2.get() != 'EFECTIVO' and self.metodopago2.get() != 'TARJETA'):
            mb.showinfo("Información", "Metodo de pago no aceptado.")
        elif self.idmod.get() == '':
            mb.showinfo("Información", "ID paciente invalido.")
        elif self.idtratpagomod.get() == '':
            mb.showinfo("Información", "ID tratamiento invalido.")
        elif self.cedulapago2.get() == '':
            mb.showinfo("Información", "Cedula invalida.")
        elif len(self.idmod.get()) > 0 or self.idmod.get() == '':
            datos=(self.idmod.get(), )
            respuesta=self.pago1.consultaPac(datos)
            if len(respuesta)>0:
                if len(self.cedulapago2.get()) > 0 or self.cedulapago2.get() == '':
                    datos=(self.cedulapago2.get(), )
                    respuesta=self.pago1.consultaDoc(datos)
                    if len(respuesta)>0:
                        if len(self.idtratpagomod.get()) > 0 or self.idtratpagomod.get() == '':
                            datos=(self.idtratpagomod.get(), )
                            respuesta=self.pago1.consultaTrat(datos)
                            if len(respuesta)>0:
                                datos=(self.cedulapago2.get(),self.fechapago2.get(),self.metodopago2.get(),self.idmod.get(),self.idtratpagomod.get())
                                cantidad=self.pago1.modificacion(datos)
                                if cantidad==1:
                                    mb.showinfo("Información", "Se modificó el pago.")
                                else:
                                    mb.showinfo("Información", "No existe algun pago con dichos ID.")
                            else:
                                mb.showinfo("Información", "ID tratamiento invalido.")
                    else:
                        mb.showinfo("Información", "Cedula invalida.")
            else:
                mb.showinfo("Información", "ID paciente invalido.")

    def consultar_mod(self):
        datos=(self.idmod.get(),self.idtratpagomod.get(), )
        respuesta=self.pago1.consulta(datos)
        if len(respuesta)>0:
            self.cedulapago2.set(respuesta[0][0])
            self.fechapago2.set(respuesta[0][1])
            self.metodopago2.set(respuesta[0][2])
        else:
            self.cedulapago2.set('')
            self.fechapago2.set('')
            self.metodopago2.set('')
            mb.showinfo("Información", "No existe algun pago con dichos ID.")

    def regresar(self):
        self.ventanapago.destroy()
        aplicacion1=Formulario() #Llama a la clase principal 

#-----------------------------------------------------------------------------------------

class Vacunas:
    def abrir(self):
        conexion5 = psycopg2.connect(database="proyecto", user="postgres", password='yourpassw')
        return conexion5

    def alta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="insert into vacunas (IDpaciente, tipo_vacuna, fechavacuna) values (%s,%s,%s)"
        cursor.execute(sql, datos)
        cone.commit()

    def consulta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select tipo_vacuna, fechavacuna from vacunas where IDpaciente=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()
    
    def consultaPac(self,datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select nombre from paciente where IDpaciente=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()
            
    def recuperar_todos(self):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select IDpaciente, tipo_vacuna, fechavacuna from vacunas"
        cursor.execute(sql)
        sql2 = "select * from vacunas order by IDpaciente"
        cursor.execute(sql2)
        return cursor.fetchall()
    
    def baja(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="delete from vacunas where IDpaciente=%s"
        cursor.execute(sql, datos)
        cone.commit()
        return cursor.rowcount # retornamos la cantidad de filas borradas
            
    def modificacion(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="update vacunas set tipo_vacuna=%s,fechavacuna=%s where IDpaciente=%s"
        cursor.execute(sql, datos)
        cone.commit()
        return cursor.rowcount # retornamos la cantidad de filas modificadas

class FormularioVacunas:
    def __init__(self):
        mb.showinfo("Información sobre vacunas", "-Las vacunas del paciente se agregan mediante su ID.")
        self.vacunas1=Vacunas() #Se llama a la clase declarada
        self.ventanavacunas=tk.Tk()  #Se crea una ventana 
        self.ventanavacunas.config(bg="dodger blue")
        self.ventanavacunas.title("Clinica Odontologica")  #Titulo de la ventana
        self.cuadernovacunas1 = ttk.Notebook(self.ventanavacunas)   #Se crea un cuaderno en la ventana 
        self.carga_Vacunas()  #Metodos base
        self.consulta_por_codigo()
        self.listado_completo()
        self.borrado()
        self.modificar()
        style = ttk.Style()
        style.theme_use("classic")
        style.configure("TNotebook.Tab", background="green", font="helvetica 10")
        self.cuadernovacunas1.grid(column=0, row=0, padx=60, pady=10) #Default 10x, 10y dimension del cuaderno
        self.ventanavacunas.mainloop() #Ejecuta la ventana principal 
                
            
    def carga_Vacunas(self):
        self.paginavacunas1 = ttk.Frame(self.cuadernovacunas1)
        self.cuadernovacunas1.add(self.paginavacunas1, text="Agregar Vacunas")
        self.labelframe1=ttk.LabelFrame(self.paginavacunas1, text="Vacunas")        
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10) #Default 5x, 10y
        self.label1=ttk.Label(self.labelframe1, text="-ID de paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=4, pady=4) #Default 4x, 4y
        self.idpacientevacuna=tk.StringVar()
        self.entryidpacientevacuna=ttk.Entry(self.labelframe1, textvariable=self.idpacientevacuna) 
        self.entryidpacientevacuna.grid(column=1, row=0, padx=4, pady=4) #Default 4x, 4y -Fin IDpaciente
        self.label2=ttk.Label(self.labelframe1, text="Tipo de vacuna:") #Inicio tipoV
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.tipovacuna=tk.StringVar()
        self.entrytipovacuna=ttk.Entry(self.labelframe1, textvariable=self.tipovacuna)
        self.entrytipovacuna.grid(column=1, row=1, padx=4, pady=4) #Default 4x, 4y -Fin tipoV
        self.label3=ttk.Label(self.labelframe1, text="Fecha de aplicación (DD/MM/AA):") #Inicio fechaV
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.fechavacuna=tk.StringVar()
        self.entryfechavacuna=ttk.Entry(self.labelframe1, textvariable=self.fechavacuna)
        self.entryfechavacuna.grid(column=1, row=2, padx=4, pady=4) #Default 4x, 4y -Fin fechaV

        self.botonvacunas1=Button(self.labelframe1, text="Confirmar",bg="red", command=self.agregarVacunas) #Inicio boton agregarVacunas
        self.botonvacunas1.grid(column=1, row=8, padx=4, pady=4) #Default 4x, 4y -Fin boton
        self.botonVacunas2=Button(self.labelframe1, text="----> Regresar ", bg="deep sky blue",command=self.regresar) #Inicio boton agregarVacunas
        self.botonVacunas2.grid(column=4, row=9, padx=4, pady=4) #Default 4x, 4y -Fin boton
            
    def agregarVacunas(self):
        if self.idpacientevacuna.get() == '':
            mb.showinfo("Información", "ID paciente invalido.")
        elif self.tipovacuna.get() == '':
            mb.showinfo("Información", "Debe añadir un tipo de vacuna.")
        elif self.fechavacuna.get() == '':
            mb.showinfo("Información", "Debe añadir fecha de aplicación de la vacuna.")
        elif len(self.idpacientevacuna.get()) > 0 or self.idpacientevacuna.get() == '':
            datos=(self.idpacientevacuna.get(), )
            respuesta=self.vacunas1.consultaPac(datos)
            if len(respuesta)>0:
                datos=(self.idpacientevacuna.get(), self.tipovacuna.get(),self.fechavacuna.get())              
                self.vacunas1.alta(datos)
                mb.showinfo("Información", "Los datos fueron cargados con exito.")
                self.idpacientevacuna.set("")
                self.tipovacuna.set("")
                self.fechavacuna.set("")
            else:
                mb.showinfo("Información", "ID paciente invalido.")

    
    def consulta_por_codigo(self):
        self.pagina2 = ttk.Frame(self.cuadernovacunas1)
        self.cuadernovacunas1.add(self.pagina2, text="Consulta de vacunas")
        self.labelframe1=ttk.LabelFrame(self.pagina2, text="Vacunas")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe1, text="-ID paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.idpacientevacuna1=tk.StringVar()
        self.entryidpacientevacuna1=ttk.Entry(self.labelframe1, textvariable=self.idpacientevacuna1) 
        self.entryidpacientevacuna1.grid(column=1, row=0, padx=4, pady=4)  #Fin IDpaciente
        self.label2=ttk.Label(self.labelframe1, text="Tipo de vacuna:") #Inicio tipoV
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.tipovacuna1=tk.StringVar()
        self.entrytipovacuna1=ttk.Entry(self.labelframe1, textvariable=self.tipovacuna1, state="readonly")
        self.entrytipovacuna1.grid(column=1, row=1, padx=4, pady=4) #Default: 4x,4y -Fin tipoV
        self.label3=ttk.Label(self.labelframe1, text="Fecha de aplicación:") #Inicio fechaV
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.fechavacuna1=tk.StringVar()
        self.entryfechavacuna1=ttk.Entry(self.labelframe1, textvariable=self.fechavacuna1, state="readonly")
        self.entryfechavacuna1.grid(column=1, row=2, padx=4, pady=4) #Default: 4x,4y -Fin fechaV

        self.boton1=Button(self.labelframe1, text="Consultar", bg="deep sky blue",command=self.consultar) #Inicio boton consultar
        self.boton1.grid(column=1, row=18, padx=4, pady=4) #Fin boton consultar

    def consultar(self):
        datos=(self.idpacientevacuna1.get(), )
        respuesta=self.vacunas1.consulta(datos)
        if len(respuesta)>0:
            self.tipovacuna1.set(respuesta[0][0])
            self.fechavacuna1.set(respuesta[0][1])
        else:
            self.tipovacuna.set('')
            self.fechavacuna.set('')
            mb.showinfo("Información", "No existen vacunas con dicho ID del paciente.")

    def listado_completo(self):
        self.pagina3 = ttk.Frame(self.cuadernovacunas1)
        self.cuadernovacunas1.add(self.pagina3, text="Listado de Vacunass")
        self.labelframe1=ttk.LabelFrame(self.pagina3, text="Vacunas")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.boton1=Button(self.labelframe1, text="Listado completo", bg="spring green",command=self.listar) #Inicio boton listar
        self.boton1.grid(column=0, row=0, padx=4, pady=4) #Fin boton listar
        self.scrolledtext1=st.ScrolledText(self.labelframe1, width=70, height=30) #Default width=30, height=10
        self.scrolledtext1.grid(column=0,row=1, padx=10, pady=10) #Default 10x, 10y
    
    def listar(self):
        respuesta=self.vacunas1.recuperar_todos()
        self.scrolledtext1.delete("1.0", tk.END)        
        for fila in respuesta:
            self.scrolledtext1.insert(tk.END, ">Código o ID de paciente: "+str(fila[0])+
                                              "\nTipo de vacuna: "+fila[1]+
                                              "\nFecha aplicación: "+str(fila[2])+"\n\n")
    
    def borrado(self):
        self.pagina4 = ttk.Frame(self.cuadernovacunas1)
        self.cuadernovacunas1.add(self.pagina4, text="Eliminar vacunas")
        self.labelframe1=ttk.LabelFrame(self.pagina4, text="Vacunas")        
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10) #Default: 5x,10y
        self.label1=ttk.Label(self.labelframe1, text="-ID paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=50, pady=100) #Default: 4x,4y
        self.idborra=tk.IntVar()
        self.entryborra=ttk.Entry(self.labelframe1, textvariable=self.idborra)
        self.entryborra.grid(column=1, row=0, padx=50, pady=100) #Default: 4x,4y -Fin IDpaciente

        self.boton1=Button(self.labelframe1, text="Borrar", bg="red",command=self.borrar) #Inicio boton borrar
        self.boton1.grid(column=1, row=1, padx=4, pady=4) #Fin boton borrar
    
    def borrar(self):
        datos=(self.idborra.get(), )
        cantidad=self.vacunas1.baja(datos)
        if cantidad==1:
            mb.showinfo("Información", "Se borró la vacuna con dicho ID.")
        else:
            mb.showinfo("Información", "No existe alguna vacuna con dicho ID.")
    
    def modificar(self):
        self.pagina5 = ttk.Frame(self.cuadernovacunas1)
        self.cuadernovacunas1.add(self.pagina5, text="Modificar vacunas")
        self.labelframe1=ttk.LabelFrame(self.pagina5, text="Vacunas")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe1, text="-ID paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.idmod=tk.StringVar()
        self.entryidmod=ttk.Entry(self.labelframe1, textvariable=self.idmod)
        self.entryidmod.grid(column=1, row=0, padx=4, pady=4) #Fin IDpaciente
        self.label2=ttk.Label(self.labelframe1, text="Tipo de vacuna:") #Inicio tipoV
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.tipovacuna2=tk.StringVar()
        self.entrytipovacuna2=ttk.Entry(self.labelframe1, textvariable=self.tipovacuna2)
        self.entrytipovacuna2.grid(column=1, row=1, padx=4, pady=4) #Default: 4x,4y -Fin tipoV
        self.label3=ttk.Label(self.labelframe1, text="Fecha de aplicación (DD/MM/AA):") #Inicio fechaV
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.fechavacuna2=tk.StringVar()
        self.entryfechavacuna2=ttk.Entry(self.labelframe1, textvariable=self.fechavacuna2) 
        self.entryfechavacuna2.grid(column=1, row=2, padx=4, pady=4) #Default: 4x,4y -Fin fechaV

        self.boton1=Button(self.labelframe1, text="Consultar", bg="deep sky blue",command=self.consultar_mod) #Inicio boton consultar
        self.boton1.grid(column=1, row=6, padx=4, pady=4) #Fin boton consultar
        self.boton1=Button(self.labelframe1, text="Modificar", bg="orange",command=self.modifica) #Inicio boton modificar
        self.boton1.grid(column=1, row=7, padx=4, pady=4) #Fin boton modificar

    def modifica(self):
        if self.idmod.get() == '':
            mb.showinfo("Información", "ID paciente invalido.")
        elif self.tipovacuna2.get() == '':
            mb.showinfo("Información", "Debe añadir un tipo de vacuna.")
        elif self.fechavacuna2.get() == '':
            mb.showinfo("Información", "Debe añadir fecha de aplicación de la vacuna.")
        elif len(self.idmod.get()) > 0 or self.idmod.get() == '':
            datos=(self.idmod.get(), )
            respuesta=self.vacunas1.consultaPac(datos)
            if len(respuesta)>0:
                datos=(self.tipovacuna2.get(),self.fechavacuna2.get(),self.idmod.get(),)
                cantidad=self.vacunas1.modificacion(datos)
                if cantidad==1:
                    mb.showinfo("Información", "Se modificó la vacuna.")
                else:
                    mb.showinfo("Información", "No existe alguna vacuna con dicho ID.")
            else:
                mb.showinfo("Información", "ID paciente invalido.")


    def consultar_mod(self):
        datos=(self.idmod.get(), )
        respuesta=self.vacunas1.consulta(datos)
        if len(respuesta)>0:
            self.tipovacuna2.set(respuesta[0][0])
            self.fechavacuna2.set(respuesta[0][1])
        else:
            self.tipovacuna2.set('')
            self.fechavacuna2.set('')
            mb.showinfo("Información", "No existe alguna vacuna con dicho ID.")

    def regresar(self):
        self.ventanavacunas.destroy()
        aplicacion1=Formulario() #Llama a la clase principal 

#-----------------------------------------------------------------------------------------

class Problemas_cronicos:
    def abrir(self):
        conexion6 = psycopg2.connect(database="proyecto", user="postgres", password='yourpassw')
        return conexion6

    def alta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="insert into problemas_cronicos (IDpaciente, problemas_cronicos) values (%s,%s)"
        cursor.execute(sql, datos)
        cone.commit()

    def consulta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select problemas_cronicos from problemas_cronicos where IDpaciente=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()
    
    def consultaPac(self,datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select nombre from paciente where IDpaciente=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()
            
    def recuperar_todos(self):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select IDpaciente, problemas_cronicos from problemas_cronicos"
        cursor.execute(sql)
        sql2 = "select * from problemas_cronicos order by IDpaciente"
        cursor.execute(sql2)
        return cursor.fetchall()
    
    def baja(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="delete from problemas_cronicos where IDpaciente=%s"
        cursor.execute(sql, datos)
        cone.commit()
        return cursor.rowcount # retornamos la cantidad de filas borradas
            
    def modificacion(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="update problemas_cronicos set problemas_cronicos=%s where IDpaciente=%s"
        cursor.execute(sql, datos)
        cone.commit()
        return cursor.rowcount # retornamos la cantidad de filas modificadas

class FormularioProblemas_cronicos:
    def __init__(self):
        mb.showinfo("Información sobre problemas crónicos", "-Los problemas crónicos del paciente se agregan mediante su ID.")
        self.problemas_cronicos1=Problemas_cronicos() #Se llama a la clase declarada
        self.ventanaproblemas_cronicos=tk.Tk()  #Se crea una ventana 
        self.ventanaproblemas_cronicos.config(bg="dodger blue")
        self.ventanaproblemas_cronicos.title("Clinica Odontologica")  #Titulo de la ventana
        self.cuadernoproblemas_cronicos1 = ttk.Notebook(self.ventanaproblemas_cronicos)   #Se crea un cuaderno en la ventana 
        self.carga_Problemas_cronicos()  #Metodos base
        self.consulta_por_codigo()
        self.listado_completo()
        self.borrado()
        self.modificar()
        style = ttk.Style()
        style.theme_use("classic")
        style.configure("TNotebook.Tab", background="green", font="helvetica 10")
        self.cuadernoproblemas_cronicos1.grid(column=0, row=0, padx=60, pady=10) #Default 10x, 10y dimension del cuaderno
        self.ventanaproblemas_cronicos.mainloop() #Ejecuta la ventana principal 
                
            
    def carga_Problemas_cronicos(self):
        self.paginaproblemas_cronicos1 = ttk.Frame(self.cuadernoproblemas_cronicos1)
        self.cuadernoproblemas_cronicos1.add(self.paginaproblemas_cronicos1, text="Agregar problemas")
        self.labelframe1=ttk.LabelFrame(self.paginaproblemas_cronicos1, text="Problemas cronicos")        
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10) #Default 5x, 10y
        self.label1=ttk.Label(self.labelframe1, text="-ID de paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=4, pady=4) #Default 4x, 4y
        self.idpacienteprob=tk.StringVar()
        self.entryidpacienteprob=ttk.Entry(self.labelframe1, textvariable=self.idpacienteprob) 
        self.entryidpacienteprob.grid(column=1, row=0, padx=4, pady=4) #Default 4x, 4y -Fin IDpaciente
        self.label2=ttk.Label(self.labelframe1, text="Problemas cronicos del paciente:") #Inicio problemasCro
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.problemas=tk.StringVar()
        self.entryproblemas=ttk.Entry(self.labelframe1, textvariable=self.problemas)
        self.entryproblemas.grid(column=1, row=1, padx=4, pady=4) #Default 4x, 4y -Fin problemasCro

        self.botonproblemas_cronicos1=Button(self.labelframe1, text="Confirmar", bg="red",command=self.agregarProblemas_cronicos) #Inicio boton agregarProblemas_cronicos
        self.botonproblemas_cronicos1.grid(column=1, row=8, padx=4, pady=4) #Default 4x, 4y -Fin boton
        self.botonProblemas_cronicos2=Button(self.labelframe1, text="----> Regresar ",bg="deep sky blue", command=self.regresar) #Inicio boton agregarProblemas_cronicos
        self.botonProblemas_cronicos2.grid(column=4, row=9, padx=4, pady=4) #Default 4x, 4y -Fin boton
            
    def agregarProblemas_cronicos(self):
        if self.idpacienteprob.get() == '':
            mb.showinfo("Información", "ID paciente invalido.")
        elif self.problemas.get() == '':
            mb.showinfo("Información", "Falta añadir los problemas cronicos.")
        elif len(self.idpacienteprob.get()) > 0 or self.idpacienteprob.get() == '':
            datos=(self.idpacienteprob.get(), )
            respuesta=self.problemas_cronicos1.consultaPac(datos)
            if len(respuesta)>0:
                datos=(self.idpacienteprob.get(), self.problemas.get(),)              
                self.problemas_cronicos1.alta(datos)
                mb.showinfo("Información", "Los datos fueron cargados con exito.")
                self.idpacienteprob.set("")
                self.problemas.set("")
            else:
                mb.showinfo("Información", "ID paciente invalido.")
    
    def consulta_por_codigo(self):
        self.pagina2 = ttk.Frame(self.cuadernoproblemas_cronicos1)
        self.cuadernoproblemas_cronicos1.add(self.pagina2, text="Consulta de problemas")
        self.labelframe1=ttk.LabelFrame(self.pagina2, text="Problemas cronicos")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe1, text="-ID paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.idpacienteprob1=tk.StringVar()
        self.entryidpacienteprob1=ttk.Entry(self.labelframe1, textvariable=self.idpacienteprob1) 
        self.entryidpacienteprob1.grid(column=1, row=0, padx=4, pady=4)  #Fin IDpaciente
        self.label2=ttk.Label(self.labelframe1, text="Problemas crónicos:") #Inicio problemasCro
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.problemas1=tk.StringVar()
        self.entryproblemas1=ttk.Entry(self.labelframe1, textvariable=self.problemas1, state="readonly" )
        self.entryproblemas1.grid(column=1, row=1, padx=4, pady=4) #Default: 4x,4y -Fin problemasCro

        self.boton1=Button(self.labelframe1, text="Consultar",bg="deep sky blue", command=self.consultar) #Inicio boton consultar
        self.boton1.grid(column=1, row=18, padx=4, pady=4) #Fin boton consultar

    def consultar(self):
        datos=(self.idpacienteprob1.get(), )
        respuesta=self.problemas_cronicos1.consulta(datos)
        if len(respuesta)>0:
            self.problemas1.set(respuesta[0][0])
        else:
            self.problemas.set('')
            mb.showinfo("Información", "No existe algun problema crónico con dicho ID paciente.")

    def listado_completo(self):
        self.pagina3 = ttk.Frame(self.cuadernoproblemas_cronicos1)
        self.cuadernoproblemas_cronicos1.add(self.pagina3, text="Listado de P-C")
        self.labelframe1=ttk.LabelFrame(self.pagina3, text="Problemas cronicos")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.boton1=Button(self.labelframe1, text="Listado completo", bg="spring green",command=self.listar) #Inicio boton listar
        self.boton1.grid(column=0, row=0, padx=4, pady=4) #Fin boton listar
        self.scrolledtext1=st.ScrolledText(self.labelframe1, width=70, height=30) #Default width=30, height=10
        self.scrolledtext1.grid(column=0,row=1, padx=10, pady=10) #Default 10x, 10y
    
    def listar(self):
        respuesta=self.problemas_cronicos1.recuperar_todos()
        self.scrolledtext1.delete("1.0", tk.END)        
        for fila in respuesta:
            self.scrolledtext1.insert(tk.END, ">Código o ID del paciente: "+str(fila[0])+
                                              "\nProblemas crónicos: "+fila[1]+"\n\n")
    
    def borrado(self):
        self.pagina4 = ttk.Frame(self.cuadernoproblemas_cronicos1)
        self.cuadernoproblemas_cronicos1.add(self.pagina4, text="Eliminar P-C")
        self.labelframe1=ttk.LabelFrame(self.pagina4, text="Problemas crónicos")        
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10) #Default: 5x,10y
        self.label1=ttk.Label(self.labelframe1, text="-ID paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=50, pady=100) #Default: 4x,4y
        self.idborra=tk.IntVar()
        self.entryborra=ttk.Entry(self.labelframe1, textvariable=self.idborra)
        self.entryborra.grid(column=1, row=0, padx=50, pady=107) #Default: 4x,4y -Fin IDpaciente

        self.boton1=Button(self.labelframe1, text="Borrar", bg="red",command=self.borrar) #Inicio boton borrar
        self.boton1.grid(column=1, row=2, padx=4, pady=4) #Fin boton borrar
    
    def borrar(self):
        datos=(self.idborra.get(), )
        cantidad=self.problemas_cronicos1.baja(datos)
        if cantidad==1:
            mb.showinfo("Información", "Se borró el problema crónico con dicho ID.")
        else:
            mb.showinfo("Información", "No existe algun problema crónico con dicho ID.")
    
    def modificar(self):
        self.pagina5 = ttk.Frame(self.cuadernoproblemas_cronicos1)
        self.cuadernoproblemas_cronicos1.add(self.pagina5, text="Modificar problemas")
        self.labelframe1=ttk.LabelFrame(self.pagina5, text="Problemas crónicos")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe1, text="-ID paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.idmod=tk.StringVar()
        self.entryidmod=ttk.Entry(self.labelframe1, textvariable=self.idmod)
        self.entryidmod.grid(column=1, row=0, padx=4, pady=4) #Fin IDpaciente
        self.label2=ttk.Label(self.labelframe1, text="Problemas crónicos del paciente:") #Inicio problemasCro
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.problemasmod=tk.StringVar()
        self.entryproblemasmod=ttk.Entry(self.labelframe1, textvariable=self.problemasmod)
        self.entryproblemasmod.grid(column=1, row=1, padx=4, pady=4) #Default: 4x,4y -Fin problemasCro

        self.boton1=Button(self.labelframe1, text="Consultar", bg="deep sky blue",command=self.consultar_mod) #Inicio boton consultar
        self.boton1.grid(column=1, row=6, padx=4, pady=4) #Fin boton consultar
        self.boton1=Button(self.labelframe1, text="Modificar", bg="orange",command=self.modifica) #Inicio boton modificar
        self.boton1.grid(column=1, row=7, padx=4, pady=4) #Fin boton modificar

    def modifica(self):
        if self.idmod.get() == '':
            mb.showinfo("Información", "ID paciente invalido.")
        elif self.problemasmod.get() == '':
            mb.showinfo("Información", "Falta añadir los problemas cronicos.")
        elif len(self.idmod.get()) > 0 or self.idmod.get() == '':
            datos=(self.idmod.get(), )
            respuesta=self.problemas_cronicos1.consultaPac(datos)
            if len(respuesta)>0:
                datos=(self.problemasmod.get(),self.idmod.get())
                cantidad=self.problemas_cronicos1.modificacion(datos)
                if cantidad==1:
                    mb.showinfo("Información", "Se modificó los problemas crónicos.")
                else:
                    mb.showinfo("Información", "No existe algun problema crónico con dicho ID.")
            else:
                mb.showinfo("Información", "ID paciente invalido.")


    def consultar_mod(self):
        datos=(self.idmod.get(), )
        respuesta=self.problemas_cronicos1.consulta(datos)
        if len(respuesta)>0:
            self.problemasmod.set(respuesta[0][0])
        else:
            self.problemasmod.set('')
            mb.showinfo("Información", "No existe algun problema crónico con dicho ID.")

    def regresar(self):
        self.ventanaproblemas_cronicos.destroy()
        aplicacion1=Formulario() #Llama a la clase principal 

#-------------------------------------------------------------------------------------------

class Alergias:
    def abrir(self):
        conexion7 = psycopg2.connect(database="proyecto", user="postgres", password='yourpassw')
        return conexion7

    def alta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="insert into alergias (IDpaciente, alergias) values (%s,%s)"
        cursor.execute(sql, datos)
        cone.commit()
        

    def consulta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select alergias from alergias where IDpaciente=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()
    
    def consultaPac(self,datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select nombre from paciente where IDpaciente=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()
            
    def recuperar_todos(self):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select IDpaciente, alergias from alergias"
        cursor.execute(sql)
        sql2 = "select * from alergias order by IDpaciente"
        cursor.execute(sql2)
        return cursor.fetchall()
    
    def baja(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="delete from alergias where IDpaciente=%s"
        cursor.execute(sql, datos)
        cone.commit()
        return cursor.rowcount # retornamos la cantidad de filas borradas
            
    def modificacion(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="update alergias set alergias=%s where IDpaciente=%s"
        cursor.execute(sql, datos)
        cone.commit()
        return cursor.rowcount # retornamos la cantidad de filas modificadas

class FormularioAlergias:
    def __init__(self):
        mb.showinfo("Información sobre alergias", "-Las alergias del paciente se agregan mediante su ID.")
        self.alergias1=Alergias() #Se llama a la clase declarada
        self.ventanaalergias=tk.Tk()  #Se crea una ventana 
        self.ventanaalergias.config(bg="dodger blue")
        self.ventanaalergias.title("Clinica Odontologica")  #Titulo de la ventana
        self.cuadernoalergias1 = ttk.Notebook(self.ventanaalergias)   #Se crea un cuaderno en la ventana 
        self.carga_Alergias()  #Metodos base
        self.consulta_por_codigo()
        self.listado_completo()
        self.borrado()
        self.modificar()
        style = ttk.Style()
        style.theme_use("classic")
        style.configure("TNotebook.Tab", background="green", font="helvetica 10")
        self.cuadernoalergias1.grid(column=0, row=0, padx=60, pady=10) #Default 10x, 10y dimension del cuaderno
        self.ventanaalergias.mainloop() #Ejecuta la ventana principal 
        
                
            
    def carga_Alergias(self):
        self.paginaalergias1 = ttk.Frame(self.cuadernoalergias1)
        self.cuadernoalergias1.add(self.paginaalergias1, text="Agregar alergias")
        self.labelframe1=ttk.LabelFrame(self.paginaalergias1, text="Alergias")        
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10) #Default 5x, 10y
        self.label1=ttk.Label(self.labelframe1, text="-ID de paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=4, pady=4) #Default 4x, 4y
        self.idpacientealerg=tk.StringVar()
        self.entryidpacientealerg=ttk.Entry(self.labelframe1, textvariable=self.idpacientealerg) 
        self.entryidpacientealerg.grid(column=1, row=0, padx=4, pady=4) #Default 4x, 4y -Fin IDpaciente
        self.label2=ttk.Label(self.labelframe1, text="Alergias:") #Inicio alergias
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.alergia=tk.StringVar()
        self.entryalergia=ttk.Entry(self.labelframe1, textvariable=self.alergia)
        self.entryalergia.grid(column=1, row=1, padx=4, pady=4) #Default 4x, 4y -Fin alergias

        self.botonalergias1=Button(self.labelframe1, text="Confirmar", bg="red",command=self.agregarAlergias) #Inicio boton agregarAlergias
        self.botonalergias1.grid(column=1, row=8, padx=4, pady=4) #Default 4x, 4y -Fin boton
        self.botonAlergias2=Button(self.labelframe1, text="----> Regresar ", bg="deep sky blue",command=self.regresar) #Inicio boton agregarAlergias
        self.botonAlergias2.grid(column=4, row=9, padx=4, pady=4) #Default 4x, 4y -Fin boton
        
            
    def agregarAlergias(self):
        if self.idpacientealerg.get() == '':
            mb.showinfo("Información", "ID paciente invalido.")
        elif self.alergia.get() == '':
            mb.showinfo("Información", "Falta añadir las alergias.")
        elif len(self.idpacientealerg.get()) > 0 or self.idpacientealerg.get() == '':
            datos=(self.idpacientealerg.get(), )
            respuesta=self.alergias1.consultaPac(datos)
            if len(respuesta)>0:
                datos=(self.idpacientealerg.get(), self.alergia.get())              
                self.alergias1.alta(datos)
                mb.showinfo("Información", "Los datos fueron cargados con exito.")
                self.idpacientealerg.set("")
                self.alergia.set("")
            else:
                mb.showinfo("Información", "ID paciente invalido.")

    
    def consulta_por_codigo(self):
        self.pagina2 = ttk.Frame(self.cuadernoalergias1)
        self.cuadernoalergias1.add(self.pagina2, text="Consulta alergias")
        self.labelframe1=ttk.LabelFrame(self.pagina2, text="Alergias")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe1, text="-ID paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.idpacientealerg1=tk.StringVar()
        self.entryidpacientealerg1=ttk.Entry(self.labelframe1, textvariable=self.idpacientealerg1) 
        self.entryidpacientealerg1.grid(column=1, row=0, padx=4, pady=4)  #Fin IDpaciente
        self.label2=ttk.Label(self.labelframe1, text="Alergias:") #Inicio alergias
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.alergia1=tk.StringVar()
        self.entryalergia1=ttk.Entry(self.labelframe1, textvariable=self.alergia1, state="readonly")
        self.entryalergia1.grid(column=1, row=1, padx=4, pady=4) #Default: 4x,4y -Fin alergias
        self.boton1=Button(self.labelframe1, text="Consultar",bg="deep sky blue", command=self.consultar) #Inicio boton consultar
        self.boton1.grid(column=1, row=18, padx=4, pady=4) #Fin boton consultar

    def consultar(self):
        datos=(self.idpacientealerg1.get(), )
        respuesta=self.alergias1.consulta(datos)
        if len(respuesta)>0:
            self.alergia1.set(respuesta[0][0])
        else:
            self.alergia.set('')
            mb.showinfo("Información", "No existe algun alergia con dicho ID paciente.")

    def listado_completo(self):
        self.pagina3 = ttk.Frame(self.cuadernoalergias1)
        self.cuadernoalergias1.add(self.pagina3, text="Listado de alergias")
        self.labelframe1=ttk.LabelFrame(self.pagina3, text="Alergias")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.boton1=Button(self.labelframe1, text="Listado completo",bg="spring green", command=self.listar) #Inicio boton listar
        self.boton1.grid(column=0, row=0, padx=4, pady=4) #Fin boton listar
        self.scrolledtext1=st.ScrolledText(self.labelframe1, width=70, height=30) #Default width=30, height=10
        self.scrolledtext1.grid(column=0,row=1, padx=10, pady=10) #Default 10x, 10y
    
    def listar(self):
        respuesta=self.alergias1.recuperar_todos()
        self.scrolledtext1.delete("1.0", tk.END)        
        for fila in respuesta:
            self.scrolledtext1.insert(tk.END, ">Código o ID: "+str(fila[0])+
                                              "\nAlergias: "+fila[1]+"\n\n")
    
    def borrado(self):
        self.pagina4 = ttk.Frame(self.cuadernoalergias1)
        self.cuadernoalergias1.add(self.pagina4, text="Eliminar alergias")
        self.labelframe1=ttk.LabelFrame(self.pagina4, text="Alergias")        
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10) #Default: 5x,10y
        self.label1=ttk.Label(self.labelframe1, text="-ID paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=50, pady=100) #Default: 4x,4y
        self.idborra=tk.IntVar()
        self.entryborra=ttk.Entry(self.labelframe1, textvariable=self.idborra)
        self.entryborra.grid(column=1, row=0, padx=50, pady=107) #Default: 4x,4y -Fin IDpaciente

        self.boton1=Button(self.labelframe1, text="Borrar", bg="red",command=self.borrar) #Inicio boton borrar
        self.boton1.grid(column=1, row=2, padx=4, pady=4) #Fin boton borrar
    
    def borrar(self):
        datos=(self.idborra.get(), )
        cantidad=self.alergias1.baja(datos)
        if cantidad==1:
            mb.showinfo("Información", "Se borró la alergia con dicho ID.")
        else:
            mb.showinfo("Información", "No existe alguna alergia con dicho ID de paciente.")
    
    def modificar(self):
        self.pagina5 = ttk.Frame(self.cuadernoalergias1)
        self.cuadernoalergias1.add(self.pagina5, text="Modificar alergias")
        self.labelframe1=ttk.LabelFrame(self.pagina5, text="Alergias")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe1, text="-ID paciente:") #Inicio IDpaciente
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.idmod=tk.StringVar()
        self.entryidmod=ttk.Entry(self.labelframe1, textvariable=self.idmod)
        self.entryidmod.grid(column=1, row=0, padx=4, pady=4) #Fin IDpaciente
        self.label2=ttk.Label(self.labelframe1, text="Alergia:") #Inicio alergia
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.alergiamod=tk.StringVar()
        self.entryalergiamod=ttk.Entry(self.labelframe1, textvariable=self.alergiamod)
        self.entryalergiamod.grid(column=1, row=1, padx=4, pady=4) #Default: 4x,4y -Fin alergia
        self.boton1=Button(self.labelframe1, text="Consultar", bg="deep sky blue",command=self.consultar_mod) #Inicio boton consultar
        self.boton1.grid(column=1, row=6, padx=4, pady=4) #Fin boton consultar
        self.boton1=Button(self.labelframe1, text="Modificar", bg="orange",command=self.modifica) #Inicio boton modificar
        self.boton1.grid(column=1, row=7, padx=4, pady=4) #Fin boton modificar

    def modifica(self):
        if self.idmod.get() == '':
            mb.showinfo("Información", "ID paciente invalido.")
        elif self.alergiamod.get() == '':
            mb.showinfo("Información", "Falta añadir las alergias.")
        elif len(self.idmod.get()) > 0 or self.idmod.get() == '':
            datos=(self.idmod.get(), )
            respuesta=self.alergias1.consultaPac(datos)
            if len(respuesta)>0:
                datos=(self.alergiamod.get(),self.idmod.get(),)
                cantidad=self.alergias1.modificacion(datos)
                if cantidad==1:
                    mb.showinfo("Información", "Se modificó la alergia.")
                else:
                    mb.showinfo("Información", "No existe alguna alergia con dicho ID de paciente.")
            else:
                mb.showinfo("Información", "ID paciente invalido.")

    def consultar_mod(self):
        datos=(self.idmod.get(), )
        respuesta=self.alergias1.consulta(datos)
        if len(respuesta)>0:
            self.alergiamod.set(respuesta[0][0])
        else:
            self.alergiamod.set('')
            mb.showinfo("Información", "No existe alguna alergia con dicho ID de paciente.")

    def regresar(self):
        self.ventanaalergias.destroy()
        aplicacion1=Formulario() #Llama a la clase principal 

#-------------------------------------------------------------------------------------------
         
def mainP():
    aplicacion1=Formulario() #Llama a la clase principal 
   

class Registro_datos():

    def __init__(self):
        self.conexion = psycopg2.connect(database="proyecto", user="postgres", password='yourpassw')
        
    def busca_users(self, users):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM login_datos WHERE usuario = {}".format(users)
        cur.execute(sql)
        usersx = cur.fetchall()
        cur.close()
        return usersx

    def busca_password(self, password):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM login_datos WHERE pass = {}".format(password) #
        cur.execute(sql)
        passwordx = cur.fetchall()
        cur.close()
        return passwordx


class Login(Frame):
	def __init__(self, master, *args):
		super().__init__( master,*args)
		self.user_marcar = "Ingrese su usuario"
		self.contra_marcar = "Ingrese su contraseña"
		self.fila1  = ''
		self.fila2 = ''
		self.datos = Registro_datos()
		self.widgets()
	def entry_out(self, event, event_text):
		if event['fg'] == 'black' and len(event.get()) ==0:
			event.delete(0, END)
			event['fg'] = 'grey'
			event.insert(0, event_text)
		if self.entry2.get() != 'Ingrese su contraseña':
			self.entry2['show'] =""
		if self.entry2.get() != 'Ingrese su correo':
			self.entry2['show'] ="*"
	def entry_in(self, event):
	    if event['fg'] == 'grey':
	        event['fg'] = 'black'
	        event.delete(0, END)

	    if self.entry2.get() != 'Ingrese su contraseña':
	    	self.entry2['show'] = "*"

	    if self.entry2.get() == 'Ingrese su contraseña':
	    	self.entry2['show'] = ""

	def salir(self):
		self.master.destroy()
		self.master.quit()

	def acceder_ventana_dos(self):
         for i in  range(101):
            self.barra['value'] +=1
            self.master.update()
            time.sleep(0.02)	
         
         self.master.destroy()
         aplicacion1=Formulario() #Llama a la clase principal
		 
          
		
	def verificacion_users(self):
		self.indica1['text'] = ''
		self.indica2['text'] = ''
		users_entry = self.entry1.get()
		password_entry = self.entry2.get()

		if users_entry!= self.user_marcar or self.contra_marcar != password_entry:
			users_entry = str("'" + users_entry + "'")
			password_entry = str("'" + password_entry + "'")

			dato1 = self.datos.busca_users(users_entry)
			dato2 = self.datos.busca_password(password_entry)

			self.fila1 = dato1
			self.fila2 = dato2

			if self.fila1 == self.fila2:
				if dato1 == [] and dato2 ==[]:
					self.indica2['text'] = 'Contraseña incorrecta'
					self.indica1['text'] = 'Usuario incorrecto'
				else:

					if dato1 ==[]:
						self.indica1['text'] = 'Usuario incorrecto'
					else:
						dato1 = dato1[0][1]

					if dato2 ==[]:
						self.indica2['text'] = 'Contraseña incorrecta'
					else:
						dato2 = dato2[0][2]

					if dato1 != [] and dato2 != []:
						self.acceder_ventana_dos()
			else:
				self.indica1['text'] = 'Usuario incorrecto'
				self.indica2['text'] = 'Contraseña incorrecta'

	def widgets(self):
		self.logo = PhotoImage(file ='odont.png')
		Label(self.master, image= self.logo, bg='DarkOrchid1',height=150, width=150).pack()
		Label(self.master, text= 'Usuario', bg='DarkOrchid1', fg= 'black', font= ('Lucida Sans', 16, 'bold')).pack(pady=5)
		self.entry1 = Entry(self.master, font=('Comic Sans MS', 12),justify = 'center', fg='grey',highlightbackground = "#E65561",
			highlightcolor= "green2", highlightthickness=5)
		self.entry1.insert(0, self.user_marcar)
		self.entry1.bind("<FocusIn>", lambda args: self.entry_in(self.entry1))
		self.entry1.bind("<FocusOut>", lambda args: self.entry_out(self.entry1, self.user_marcar))
		self.entry1.pack(pady=4)

		self.indica1 = Label(self.master, bg='DarkOrchid1', fg= 'black', font= ('Arial', 8, 'bold'))
		self.indica1.pack(pady=2)

		# contraseña y entry
		Label(self.master, text= 'Contraseña', bg='DarkOrchid1', fg= 'black', font= ('Lucida Sans', 16, 'bold')).pack(pady=5)
		self.entry2 = Entry(self.master,font=('Comic Sans MS', 12),justify = 'center',  fg='grey',highlightbackground = "#E65561",
			highlightcolor= "green2", highlightthickness=5)
		self.entry2.insert(0, self.contra_marcar)
		self.entry2.bind("<FocusIn>", lambda args: self.entry_in(self.entry2))
		self.entry2.bind("<FocusOut>", lambda args: self.entry_out(self.entry2, self.contra_marcar))
		self.entry2.pack(pady=4)
		self.indica2 = Label(self.master, bg='DarkOrchid1', fg= 'black', font= ('Arial', 8, 'bold'))
		self.indica2.pack(pady=2)
		Button(self.master, text= 'Iniciar Sesion',  command = self.verificacion_users,activebackground='magenta', bg='#D64E40', font=('Arial', 12,'bold')).pack(pady=10)
		estilo = ttk.Style()
		estilo.theme_use('clam')
		estilo.configure("TProgressbar", foreground='red', background='black',troughcolor='DarkOrchid1',
																bordercolor='#970BD9',lightcolor='#970BD9', darkcolor='black')
		self.barra = ttk.Progressbar(self.master, orient= HORIZONTAL, length=200, mode='determinate', maximum=100, style="TProgressbar")
		self.barra.pack()
		Button(self.master, text= 'Salir', bg='DarkOrchid1',activebackground='DarkOrchid1', bd=0, fg = 'black', font=('Lucida Sans', 15,'italic'),command= self.salir).pack(pady=10)

if __name__ == "__main__":
	ventana = Tk()
	ventana.config(bg='DarkOrchid')
	ventana.geometry('350x500+500+50')
	ventana.overrideredirect(1)
	ventana.resizable(0,0)
	app = Login(ventana)
	app.mainloop()
    
#---------------------------------------------------------------------------------------



    


   





