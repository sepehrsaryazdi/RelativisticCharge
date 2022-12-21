import tkinter as tk
from threading import Thread
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import time
from scipy.optimize import fsolve
import matplotlib.style as mplstyle
mplstyle.use('fast')


class Charge:
    def __init__(self, x0, charge, visualisation):
        assert len(x0) == 2
        self.max_num_history = 100
        self.previous_positions = deque([x0]*self.max_num_history)
        self.updating_pos = False
        self.charge = charge
        self.c = 10
        self.d = 0.05
        self.k = 1
        self.visualisation = visualisation
        self.index = self.max_num_history-1
        self.active = True
        self.clock_update_thread = Thread(target=self.update_clock)
        self.clock_update_thread.start()
    
    def destroy(self):
        self.active = False
        
    def update_clock(self):
        while self.active:
            if self.index < self.max_num_history - 1:
                self.index+=1
            time.sleep(self.d/self.c)
            try:
                self.update_position(self.previous_positions[-1])
                self.visualisation.draw_updates()
            except:
                continue
            #print(self.electric_field(*self.previous_positions[-1]))
            
        

    def update_position(self, x):
        self.previous_positions.popleft()
        self.previous_positions.append(x)
        self.index -= 1
    
    def retarded_time_index(self, r, r_prime):
        distance = np.linalg.norm(r-r_prime)
        
        effective_index = int(np.round(self.index - distance/self.d))

        if effective_index < 0:
            effective_index = 0
        
        return effective_index
        

    def electric_field(self, r):
        f = self.create_norm_lambda_function(r)
        effective_centre = fsolve(f, np.array([0,0]))
        if np.square(r-effective_centre).sum(0) != 0:
            E = self.k*self.charge/(np.square(r-effective_centre).sum(0)) * (effective_centre - r)
        else:
            E = np.array([0,0])
       
        return E
        


    
    def create_norm_lambda_function(self, r):
        return lambda r_prime : r_prime - self.previous_positions[self.retarded_time_index(r, r_prime)]

        
        



class Visualise(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Relativistic Charge Visualisation')
        self.root.geometry("1280x520")
        super().__init__(self.root)
        self.num_charges = 1
        self.initial_points = [np.array([np.random.uniform(-1,1),0]) for i in range(self.num_charges)]
        self.charges = [Charge(self.initial_points[i], 2*np.random.random()-1, self) for i in range(self.num_charges)]
        self.updating_pos = False
        self.selected_charge = None
        self.xlim = [-1,1]
        self.ylim = [-1,1]
        self.num_vectors = 20
        self.arrow_scale = 0.1

        x = np.linspace(*self.xlim, self.num_vectors)
        y = np.linspace(*self.ylim, self.num_vectors)
        x,y = np.meshgrid(x,y)
        self.vector_points = np.array([x.flatten(), y.flatten()]).T

        self.figure = plt.Figure(figsize=(9, 5), dpi=100)
        self.figure.canvas.mpl_connect('motion_notify_event', lambda e: self.update_charge_pos(e))
        self.figure.canvas.mpl_connect('button_press_event', lambda e: self.toggle_updating(e))
        self.figure.canvas.mpl_connect('button_release_event', lambda e: self.toggle_updating(e))
        self.ax = self.figure.add_subplot(111)
        self.chart_type = FigureCanvasTkAgg(self.figure, self.root)
        self.chart_type.get_tk_widget().pack()
        self.draw_updates()
        # self.ax.plot(np.linspace(0,1,5), np.linspace(0,1,5))
    
    def draw_updates(self):
        self.ax.clear()
        self.ax.set_xlim(*self.xlim)
        self.ax.set_ylim(*self.ylim)
        self.ax.set_axis_off()
        self.draw_charge_positions()
        self.draw_net_vector_field()
        self.chart_type.draw()
        self.chart_type.draw()

    def get_net_electric_field(self, r):
        E = np.array([0.,0.])
        for q in self.charges:
            E += q.electric_field(r)
        return self.arrow_scale*E/np.linalg.norm(E) if np.linalg.norm(E) > 0 else np.array([0,0])

    def draw_net_vector_field(self):
        
        for v in self.vector_points:
            E = self.get_net_electric_field(v)
            self.ax.arrow(*v, *E , head_width=0.02,color="red")

       

    def draw_charge_positions(self):
        
        
        for q in self.charges:
            #self.ax.set_title(f"{q.previous_positions[-1]}")
            self.ax.scatter(*q.previous_positions[-1])
        
    

    def toggle_updating(self, event):
        self.updating_pos = not self.updating_pos
        if not self.updating_pos:
            for q in self.charges:
                q.updating_pos = False
            self.selected_charge = False

    def update_charge_pos(self, event):
        x_matplot = event.xdata
        y_matplot = event.ydata
        
        x = np.array([x_matplot,y_matplot])

        if not self.updating_pos:
            return

        if self.selected_charge:
            self.selected_charge.update_position(x)
            self.draw_updates()
            return
        
        distances = [np.linalg.norm(x-q.previous_positions[-1]) for q in self.charges]
        closest_charge = self.charges[np.argmin(distances)]
        
        if min(distances) < 0.5:
            closest_charge.updating_pos = True
            self.selected_charge = closest_charge
            
        closest_charge.update_position(x)
        self.draw_charge_positions()
    
    def destroy(self):
        for q in self.charges:
            q.destroy()

visualisation = Visualise()

visualisation.mainloop()
visualisation.destroy()
