import tkinter as tk
from tkinter import ttk, messagebox
from functools import reduce

class EncuestaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Evaluación de Asignaturas")
        
        self.root.geometry("400x300")  
        self.root.resizable(False, False)
        
        self.evaluaciones = []
        self.aspectos = [
            "Contenido", "Actividades",  
            "Dificultad"  
        ]
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz gráfica"""
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.main_frame, text="Asignatura:").grid(row=0, column=0, sticky=tk.W)
        self.asignatura_entry = ttk.Entry(self.main_frame, width=30)
        self.asignatura_entry.grid(row=0, column=1, columnspan=3, sticky=tk.EW, pady=5)
        
        self.eval_vars = dict(zip(
            self.aspectos,
            [tk.IntVar(value=3) for _ in self.aspectos]
        ))
        
        def crear_controles_calificacion(aspecto, row):
            frame = ttk.Frame(self.main_frame)
            frame.grid(row=row, column=0, columnspan=4, sticky=tk.EW, pady=2)
            
            ttk.Label(frame, text=f"{aspecto}:").pack(side=tk.LEFT)
            
            ttk.Button(
                frame, text="-", width=3,
                command=lambda: self._ajustar_calificacion(aspecto, -1)
            ).pack(side=tk.LEFT, padx=5)
            
            ttk.Label(frame, textvariable=self.eval_vars[aspecto], width=3).pack(side=tk.LEFT)
            
            ttk.Button(
                frame, text="+", width=3,
                command=lambda: self._ajustar_calificacion(aspecto, 1)
            ).pack(side=tk.LEFT)
        
        list(map(
            lambda item: crear_controles_calificacion(item[1], item[0]+1),
            enumerate(self.aspectos)
        ))
        
        ttk.Button(
            self.main_frame, text="Agregar Evaluación", 
            command=self.agregar_evaluacion
        ).grid(row=len(self.aspectos)+2, column=0, columnspan=4, pady=10, sticky=tk.EW)
        
        ttk.Button(
            self.main_frame, text="Mostrar Resultados", 
            command=self.mostrar_resultados
        ).grid(row=len(self.aspectos)+3, column=0, columnspan=4, sticky=tk.EW)
        
        self.main_frame.columnconfigure(1, weight=1)
    
    def _ajustar_calificacion(self, aspecto, cambio):
        valor_actual = self.eval_vars[aspecto].get()
        nuevo_valor = max(1, min(5, valor_actual + cambio))
        self.eval_vars[aspecto].set(nuevo_valor)
    
    def agregar_evaluacion(self):
        asignatura = self.asignatura_entry.get().strip()
        if not asignatura:
            messagebox.showerror("Error", "Debe ingresar el nombre de la asignatura")
            return
        
        evaluacion = {
            "Asignatura": asignatura,
            **{aspecto: var.get() for aspecto, var in self.eval_vars.items()}
        }
        
        self.evaluaciones.append(evaluacion)
        messagebox.showinfo("Éxito", "Evaluación agregada correctamente")
        self.asignatura_entry.delete(0, tk.END)
    
    def mostrar_resultados(self):
        if not self.evaluaciones:
            messagebox.showinfo("Información", "No hay evaluaciones para mostrar")
            return
        
        result_window = tk.Toplevel(self.root)
        result_window.title("Resultados de Evaluaciones")
        result_window.geometry("600x400")
        
        notebook = ttk.Notebook(result_window)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        resumen_frame = ttk.Frame(notebook)
        notebook.add(resumen_frame, text="Resumen")
        
        asignaturas = list(set(map(lambda e: e["Asignatura"], self.evaluaciones)))
        
        list(map(
            lambda item: self._mostrar_asignatura(resumen_frame, item[1], item[0]),
            enumerate(asignaturas)
        ))
        
        detalles_frame = ttk.Frame(notebook)
        notebook.add(detalles_frame, text="Detalles")
        
        # Versión funcional para generar el texto
        def formatear_item(item):
            return f"  {item[0]}: {item[1]}"

        def formatear_evaluacion(e):
            items_no_asignatura = filter(lambda item: item[0] != 'Asignatura', e.items())
            items_formateados = map(formatear_item, items_no_asignatura)
            items_str = reduce(lambda a, b: a + "\n" + b, items_formateados, "")
            return f"Asignatura: {e['Asignatura']}\n" + items_str

        def concatenar_evaluaciones(e1, e2):
            return e1 + "\n\n" + e2

        texto = "Detalles de todas las evaluaciones:\n\n" + \
               reduce(
                   concatenar_evaluaciones,
                   map(formatear_evaluacion, self.evaluaciones),
                   ""
               )
        
        text_widget = tk.Text(detalles_frame, wrap=tk.WORD)
        text_widget.insert(tk.END, texto)
        text_widget.config(state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(detalles_frame, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _mostrar_asignatura(self, parent, asignatura, row):
        evals_asignatura = list(filter(lambda e: e["Asignatura"] == asignatura, self.evaluaciones))
        
        asignatura_frame = ttk.LabelFrame(parent, text=asignatura)
        asignatura_frame.grid(row=row, column=0, padx=10, pady=5, sticky=tk.EW)
        
        promedios = dict(zip(
            self.aspectos,
            map(
                lambda aspecto: reduce(lambda x, y: x + y, 
                                     map(lambda e: e[aspecto], evals_asignatura)) / len(evals_asignatura),
                self.aspectos
            )
        ))
        
        list(map(
            lambda item: (
                ttk.Label(asignatura_frame, text=f"{item[1]}:").grid(row=item[0], column=0, sticky=tk.W),
                ttk.Label(asignatura_frame, text=f"{promedios[item[1]]:.2f}").grid(row=item[0], column=1, sticky=tk.W)
            ),
            enumerate(self.aspectos)
        ))
        
        total = reduce(lambda x, y: x + y, promedios.values()) / len(promedios)
        ttk.Label(asignatura_frame, text="Total:").grid(row=len(self.aspectos), column=0, sticky=tk.W)
        ttk.Label(asignatura_frame, text=f"{total:.2f}").grid(row=len(self.aspectos), column=1, sticky=tk.W)

root = tk.Tk()
app = EncuestaApp(root)
root.mainloop()