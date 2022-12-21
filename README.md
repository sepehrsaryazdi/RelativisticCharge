# Relativistic Charge Visualisation

This is a quick project that visualises the relativistic electric field generated by moving charges. More precisely, this is computing:


![Electric Field Equation](equation.png | width=100px)

Note the equation above is ignoring magnetic field effects.

How it works:

1. Simply run the following in the main git repository:

```
pip3 install matplotlib numpy scipy
python3 main.py
```
2. The program will randomly generate two charges of any polarity `+1` or `-1` and draws their electric field.


![Electric Field During Update](screenshot.png)

3. The user can drag charges around and the field will update automatically.

![Charge Moved](screenshot2.png)

4. The program is relatively slow because of Matplotlib's plotting library; speed-ups can be made using better plotting techniques including caching.
