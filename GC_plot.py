# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 13:21:49 2016

@author: Diego Castaneda
email: dfcanopus@gmail.com

The data used here is from the work of Bellini et al. (2009)
http://adsabs.harvard.edu/abs/2009A%26A...493..959B

"""

import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly as py

# The database doesn't come with a header, so I copied the info from the 
# README file to get the colunm names
st = ("""   1-6  I6    ---      Seq     [1/376478] Star sequential number
   8-17  F10.6 deg      RAdeg   Right ascension (J2000, Epoch J2003.29)
  19-28  F10.6 deg      DEdeg   Declination (J2000, Epoch J2003.29)
  30-37  F8.3  pix      Xpos    X master frame position (distortion free)
  39-46  F8.3  pix      Ypos    Y master frame position (distortion free)
  48-53  F6.2  mas/yr   pmRA    Proper motion along RA, pmRAcosDE
  55-59  F5.2  mas/yr e_pmRA    Proper motion rms along pmRAcosDE
  61-66  F6.2  mas/yr   pmDE    Proper motion along pmDE
  68-72  F5.2  mas/yr e_pmDE    Proper motion rms along pmDE
  74-79  F6.3  mag      Umag    ?=99.999 Johnson U visual magnitude
  81-86  F6.3  mag    e_Umag    ?=99.999 Johnson U visual magnitude rms
  88-93  F6.3  mag      Bmag    ?=99.999 Johnson B visual magnitude
  95-100  F6.3  mag    e_Bmag    ?=99.999 Johnson B visual magnitude rms
 102-107  F6.3  mag      Vmag    ?=99.999 Johnson V visual magnitude
 109-114  F6.3  mag    e_Vmag    ?=99.999 Johnson V visual magnitude rms
 116-121  F6.3  mag      Rcmag   ?=99.999 Cousins R visual magnitude
 123-128  F6.3  mag    e_Rcmag   ?=99.999 Cousins R visual magnitude rms
 130-135  F6.3  mag      Icmag   ?=99.999 Cousins I visual magnitude
 137-142  F6.3  mag    e_Icmag   ?=99.999 Cousins I visual magnitude rms
 144-149  F6.3  mag      Ha      ?=99.999 Halpha visual magnitude
 151-156  F6.3  mag    e_Ha      ?=99.999 Halpha visual magnitude rms
 158-160  I3    %        Mm      Membership probability
 162-164  I3    %        Mm2     ?=-1 Membership probability alternative""").split("\n")
 
st = [i.split()[3] for i in st] # Select the column names from the st

# Read the file where the catalog is stored:
df = np.genfromtxt("catalog.dat")
# Make it a Pandas DataFrame for easy manipulation
# Setting the column names found in 'st'
df = pd.DataFrame(df, columns=st)

# Make the data selection so that only the objects with known
# Bmag, Vmag, Rmag, and proper motions are included.
sdf = df[df["Bmag"]!=99.999]
sdf = sdf[sdf["Rcmag"]!=99.999]
sdf = sdf[sdf["Vmag"]!=99.999]
sdf["pmMag"] = p_mot = np.sqrt((sdf.loc[:,"pmRA"])**2+(sdf.loc[:,"pmDE"])**2)
sdf = sdf[sdf["pmMag"]<10]

# Determine the x, y and z values we want to plot:
x = (sdf.loc[:,"Bmag"]-sdf.loc[:,"Rcmag"]).values
y = (sdf.loc[:,"Bmag"]-sdf.loc[:,"Vmag"]).values
z = -1.*(sdf.loc[:,"Bmag"]).values

# Define the Plotly dictionary that contains the information about the
# data and the kind of plot to render
trace = go.Scatter3d(
        name = "NGC5139",
        x = x[0:10000], y = y[0:10000], z = z[0:10000],
        mode = 'markers',
        marker = dict(
        cmin = 0,
        cmax = 10,
        color = sdf.loc[:,"pmMag"].values,
        colorscale = 'Jet',
        colorbar = go.ColorBar(title="Proper Motion [mas/yr]"),
        size=2.,
        line=dict(width=0)),
        opacity = 0.5
        )
data = [trace]


# Set the different layout properties of the figure:
layout = go.Layout(
    autosize=False,
    width=700,
    height=700,
    title='NGC5139',
    scene = go.Scene(
    camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=0.1, y=2.5, z=0.1)
    ),
    aspectmode='cube',
    xaxis=dict(
    title = "B-R [mag]"
    ),
    yaxis=dict(
    title = "B-V [mag]"
    ),
    zaxis=dict(
    title = "B [mag]",
    tickmode = "array",
    tickvals = [-24, -20, -16, -12],
    ticktext = ["24","20","16","12"]
    )),
)

# Finally, ask Plotly to render the plot and save it as some-name.html
fig = go.Figure(data=data, layout=layout)
py.offline.plot(fig, filename='ngc5139_3d.html')