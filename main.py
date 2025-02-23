import pandas as pd
import matplotlib.pyplot as mat
import tkinter as tk
import os,shutil,time,datetime
from tkinter import filedialog


class App: 
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.geometry("1200x600")
        self.root.config(background="gray")
        self.root.resizable(False,False)
        self.root.columnconfigure(0, weight=2)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(1, weight=1)


    def PrincipalLayout(self): 
            #configuracion del layout
            self.frame_1: tk.Label = tk.Frame(self.root,background="lightblue",width=1200,height=90)
            self.frame_1.grid(row=0, column=0, columnspan=3,sticky="NSEW")

            self.frame_2: tk.Label = tk.Frame(self.root, background="white",width=400)
            self.frame_2.grid(row=1, column=0, sticky="NSEW")

            self.frame_3: tk.Label = tk.Frame(self.root, background="lightgreen",width=400)
            self.frame_3.grid(row=1, column=1, sticky="NSEW")

            self.frame_4: tk.Label = tk.Frame(self.root, background="lightpink",width=400)
            self.frame_4.grid(row=1, column=2, sticky="NSEW")


            self.frame_1.columnconfigure(0, weight=2)
            self.frame_2.columnconfigure(0, weight=1)  
            self.frame_3.columnconfigure(0, weight=1)

            self.frame_1.rowconfigure(0, weight=2)
            self.frame_2.rowconfigure(0, weight=1) 
            self.frame_3.rowconfigure(0, weight=1)
            self.Layout_Content()


    def Layout_Content(self):
            #header
            self.title: tk.Label = tk.Label(self.frame_1,text="Analizador De Ventas",font="consola 16 bold",foreground="white",background="lightblue")
            self.title.grid(row=0,column=0)

            #aside izquierdo 
            self.info: tk.Label = tk.Label(self.frame_2,text="Seleccione Un Csv De Su Dispositivo",font="consola 12 bold",background="white",foreground="lightgray")
            self.info.place(x=37,y=17)

            self.seleccionar: tk.Button = tk.Button(self.frame_2,text="Seleccionar",background="lightgray",foreground="white",font="consola 13 bold",relief="raised",command=self.Agg_Logic)
            self.seleccionar.place(x=140,y=87)

            self.Eliminar: tk.Button = tk.Button(self.frame_2,text="Eliminar",background="lightgray",foreground="white",font="consola 13 bold",relief="raised",command=self.delete_content)
            self.Eliminar.place(x=155,y=177)

            self.title_frame_3: tk.Label = tk.Label(self.frame_4,text="Configuracion Matplotlib",font="consola 15 bold",foreground="white",background="lightpink")
            self.title_frame_3.place(x=10 , y=10)


    def Agg_Logic(self):
        self.seleccionar.config(state="disabled")
        try: 

            self.file_path: shutil = filedialog.askopenfilename(
                filetypes=[("CSV files", "*.csv")],  
                title="Select a CSV file") 
            self.ORIGIN_PATH: str = f"{os.getcwd()}/03-AnalisisVentas/csv"

            if os.path.exists(self.ORIGIN_PATH):
                shutil.copy(self.file_path,self.ORIGIN_PATH)
            else:
                os.mkdir(self.ORIGIN_PATH)
                shutil.copy(self.file_path,self.ORIGIN_PATH)

            self.info_csv: tk.Label = tk.Label(self.frame_2,text="El csv ha sido importado correctamente",background="white",foreground="black",font="consola 11 bold")
            self.info_csv.place(x=7,y=550)
            self.manipulation_csv()

        except shutil.Error: 
            self.info_csv: tk.Label = tk.Label(self.frame_2,text="El archivo de destino no existe!",background="white",foreground="black",font="consola 11 bold")
            self.info_csv.place(x=7,y=550)
            time.sleep(3)
            self.info_csv.config(text=" ")
            

        except FileNotFoundError:
            self.info_csv: tk.Label = tk.Label(self.frame_2,text="El archivo no se encuentra!",background="white",foreground="black",font="consola 11 bold")
            self.info_csv.place(x=7,y=550)
            time.sleep(3)
            self.info_csv.config(text=" ")

        except FileExistsError: 
            self.info_csv: tk.Label = tk.Label(self.frame_2,text="El archivo no existe!",background="white",foreground="black",font="consola 11 bold")
            self.info_csv.place(x=7,y=550)
            time.sleep(3)
            self.info_csv.config(text=" ")

        except pd.errors.EmptyDataError:
            self.info_csv: tk.Label = tk.Label(self.frame_2,text="El csv esta vacio!",background="white",foreground="black",font="consola 11 bold")
            self.info_csv.place(x=7,y=550)
            time.sleep(3)
            self.info_csv.config(text=" ")

    def delete_content(self): 
        try: 
            shutil.rmtree(self.ORIGIN_PATH)
            for widget in self.frame_3.winfo_children():
                widget.destroy()
            self.seleccionar.config(state="active")
            self.info_csv.config(text=" ")
            self.entry_axes_x.config(state="normal")
            self.entry_axes_y.config(state="normal")
            self.lista_axes_x.clear()
            self.lista_axes_y.clear()
        except FileNotFoundError:
            self.info_csv.config(text="El archivo ya ha sido eliminado!")

    def manipulation_csv(self):
            self.read_csv: pd = pd.read_csv(self.file_path)

            timestamp: os = os.path.getmtime(self.file_path)
            fecha_modificacion: datetime = datetime.datetime.fromtimestamp(timestamp)

            #previsualizacion del csv con su nombre de archivo , Nfilas , Ncolumnas , headersrow y headerscolumns
            self.title_csv_1: tk.Label = tk.Label(self.frame_3,text=f"Nombre: {os.path.basename(self.file_path)}",background="lightgreen",foreground="black",font="consola 11 bold" )
            self.title_csv_1.place(x=7,y=10)

            self.title_csv_2: tk.Label = tk.Label(self.frame_3,text=f"Nfilas: {self.read_csv.shape[0]}",background="lightgreen",foreground="black",font="consola 11 bold" )
            self.title_csv_2.place(x=7,y=30)

            self.title_csv_3: tk.Label = tk.Label(self.frame_3,text=f"NColumnas: {self.read_csv.shape[1]}",background="lightgreen",foreground="black",font="consola 11 bold" )
            self.title_csv_3.place(x=7,y=50)

            self.title_csv_4: tk.Label = tk.Label(self.frame_3,text=f"Tamaño Del Archivo: {os.path.getsize(self.file_path)} bytes",background="lightgreen",foreground="black",font="consola 11 bold" )
            self.title_csv_4.place(x=7,y=70)

            self.title_csv_5: tk.Label = tk.Label(self.frame_3,text=f"Ultima Modificacion: {fecha_modificacion}",background="lightgreen",foreground="black",font="consola 11 bold" )
            self.title_csv_5.place(x=7,y=90)

            self.columns: tk.Label= tk.Label(self.frame_3,text="Nombres de las columnas: ",font="consola 13 bold",background="lightgreen",foreground="white")
            self.columns.place(x=7,y=150)

            self.counter_columns: pd = self.read_csv.columns
            COORX = 170
            for i in self.counter_columns: 
                self.info_columns: tk.Label = tk.Label(self.frame_3,text=i,background="lightgreen",foreground="black",font="consola 11 bold")
                self.info_columns.place(x=7,y=COORX)
                COORX+=20

            COORX+=15
            self.info_integer_or_string: tk.Label = tk.Label(self.frame_3,text="Celdas las cuales son integers para operar: ",foreground="white",background="lightgreen",font="consola 13 bold")
            self.info_integer_or_string.place(x=7, y=COORX)

            for j in self.read_csv:
                 for index , value in enumerate(self.read_csv[f"{j}"]):
                      if isinstance(value,(int,float)):
                        COORX+=20
                        self.label_integer_or_string: tk.Label = tk.Label(self.frame_3,text=j,font="consola 11 bold",background="lightgreen",foreground="black")
                        self.label_integer_or_string.place(x=7,y=COORX)
                        break
                      else:
                        break
            
            warning: tk.Label = tk.Label(self.frame_2,text="!importante la app se suceptible a mayusculas \n y minusculas",font="consola 11 bold",foreground="black",background="white")
            warning.place(x=7, y=500)

            self.Frame_4_Matplotlib()

    def Frame_4_Matplotlib(self):
         constx: int = 90

         self.label_axes_X: tk.Label = tk.Label(self.frame_4,text=" - Nombre del eje x de la grafica: ",font="consola 12 bold",foreground="black",background="lightpink")
         self.label_axes_X.place(x=35,y=50)

         self.entry_axes_x: tk.Entry = tk.Entry(self.frame_4,bd=6,foreground="black",font="consola 10 bold",justify="center",relief="raised")
         self.entry_axes_x.place(x=constx,y=90)

         self.label_axes_y: tk.Label = tk.Label(self.frame_4,text=" - Nombre del eje y de la grafica: ",font="consola 12 bold",foreground="black",background="lightpink")
         self.label_axes_y.place(x=35,y=130)

         self.entry_axes_y: tk.Entry = tk.Entry(self.frame_4,bd=6,foreground="black",font="consola 10 bold",justify="center",relief="raised")
         self.entry_axes_y.place(x=constx,y=170)

         self.variables_axes_x: tk.Label = tk.Label(self.frame_4,text=" - Nombre de la Celda del csv para el \n eje x: ",font="consola 12 bold",foreground="black",background="lightpink")
         self.variables_axes_x.place(x=35,y=220)

         self.entry_variables_axes_x: tk.Entry = tk.Entry(self.frame_4,bd=6,foreground="black",font="consola 10 bold",justify="center",relief="raised")
         self.entry_variables_axes_x.place(x=constx,y=270)

         self.variables_axes_y: tk.Label = tk.Label(self.frame_4,text=" - Nombre de la Celda del csv para el \n eje y: ",font="consola 12 bold",foreground="black",background="lightpink")
         self.variables_axes_y.place(x=35,y=310)

         self.entry_variables_axes_y: tk.Entry = tk.Entry(self.frame_4,bd=6,foreground="black",font="consola 10 bold",justify="center",relief="raised")
         self.entry_variables_axes_y.place(x=constx,y=360)
         
         self.Agg_datos_frame_4 = tk.Button(self.frame_4,text="Crear Grafico",bd=6,foreground="black",background="lightgray",command=self.Matplotlib_graf)
         self.Agg_datos_frame_4.place(x=120 , y=460)
    
    def Matplotlib_graf(self):
        label_name_x: str = self.entry_axes_x.get()
        label_name_y: str = self.entry_axes_y.get()
        self.entry_axes_x.config(state="disabled")
        self.entry_axes_y.config(state="disabled")

        label_name_celd_axes_x: str = self.entry_variables_axes_x.get()
        label_name_celd_axes_y: str = self.entry_variables_axes_y.get()

        self.lista_axes_x: pd = self.read_csv[label_name_celd_axes_x].to_list()
        self.lista_axes_y: pd = self.read_csv[label_name_celd_axes_y].to_list()

        try:
            mat.plot(self.lista_axes_x, self.lista_axes_y,color="blue")
            mat.title("Grafico")
            mat.xlabel(label_name_x)
            mat.ylabel(label_name_y)
            mat.legend()
            mat.grid(True)
            mat.show()
        except KeyError:
            info = tk.Label(self.frame_4,text="La celda no son integer \n o no existe dicha celda",foreground="black",background="lightpink",font="consola 11 bold")
            info.place(x=7, y=500)


if __name__ == "__main__":
    root: tk.Tk = tk.Tk()
    appication = App(root)
    appication.PrincipalLayout()
    root.mainloop()