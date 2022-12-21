import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque


class Charge:
    def __init__(self, x0):
        assert len(x0) == 2
        self.max_num_history = 100
        self.previous_positions = deque([x0]*self.max_num_history)
        self.updating_pos = False
    
    def update_position(self, x):
        self.previous_positions.popleft()
        self.previous_positions.append(x)



class Visualise(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Relativistic Charge Visualisation')
        self.root.geometry("1280x520")
        super().__init__(self.root)
        self.num_charges = 1
        self.initial_points = [np.array([np.random.uniform(-1,1),0]) for i in range(self.num_charges)]
        self.charges = [Charge(self.initial_points[i]) for i in range(self.num_charges)]
        self.updating_pos = False
        self.figure = plt.Figure(figsize=(7, 5), dpi=100)
        self.figure.canvas.mpl_connect('motion_notify_event', lambda e: self.update_charge_pos(e))
        self.figure.canvas.mpl_connect('button_press_event', lambda e: self.toggle_updating(e))
        self.figure.canvas.mpl_connect('button_release_event', lambda e: self.toggle_updating(e))
        self.ax = self.figure.add_subplot(111)
        self.chart_type = FigureCanvasTkAgg(self.figure, self.root)
        self.chart_type.get_tk_widget().pack()
        self.draw_charge_positions()
        # self.ax.plot(np.linspace(0,1,5), np.linspace(0,1,5))
    
    def draw_charge_positions(self):
        self.ax.clear()
        self.ax.set_xlim(-1,1)
        self.ax.set_ylim(-1,1)
        self.ax.set_axis_off()
        
        for q in self.charges:
            #self.ax.set_title(f"{q.previous_positions[-1]}")
            self.ax.scatter(*q.previous_positions[-1])
        
        self.chart_type.draw()



    def toggle_updating(self, event):
        self.updating_pos = not self.updating_pos
        if not self.updating_pos:
            for q in self.charges:
                q.updating_pos = False

    def update_charge_pos(self, event):
        x_matplot = event.xdata
        y_matplot = event.ydata
        
        x = np.array([x_matplot,y_matplot])
        for q in self.charges:
            if self.updating_pos or q.updating_pos:
                #print(np.linalg.norm(np.array([x_matplot,y_matplot])-q.previous_positions[-1]))
                if np.linalg.norm(x-q.previous_positions[-1]) < 0.5:
                    q.updating_pos = True
                q.update_position(x)
                self.draw_charge_positions()


                    
                    #print(x_matplot,y_matplot)
                    #print(np.linalg.norm(np.array([x_matplot,y_matplot])-q.previous_positions[-1]))

        
            
        #x = self.root.winfo_pointerx()
        #y = self.root.winfo_pointery()
        #print(x,y)
        pass

visualisation = Visualise()
visualisation.mainloop()