import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg




class Visualise(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Relativistic Charge Visualisation')
        self.root.geometry("1280x520")
        super().__init__(self.root)
        #self.win = tk.Toplevel()
        self.updating_pos = False
        self.figure = plt.Figure(figsize=(7, 5), dpi=100)
        self.figure.canvas.mpl_connect('motion_notify_event', lambda e: self.update_charge_pos(e))
        self.figure.canvas.mpl_connect('button_press_event', lambda e: self.toggle_updating(e))
        self.figure.canvas.mpl_connect('button_release_event', lambda e: self.toggle_updating(e))
        self.ax = self.figure.add_subplot(111)
        self.chart_type = FigureCanvasTkAgg(self.figure, self.root)
        self.chart_type.get_tk_widget().pack()
        self.ax.plot(np.linspace(0,1,5), np.linspace(0,1,5))
        self.chart_type.draw()

    
    # def matplotlib_to_tkinter(self, x):
    #     x = np.array([[x[0]],[x[1]]])
    #     mat1 = [-3.031443579456372, -4.828833563156737]
    #     tk1 = [-66., 87.]
    #     mat2 = [10.675953475476799, -0.25732417952460196]
    #     tk2 = [272., 7.]
    #     M = [[mat1[0], mat1[1], 0, 0], [0, 0, mat1[0], mat1[1]], [mat2[0], mat2[1], 0, 0], [0, 0, mat2[0], mat2[1]]]
    #     T = [[tk1[0]], [tk1[1]], [tk2[0]], [tk2[1]]]
    #     M = np.array(M)
    #     T = np.array(T)
    #     solution = np.matmul(np.linalg.inv(M), T).T.flatten()
    #     A = np.array([[solution[0], solution[1]], [solution[2], solution[3]]])
    #     kt_coords = np.matmul(A, x)
    #     kt_coords = kt_coords.T.flatten()
    #     abs_coord_x = self.chart_type.get_tk_widget().winfo_x() + kt_coords[
    #         0] + 0.5 * self.chart_type.get_tk_widget().winfo_width()
    #     abs_coord_y = self.chart_type.get_tk_widget().winfo_y() + kt_coords[
    #         1] + 0.5 * self.chart_type.get_tk_widget().winfo_height()
    #     return [abs_coord_x, abs_coord_y]

    def toggle_updating(self, event):
        self.updating_pos = not self.updating_pos

    def update_charge_pos(self, event):
        if self.updating_pos:
            print(event)
        #x = self.root.winfo_pointerx()
        #y = self.root.winfo_pointery()
        #print(x,y)
        pass

visualisation = Visualise()
visualisation.mainloop()