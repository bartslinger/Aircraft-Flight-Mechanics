*(Note: the US spelling is maneuver, but it took me years of muscle memory training to spell manoeuvre correctly, and I won't be losing it easily.)*

# Acceleration, Manoeuvres, and Aircraft Loading

The preceding analysis has been constrained to *steady* flight - that is, with zero acceleration. For the cases of climb, the climb rate was assumed to be steady.

To understand unconstrained aircraft manoeuvres requires an understanding of accelerated flight.

Manoeuvre will be broken down into horizontal (e.g., flat or banked turns) and vertical manoeuvres (e.g., loops, pull-ups), comprising curvilinear motion. Such manoeuvres are the result of a force *perpendicular* to the flight path, giving a normal acceleration.

All of the manoevures discussed are the result of a **variation in lift**, which can be *large*. Consider that the dynamic pressure rises with the square of the forward speed, so a five-fold speed increase results in twenty-five times the aerodynamic forces.

Before discussing manoeuvres, a means to represent the allowable amount of load on an aircraft will be introduced. 

## Load Factor

The load that can be safely taken through an aircraft dictates the load limits on an aircraft - for this the **load factor** is introduced as a non-dimensional measure of the load variation.

```{math}
:label: LoadFactor
n=\frac{L}{W}
````

```{admonition} So - *what is the load factor for steady level flight?*
:class: dropdown
In steady level flight, the equilibrium steady flight condition is $L=W$ so $n=1$
```

There are two structural limits defined for aircraft:
- **Limit Loads**, $n_{l}$ are the loads at which *plastic deformation* will occur. At flight with $1<n<n_1$, *elastic structural deformation* will occur on parts of the aircraft, and the parts will return to the design or equilibrium position once the loads are removed

   If flight occurs at $n>n_l$, the aircraft will require inspection and likely replacement of parts.
   
   
- **Ultimate Loads**, $n_{u}$ are the loads at which *failure* will occur. At flight with $n>n_u$, *parts of the aircraft will break*

The numerical value of the load factor is an exercise in structural analysis, whereby the loads and their paths are applied to a model of the aircraft, and a determination of $n_l$ and $n_u$ can be made.

In general, $n_l$ and $n_u$ will be defined with a safety factor of 50% - such that plastic structural deformation may not actually occur until $n_l*1.5$. This should not be considered a margin to 'play with', however!

### Values of the load factor

FAR 23 (Federal Aviation Requirement) dictates the *minimum* load factor required for three categories of aircraft:
- Commuter Aircraft
- Utility Aircraft
- Aerobatic Aircraft

The minimum load factors are defined as (since this is from FAR 23, $W$ is defined in $lbf$)


| Aircraft Category | Minimum positive load factor, $n+$    | Minimum negative load factor, $n-$ |
|-------------------|---------------------------------------|------------------------------------|
| Normal/Commuter   | smaller of $2.1+\frac{24000}{W+1000}$ or $3.8$  | $0.4n+$                            |
| Utility           | $4.4$                                 | $0.4n+$                            |
| Aerobatic         | $6.0$                                 | $0.5n+$                            |

Often pilots will talk about *load factor* in terms of "g"s - for straight and level flight, 1$g$ feels like regular earth gravity, whilst an $n=2$ or $2g$ manoeuvre makes the occupants feel *twice as heavy*.

Since the load factor represents the amount of lift being produced, it is an easy and instructive means to define the structural limits of an aircraft - $e.g.,$ the loads for which the wings will break off.

### V-n diagram

```{admonition} Bear in mind...
:class: dropdown

In what's becoming a common phrase in this document - the following is a simplification of the theory, designed to give you a good insight into the physics of the problem. Construction of a full $V-n$ diagram is complicated and more of an exercise in understanding FAA certification than it is the flight physics.

What follows is a suitable explanation for an undergraduate aerospace engineer.

```

The values of the limit loads, and ultimate loads are presented on a graph vs. airspeed. For the following, the loads will be presented against *equivalent airspeed* because that enables a single graph to be plotted, but for real aircraft this is usually presented against *indicated airspeed*, with several lines representing different altitudes.

There are many different means of showing how to construct a $V-n$ diagram in textbook and online, but most seem geared up to helping pilots understand them rather than aerospace engineers. For example - the following show good examples of how to formulate a $V-n$ diagram, [website one](http://www.aviationchief.com/operating-flight-strength-v-g--v-n-diagrams.html), [website two](https://code7700.com/g450_limitations.htm#weight).

For the following example, a representative jet trainer aircraft will be used, with structural limit loads of $-3.0<n_l<7.0$ and ultimate loads of $-5.0<n_u<11.0$.

For a range of flight speeds up to $M=1.0$, the loads above can be plotted against $EAS$ taking into account the $n$ values above only.


import numpy as np
import plotly.graph_objects as go

# Limit loads
n_l = [-3.0, 7.0]

# Ultimate loads
n_u = [-5.0, 11.0]

# Make a figure
fig = go.Figure()

# Make a vector of equivalent airspeed (m/s)
VE = np.linspace(0, 340, 1000)

# Plot the Structural damage area
x_structural_damage = [VE.min(), VE.max()]
y_structural_damage = [n_l[1], n_l[1]]
y_structural_failure = [n_u[1], n_u[1]]

## Positive strucutral damage
# Plot a line of the structural damage
fig.add_trace(go.Scatter(x=VE, y=n_l[1] * np.ones(VE.shape),
    fill=None,
    mode='lines',
    line_color='indigo', name="+nl",
    showlegend=False))

# Then a line of the structural failure that is filled to the structural damage
fig.add_trace(go.Scatter(
    x=x_structural_damage,
    y=y_structural_failure,
    fill='tonexty', # fill area between structural failure and structural Damage
    mode='none', fillcolor='rgba(255, 0, 0, 0.25)', name="Structural Damage", showlegend=False))

# Annotate the structural failure area
fig.add_trace(go.Scatter(
    x=[np.mean(x_structural_damage)],
    y=[0.5 * (n_l[1] + n_u[1])],
    mode='text',
    text="Structural Damage", showlegend=False))

# Add the ultimate load factor
fig.add_trace(go.Scatter(x=VE, y=n_u[1] * np.ones(VE.shape),
    mode='lines',
    line_color='red', name="+nu",
    showlegend=False))

# Then a line of the structural failure that is filled to the structural damage
fig.add_trace(go.Scatter(
    x=VE, y=3*n_u[1] * np.ones(VE.shape),
    fill='tonexty', # fill area between structural failure and structural Damage
    mode='none', fillcolor='rgba(255, 0, 0, 0.55)', name="Structural Damage", showlegend=False, hoverinfo="none"))

# Annotate the structural failure area
fig.add_trace(go.Scatter(
    x=[np.mean(x_structural_damage)],
    y=[n_u[1] + 0.05 * (n_l[1] + n_u[1])],
    mode='text',
    text="Structural Failure", showlegend=False, hoverinfo="none"))




### Negative side



## Negative structural damage
x_structural_damage = [VE.min(), VE.max()]
y_structural_damage = [n_l[0], n_l[0]]
y_structural_failure = [n_u[0], n_u[0]]
# Plot a line of the structural damage
fig.add_trace(go.Scatter(x=VE, y=n_l[0] * np.ones(VE.shape),
    fill=None,
    mode='lines',
    line_color='indigo',
    name="-nl",
    showlegend=False))

# Then a line of the structural failure that is filled to the structural damage
fig.add_trace(go.Scatter(
    x=x_structural_damage,
    y=y_structural_failure,
    fill='tonexty', # fill area between trace0 and trace1
    mode='none', fillcolor='rgba(255, 0, 0, 0.25)', name="Structural Damage", showlegend=False))

# Annotate the structural damage area
fig.add_trace(go.Scatter(
    x=[np.mean(x_structural_damage)],
    y=[0.5 * (n_l[0] + n_u[0])],
    mode='text',
    text="Structural Damage", showlegend=False))

# Add the ultimate load factor
fig.add_trace(go.Scatter(x=VE, y=n_u[0] * np.ones(VE.shape),
    fill=None,
    mode='lines',
    line_color='red', name="-nu",
    showlegend=False))

# Then a line of the structural failure that is filled to the structural damage
fig.add_trace(go.Scatter(
    x=VE, y=3*n_u[0] * np.ones(VE.shape),
    fill='tonexty', # fill area between structural failure and structural Damage
    mode='none', fillcolor='rgba(255, 0, 0, 0.55)', name="Structural Damage", showlegend=False, hoverinfo="none"))


# Annotate the structural failure area
fig.add_trace(go.Scatter(
    x=[np.mean(x_structural_damage)],
    y=[n_u[0] + 0.05 * (n_l[0] + n_u[0])],
    mode='text',
    text="Structural Failure", showlegend=False, hoverinfo="none"))

# Change the limits
fig.update_yaxes(range= [1.2 * n_u[0], 1.2 * n_u[1]])

fig.update_layout(
    title="Representative Structural Damage and Failure Load Factors",
    xaxis_title="$V_E/\\text{m/s}$",
    yaxis_title="$n$",
)

# Dick around with the hover behaviour
fig.update_traces(hovertemplate=None)
fig.update_layout(hovermode="x unified")

fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='black')
fig.show()

#### Stall limits on V-n diagram

At this stage, the $V-n$ diagram isn't particularly useful. You can hover over the graph and see that values of allowable load is constant with airspeed. 

The graph will be adapted by inclusion of other limitations. The first of which is that **at certain airspeeds, the aircraft will stall prior to $n_l$ being reached**, and therefore this influences the speed at which manoeuvres can be attempted safely.

It can be shown from the definition of the load factor, and the definition of the lift coefficient that the load factor associated with *stall* is given by

$$n_{stall}=\frac{C_{L,max}\,\tfrac{1}{2}\rho V^2\,S}{W}$$

If the aircraft is taken to have a wing area of 16m$^2$, and a weight of 53kN, and a $C_{L,max}$ of 1.6 with a $C_{L,min}$ of -1.0, then the variation of $n_{stall}$ can be overlaid on the previous graph

```{margin}
You might not have considered Clmin before - but it's the condition at which the flow around the wing will separate due to *negative* incidence
```

It can be appreciated that if the stall occurs for $n < 1$, then steady flight is not possible at this speed.


import numpy as np
import plotly.graph_objects as go

# Limit loads
n_l = [-3.0, 7.0]

# Ultimate loads
n_u = [-5.0, 11.0]

# Make a figure
fig = go.Figure()

# Make a vector of equivalent airspeed (m/s)
VE = np.linspace(0, 340, 1000)

# Plot the Structural damage area
x_structural_damage = [VE.min(), VE.max()]
y_structural_damage = [n_l[1], n_l[1]]
y_structural_failure = [n_u[1], n_u[1]]

## Positive strucutral damage
# Plot a line of the structural damage
fig.add_trace(go.Scatter(x=VE, y=n_l[1] * np.ones(VE.shape),
    fill=None,
    mode='lines',
    line_color='indigo', name="+nl",
    showlegend=False))

# Then a line of the structural failure that is filled to the structural damage
fig.add_trace(go.Scatter(
    x=x_structural_damage,
    y=y_structural_failure,
    fill='tonexty', # fill area between structural failure and structural Damage
    mode='none', fillcolor='rgba(255, 0, 0, 0.25)', name="Structural Damage", showlegend=False))

# Annotate the structural failure area
fig.add_trace(go.Scatter(
    x=[np.mean(x_structural_damage)],
    y=[0.5 * (n_l[1] + n_u[1])],
    mode='text',
    text="Structural Damage", showlegend=False))

# Add the ultimate load factor
fig.add_trace(go.Scatter(x=VE, y=n_u[1] * np.ones(VE.shape),
    mode='lines',
    line_color='red', name="+nu",
    showlegend=False))

# Then a line of the structural failure that is filled to the structural damage
fig.add_trace(go.Scatter(
    x=VE, y=3*n_u[1] * np.ones(VE.shape),
    fill='tonexty', # fill area between structural failure and structural Damage
    mode='none', fillcolor='rgba(255, 0, 0, 0.55)', name="Structural Damage", showlegend=False, hoverinfo="none"))

# Annotate the structural failure area
fig.add_trace(go.Scatter(
    x=[np.mean(x_structural_damage)],
    y=[n_u[1] + 0.05 * (n_l[1] + n_u[1])],
    mode='text',
    text="Structural Failure", showlegend=False, hoverinfo="none"))


# Add in stall
S = 16
W = 53e3
Clmax = 1.6
Clmin = -1.0
n_stall = Clmax * 0.5 * 1.225 * VE**2 * S / W
n_stall_negative = Clmin * 0.5 * 1.225 * VE**2 * S / W

## Get the maneovure speeds
Va = np.sqrt(n_l[1] * W / (Clmax * 0.5 * 1.225 * S))
fig.add_trace(go.Scatter(x=[Va], y=[n_l[1]],
    mode='markers+text',
    text="$V_A$",
    textposition="bottom right",
    showlegend=False))

Va2 = np.sqrt(n_l[0] * W / (Clmin * 0.5 * 1.225 * S))
fig.add_trace(go.Scatter(x=[Va2], y=[n_l[0]],
    mode='markers+text',
    text="$V_{A2}$",
    textposition="top right",
    showlegend=False))

# Overlay the stall n diagrams
# Positive
fig.add_trace(go.Scatter(x=VE, y=n_stall,
    mode='lines',
    line_color='red', name="Positive Stall",
    showlegend=True))

# Redo just up to Va to make sure the next fill is correct (else it fills above the limit load)
fig.add_trace(go.Scatter(x=VE[n_stall <= n_l[1]], y=n_stall[n_stall <= n_l[1]],
    mode='lines',
    line_color='red',
    showlegend=False, name="Positive Stall"))

## Put some filled areas in here to show the positive stall limit
V_stall_limited = np.linspace(0.1, Va, 100)
fig.add_trace(go.Scatter(
    x=V_stall_limited, y=n_l[1] * np.ones(V_stall_limited.shape),
    fill='tonexty', fillcolor='rgba(255, 255, 0, 0.55)', 
    name="Stall Limited", showlegend=False, hoverinfo="none"))

# Annotate the postitive stall limit
fig.add_trace(go.Scatter(
    x=[np.mean(V_stall_limited)],
    y=[0.5 * np.array([n_l[1] * np.ones(V_stall_limited.shape)]).mean()],
    mode='text',
    text="Stall Limited", showlegend=False, hoverinfo="none"))

# Negative
fig.add_trace(go.Scatter(x=VE, y=n_stall_negative,
    mode='lines',
    line_color='green', name="Negative Stall",
    showlegend=True))

# Redo just up to Va to make sure the next fill is correct (else it fills above the limit load)
fig.add_trace(go.Scatter(x=VE[n_stall_negative >= n_l[0]], y=n_stall_negative[n_stall_negative >= n_l[0]],
    mode='lines',
    line_color='green',
    showlegend=False, name ="Negative Stall"))

## Put some filled areas in here to show the negative stall limit
V_stall_limited = np.linspace(0.1, Va2, 100)
fig.add_trace(go.Scatter(
    x=V_stall_limited, y=n_l[0] * np.ones(V_stall_limited.shape),
    fill='tonexty', fillcolor='rgba(255, 255, 0, 0.55)', 
    name="Stall Limited", showlegend=False, hoverinfo="none"))

# Annotate the negative stall limit
fig.add_trace(go.Scatter(
    x=[np.mean(V_stall_limited)],
    y=[0.5 * np.array([n_l[0] * np.ones(V_stall_limited.shape)]).mean()],
    mode='text',
    text="Stall Limited", showlegend=False, hoverinfo="none"))

# Add a line for the steady stall



### Negative side
## Negative structural damage
x_structural_damage = [VE.min(), VE.max()]
y_structural_damage = [n_l[0], n_l[0]]
y_structural_failure = [n_u[0], n_u[0]]
# Plot a line of the structural damage
fig.add_trace(go.Scatter(x=VE, y=n_l[0] * np.ones(VE.shape),
    fill=None,
    mode='lines',
    line_color='indigo',
    name="-nl",
    showlegend=False))

# Then a line of the structural failure that is filled to the structural damage
fig.add_trace(go.Scatter(
    x=x_structural_damage,
    y=y_structural_failure,
    fill='tonexty', # fill area between trace0 and trace1
    mode='none', fillcolor='rgba(255, 0, 0, 0.25)', name="Structural Damage", showlegend=False))

# Annotate the structural damage area
fig.add_trace(go.Scatter(
    x=[np.mean(x_structural_damage)],
    y=[0.5 * (n_l[0] + n_u[0])],
    mode='text',
    text="Structural Damage", showlegend=False))

# Add the ultimate load factor
fig.add_trace(go.Scatter(x=VE, y=n_u[0] * np.ones(VE.shape),
    fill=None,
    mode='lines',
    line_color='red', name="-nu",
    showlegend=False))

# Then a line of the structural failure that is filled to the structural damage
fig.add_trace(go.Scatter(
    x=VE, y=3*n_u[0] * np.ones(VE.shape),
    fill='tonexty', # fill area between structural failure and structural Damage
    mode='none', fillcolor='rgba(255, 0, 0, 0.55)', name="Structural Damage", showlegend=False, hoverinfo="none"))


# Annotate the structural failure area
fig.add_trace(go.Scatter(
    x=[np.mean(x_structural_damage)],
    y=[n_u[0] + 0.05 * (n_l[0] + n_u[0])],
    mode='text',
    text="Structural Failure", showlegend=False, hoverinfo="none"))

# Change the limits
fig.update_yaxes(range= [1.2 * n_u[0], 1.2 * n_u[1]])

fig.update_layout(
    title="Representative Structural Damage and Failure Load Factors",
    xaxis_title="$EAS/m/s$",
    yaxis_title="$n$",
)

# Dick around with the hover behaviour
# fig.update_traces(hovertemplate=None)
# fig.update_layout(hovermode="x unified")

fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='black')
fig.show()

#### Manoeuvre Speed

The intersection of the stall boundary and the limit load defines $V_A$, the **Manoeuvre Speed**. Sometimes this is called the *corner speed*. 

At speeds below $V_A$, fore/aft motion of the stick cannot produce enough load for structural damage to occur as the flow will separate before reaching an incidence at which $n_l$ would occur. Hence at speeds below $V_A$, the aircraft is *stall limited*.

Hence $V_A$ is the **highest speed for safe application of maximum control deflection**, whereas **at speeds above $V_A$, the controls inputs must be limited to avoid overloading the airframe**.

$V_A$ can be defined in terms of the maxmimum lift coefficient and the aircraft parameters

$$V_A=\sqrt{\frac{2\cdot n_l\cdot W}{C_{L_{max}}\,\rho\,S}}$$

##### Manoeuvre Speed on a real aircraft

On a real aircraft, $V_A$ may be defined at a *lower* speed allowing for a dynamic overshoot.

Furthermore, $V_A$ is defined **only for pure pitching motion**. Combinations of pitch, roll, and yaw can lead to increased loads, as can *dynamic motion* which allows flow to stay *attached* for higher angles of attack than the steady state condition.

The latter proved fatal in 2001, when American Airlines Flight 587 took off from JFK. The Airbus A300-605R followed Japan Airlines Flight 47, and encountered *wake turbulence*.

The First Officer applied repeated opposite rudder inputs (which, as an aside, is a great way to set up a *Dutch Roll* oscillation), which increased the load on the vertical stabiliser until it ultimately sheared off - which occurred in <7s.

All 260 people aboard the aircraft, and 5 people on the ground were killed in the crash. This is America's second-deadliest aviation accident.

```{epigraph}
*The National Transportation Safety Board determines that the probable cause of this accident was the in-flight separation of the vertical stabilizer as a result of the loads beyond ultimate design that were created by the first officer’s unnecessary and excessive rudder pedal inputs. Contributing to these rudder pedal inputs were characteristics of the Airbus A300-600 rudder system design and elements of the American Airlines Advanced Aircraft Maneuvering Program (AAMP).*

-- [NTSB Accident Report](https://www.ntsb.gov/investigations/AccidentReports/Reports/AAR0404.pdf)
```
There were other contributing factors to the accident, such as the light pedal forces on the aircraft misleading the pilots to the tail aerodynamic forces. But the salient point here is that **the airframe was destroyed due to aerodynamic load at a velocity far lower than the manoeuvring speed**.

The sobering story here is included to show the real world application, and limitations of the theory taught in this class. Manoeuvring speed is a useful tool to understand loads on an airframe, and we will use it to understand the limits in certain manoevures - whether they are *stall limited* or $n$ *limited*.

However, maoeuvring speed is is often poorly understood, and this can be disastrous.


#### High-Speed Limit

The graph above has been present with all speeds up the speed of sound at sea-level. Not all aircraft can achieve this speed, some due to powerplant limitations, and others due to dangerous aerodynamic phenomena including:
- **Torsional Divergence** - where the wings twist up to the point that they snap off. Less common with wing aft-sweep, and impossible for certain planforms (*e.g.,* the *Spitfire* had an *imaginary* divergence speed).
- **Flutter** - a coupled bend/twist oscillation that is _negatively aerodynamically damped_ which, again, can lead to the wings or other aerodynamic surface snapping off.
- **Control Reversal** - where the moment provided by the control surface causes the entire wing to flex to the point that the incremental aerodynamic change due to control surface deflection is negated by the change to flexure of the wing. At speeds above the _control reversal speed_ the controls are...well...reversed.
- **Buffeting** - high frequency oscillatory aerodynamic phenomena that may occur at high speeds.

The mechanism of action is not of interest of this course - though if you took MMAE 304 Aerostructures, you will know how to determine *divergence speed* and *control reversal speed*.

Fundamentally, there will be a *defined speed* that the aircraft cannot fly above and this needs to be represented on the $V-n$ diagram. This is called the **dive speed**, $V_D$.

For the jet trainer aircraft, consider $V_D=300$m/s. This can be represented on the figure as a vertical line on the right-hand side.

import numpy as np
import plotly.graph_objects as go

# Limit loads
n_l = [-3.0, 7.0]

# Ultimate loads
n_u = [-5.0, 11.0]

# Make a figure
fig = go.Figure()

# Make a vector of equivalent airspeed (m/s)
VE = np.linspace(0, 340, 1000)

# Plot the Structural damage area
x_structural_damage = [VE.min(), VE.max()]
y_structural_damage = [n_l[1], n_l[1]]
y_structural_failure = [n_u[1], n_u[1]]

## Positive strucutral damage
# Plot a line of the structural damage
fig.add_trace(go.Scatter(x=VE, y=n_l[1] * np.ones(VE.shape),
    fill=None,
    mode='lines',
    line_color='indigo', name="+nl",
    showlegend=False))

# Then a line of the structural failure that is filled to the structural damage
fig.add_trace(go.Scatter(
    x=x_structural_damage,
    y=y_structural_failure,
    fill='tonexty', # fill area between structural failure and structural Damage
    mode='none', fillcolor='rgba(255, 0, 0, 0.25)', name="Structural Damage", showlegend=False))

# Annotate the structural failure area
fig.add_trace(go.Scatter(
    x=[np.mean(x_structural_damage)],
    y=[0.5 * (n_l[1] + n_u[1])],
    mode='text',
    text="Structural Damage", showlegend=False))

# Add the ultimate load factor
fig.add_trace(go.Scatter(x=VE, y=n_u[1] * np.ones(VE.shape),
    mode='lines',
    line_color='red', name="+nu",
    showlegend=False))

# Then a line of the structural failure that is filled to the structural damage
fig.add_trace(go.Scatter(
    x=VE, y=3*n_u[1] * np.ones(VE.shape),
    fill='tonexty', # fill area between structural failure and structural Damage
    mode='none', fillcolor='rgba(255, 0, 0, 0.55)', name="Structural Damage", showlegend=False, hoverinfo="none"))

# Annotate the structural failure area
fig.add_trace(go.Scatter(
    x=[np.mean(x_structural_damage)],
    y=[n_u[1] + 0.05 * (n_l[1] + n_u[1])],
    mode='text',
    text="Structural Failure", showlegend=False, hoverinfo="none"))


# Add in stall
S = 16
W = 53e3
Clmax = 1.6
Clmin = -1.0
n_stall = Clmax * 0.5 * 1.225 * VE**2 * S / W
n_stall_negative = Clmin * 0.5 * 1.225 * VE**2 * S / W

## Get the maneovure speeds
Va = np.sqrt(n_l[1] * W / (Clmax * 0.5 * 1.225 * S))
fig.add_trace(go.Scatter(x=[Va], y=[n_l[1]],
    mode='markers+text',
    text="$V_A$",
    textposition="bottom right",
    showlegend=False))

Va2 = np.sqrt(n_l[0] * W / (Clmin * 0.5 * 1.225 * S))
fig.add_trace(go.Scatter(x=[Va2], y=[n_l[0]],
    mode='markers+text',
    text="$V_{A2}$",
    textposition="top right",
    showlegend=False))

# Overlay the stall n diagrams
# Positive
fig.add_trace(go.Scatter(x=VE, y=n_stall,
    mode='lines',
    line_color='red', name="Positive Stall",
    showlegend=False))

# Redo just up to Va to make sure the next fill is correct (else it fills above the limit load)
fig.add_trace(go.Scatter(x=VE[n_stall <= n_l[1]], y=n_stall[n_stall <= n_l[1]],
    mode='lines',
    line_color='red',
    showlegend=False, name="Positive Stall"))

## Put some filled areas in here to show the positive stall limit
V_stall_limited = np.linspace(0.1, Va, 100)
fig.add_trace(go.Scatter(
    x=V_stall_limited, y=n_l[1] * np.ones(V_stall_limited.shape),
    fill='tonexty', fillcolor='rgba(255, 255, 0, 0.55)', 
    name="Stall Limited", showlegend=False, hoverinfo="none"))

# Annotate the postitive stall limit
fig.add_trace(go.Scatter(
    x=[np.mean(V_stall_limited)],
    y=[0.5 * np.array([n_l[1] * np.ones(V_stall_limited.shape)]).mean()],
    mode='text',
    text="Stall Limited", showlegend=False, hoverinfo="none"))

# Negative
fig.add_trace(go.Scatter(x=VE, y=n_stall_negative,
    mode='lines',
    line_color='green', name="Negative Stall",
    showlegend=False))

# Redo just up to Va to make sure the next fill is correct (else it fills above the limit load)
fig.add_trace(go.Scatter(x=VE[n_stall_negative >= n_l[0]], y=n_stall_negative[n_stall_negative >= n_l[0]],
    mode='lines',
    line_color='green',
    showlegend=False, name ="Negative Stall"))

## Put some filled areas in here to show the negative stall limit
V_stall_limited = np.linspace(0.1, Va2, 100)
fig.add_trace(go.Scatter(
    x=V_stall_limited, y=n_l[0] * np.ones(V_stall_limited.shape),
    fill='tonexty', fillcolor='rgba(255, 255, 0, 0.55)', 
    name="Stall Limited", showlegend=False, hoverinfo="none"))

# Annotate the negative stall limit
fig.add_trace(go.Scatter(
    x=[np.mean(V_stall_limited)],
    y=[0.5 * np.array([n_l[0] * np.ones(V_stall_limited.shape)]).mean()],
    mode='text',
    text="Stall Limited", showlegend=False, hoverinfo="none"))

# Add an area for the stall that occurs with n < 1 - steady flight not possible
slow_stall_x = VE[n_stall < 1]
slow_stall_y = n_stall[n_stall < 1]
slow_negative_stall_x = VE[n_stall < 1]
slow_negative_stall_y = n_stall_negative[n_stall < 1]

fig.add_trace(go.Scatter(
    x=slow_negative_stall_x, y=slow_negative_stall_y,
    mode='lines', fillcolor='rgba(255, 0, 0, 0.55)', name="Steady Stall", showlegend=False, hoverinfo="none"))

fig.add_trace(go.Scatter(
    x=slow_stall_x, y=slow_stall_y,
    fill='tonexty', # fill area between structural failure and structural Damage
    mode='lines', fillcolor='rgba(255, 0, 0, 0.55)', name="Steady Stall", showlegend=False, hoverinfo="none"))

### Negative side
## Negative structural damage
x_structural_damage = [VE.min(), VE.max()]
y_structural_damage = [n_l[0], n_l[0]]
y_structural_failure = [n_u[0], n_u[0]]
# Plot a line of the structural damage
fig.add_trace(go.Scatter(x=VE, y=n_l[0] * np.ones(VE.shape),
    fill=None,
    mode='lines',
    line_color='indigo',
    name="-nl",
    showlegend=False))

# Then a line of the structural failure that is filled to the structural damage
fig.add_trace(go.Scatter(
    x=x_structural_damage,
    y=y_structural_failure,
    fill='tonexty', # fill area between trace0 and trace1
    mode='none', fillcolor='rgba(255, 0, 0, 0.25)', name="Structural Damage", showlegend=False))

# Annotate the structural damage area
fig.add_trace(go.Scatter(
    x=[np.mean(x_structural_damage)],
    y=[0.5 * (n_l[0] + n_u[0])],
    mode='text',
    text="Structural Damage", showlegend=False))

# Add the ultimate load factor
fig.add_trace(go.Scatter(x=VE, y=n_u[0] * np.ones(VE.shape),
    fill=None,
    mode='lines',
    line_color='red', name="-nu",
    showlegend=False))

# Then a line of the structural failure that is filled to the structural damage
fig.add_trace(go.Scatter(
    x=VE, y=3*n_u[0] * np.ones(VE.shape),
    fill='tonexty', # fill area between structural failure and structural Damage
    mode='none', fillcolor='rgba(255, 0, 0, 0.55)', name="Structural Damage", showlegend=False, hoverinfo="none"))


# Annotate the structural failure area
fig.add_trace(go.Scatter(
    x=[np.mean(x_structural_damage)],
    y=[n_u[0] + 0.05 * (n_l[0] + n_u[0])],
    mode='text',
    text="Structural Failure", showlegend=False, hoverinfo="none"))



# Add the Dive Speed

Vd = 300

fig.add_trace(go.Scatter(x=[Vd, Vd], y=[n_l[0], n_l[1]],
    fill=None,
    mode='lines',
    line_color='violet', name="Dive Speed",
    showlegend=True))

# Add a line of the dynamic damage
fig.add_trace(go.Scatter(
    x=[340, 340], y=[n_l[0], n_l[1]],
    fill='tonextx', # fill area between structural failure and structural Damage
    mode='none', fillcolor='rgba(255, 0, 255, 0.55)', name="Structural Damage", showlegend=False, hoverinfo="none"))

# Annotate the negative stall limit
fig.add_trace(go.Scatter(
    x=[315],
    y=[0.5 * (n_l[0] + n_l[1])],
    mode='text',
    text="Dynamic", showlegend=False, hoverinfo="none"))

fig.add_trace(go.Scatter(
    x=[315],
    y=[0.2 * (n_l[0] + n_l[1])],
    mode='text',
    text="Phenomena", showlegend=False, hoverinfo="none"))






# Change the limits
fig.update_yaxes(range= [1.2 * n_u[0], 1.2 * n_u[1]])

fig.update_layout(
    title="Representative Structural Damage and Failure Load Factors",
    xaxis_title="$EAS/m/s$",
    yaxis_title="$n$",
)

# Dick around with the hover behaviour
# fig.update_traces(hovertemplate=None)
# fig.update_layout(hovermode="x unified")

fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='black')
fig.show()

The area inside the graph above represents the *envelope*, and is the source of the phrase *out of the envelope*.



import numpy as np
import plotly.graph_objects as go

# Limit loads
n_l = [-3.0, 7.0]

# Ultimate loads
n_u = [-5.0, 11.0]

# Make a figure
fig = go.Figure()

Vstall = np.sqrt(2 * W / 1.225 / S / Clmax)

# Make a vector of equivalent airspeed (m/s) - only up to dive speed
VE = np.linspace(Vstall, Vd, 1000)
VE = VE[VE > Vstall]

# Make the positive and negative stall limits
S = 16
W = 53e3
Clmax = 1.6
Clmin = -1.0
n_stall = Clmax * 0.5 * 1.225 * VE**2 * S / W
n_stall_negative = Clmin * 0.5 * 1.225 * VE**2 * S / W

# Make vectors of positive and negative limit loads
n_l_positive = n_l[1] * np.ones(VE.shape)
n_l_negative = n_l[0] * np.ones(VE.shape)

# Make an array of the MINIMUM of the stall or the n_l
n_limit_positive = [min(nstall, nlim) for nstall, nlim in zip(n_stall, n_l_positive)]
n_limit_negative = [max(nstall, nlim) for nstall, nlim in zip(n_stall_negative, n_l_negative)]


# Plot the negative limit
fig.add_trace(go.Scatter(x=VE, y=n_limit_negative,
    fill=None,
    mode='lines',
    line_color='indigo', name="+nl",
    showlegend=False))

# Then a line of the structural failure that is filled to the structural damage
fig.add_trace(go.Scatter(
    x=VE,
    y=n_limit_positive,
    mode='lines',
    line_color='indigo',
    fill='tonexty', # fill area between structural failure and structural Damage
    fillcolor='rgba(0, 0, 255, 0.25)', name="Flight Envelope", showlegend=False))

fig.add_trace(go.Scatter(x=[Vd, Vd], y=[n_l[1], n_l[0]],
    fill=None,
    mode='lines',
    line_color='indigo',
    showlegend=False))

fig.update_xaxes(range= [0, 400])

# # Change the limits
# fig.update_yaxes(range= [1.2 * n_u[0], 1.2 * n_u[1]])

fig.update_layout(
    title="Representative Flight Envelope",
    xaxis_title="$EAS/m/s$",
    yaxis_title="Load Factor, $n$",
)

# # Dick around with the hover behaviour
# # fig.update_traces(hovertemplate=None)
# # fig.update_layout(hovermode="x unified")

# fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='black')
fig.show()

## Loops

In the following, _loops_ will be analysed using the definition of load factor and the basics of motion in a circle. If you can understand the forces during a loop, you can understand the forces during a general pull-up manoeuvre

If the pilot pulls back on the stick, provided there is sufficient thrust, the angle of attack will be increased and the lift will also increase. This increases the load factor.


### Constant Radius Loop

A 'perfect' *constant radius* loop is:
- Constant airspeed
- Constant radius

```{figure} ../Images/Loop.png
---
height: 300px
name: Loop
---
Constant Radius Loop
```
If the angular displacement is denoted by $\gamma$, with $\gamma=0$ being the bottom of the loop, increasing clockwise, then the equations of motion are, in the aircraft longitudinal direction
```{margin}
From motion in a circle, recall that centripetal (centre-seeking) acceleration is:

$a_c = \frac{V^2}{r}$

hence from Newton's second law, the force required to maintain a loop of radius $r$ is:

$F_c=\frac{m\,V^2}{r}$
```
$$T-D-W\sin\gamma=0$$

and

$$L - W\cos\gamma=\frac{W\,V^2}{g\,r}$$

So, at different points in the circle the equations of motion give, with $F_c = \frac{W\,V^2}{g\,r}$:

|         | Horizontal Equilibrium | Vertical Equilibrium |
|---------|------------------------|----------------------|
| Point A | $T-D=0$                | $L-W=F_c$            |
| Point B | $T-D-W=0$              | $L=F_c$              |
| Point C | $T-D=0$                | $L+W=F_c$            |
| Point D | $T-D+W=0$              | $L=F_c$              |

For the perfect loop, the normal acceleration is **constant**, and the load factor varies according to

$$n=\cos\gamma + \frac{V^2}{g\,r}$$

so at the different points of the loop above, the load factor is:

|         | Load Factor          |
|---------|----------------------|
| Point A | $1+\frac{V^2}{g\,r}$ |
| Point B | $\frac{V^2}{g\,r}$   |
| Point C | $\frac{V^2}{g\,r}-1$ |
| Point D | $\frac{V^2}{g\,r}$   |

Hence it is the load factor required to _initiate_ the loop that will set the minimum turn radius, and hence the minimimum turn radius is given by

$$r_{min}=\frac{V^2}{g\left(n-1\right)}$$

Hence the minimum value of the equation above will give the minimum radius for a constant radius loop. For the aircraft $V-n$ diagram already constructed, the ratio of this can be plotted

# Plot the minimum turn radius vs speed
g = 9.80665
n_limit_positive = np.array(n_limit_positive)
r_min = VE**2 / g / (n_limit_positive - 1)

# Find the minimum 
i_minimum = np.argmin(r_min)



minimum_turn_radius = r_min[i_minimum]
minimum_turn_speed = VE[i_minimum]

print(f"The minimum constant turn radius is {minimum_turn_radius:1.0f}m, which is at {minimum_turn_speed:1.0f}m/s EAS")

fig = go.Figure()

fig.add_trace(go.Scatter(x=VE, y=r_min,
    mode='lines',
    line_color='indigo', name="Turn Radius",
    showlegend=False))

fig.update_layout(
    title="Turn Radius vs EAS",
    xaxis_title="$EAS/m/s$",
    yaxis_title="Minimum turn radius $r_{min}$",
)

fig.update_yaxes(range= [0, 5e3])



```{admonition} What is the significance of the speed shown?
:class: dropdown
You should recognise that the speed for the minimum turn radius is the same as the manouvre speed.

At speeds below $V_A$, the turns are limited by the onset of stall.

At speeds above $V_A$, the turns are limited by strucutral limitations.

Note that in the above, no mention has been made of *thrust* available, which will also affect the turn radius.
```


For reasons that can be readily appreciated, the *lift* and the *thrust* must be continually varied to maintain constant $F_C$ required for a constant radius loop. 

For these reasons, your average loop looks something more like this - consider a loop with **constant load factor**.

### Constant Load Factor Loop

The equation for the load factor in a constant radius loop can be rearranged for the radius

$$r=\frac{V^2}{g\,\left(n-\cos\gamma\right)}$$

*radius*, here might be a little confusing since in the above it refers to the radius of a theoretical circle that would be flown if, at any point in the loop, the *instantaneous* value of the *pitching velocity* were maintained.

Effectively, this means that the distance flow during a given section of the loop is inversely proportional to the load factor - so the aircraft flies *further* during the parts where $\cos\gamma=0$ since $r$ is *larger* there. This means that the shape flow is elongated vertically to give a *tighter* turn at the top and bottom of the loop.



```{figure} ../Images/ConstantLoadFactorLoop.png
---
height: 300px
name: Loop
---
A loop with constant load factor and constant speed (representative, not to scale)
```

```{admonition} Think: why is the constant radius loop shaped like a balloon?
:class: dropdown

From motion in a circle, a tighter radius of turn $r$ can be effected by a greater $F_c$.

Without perfect input by the pilot, the weight vector will *add* to $F_C$ at the top of the loop, *subtract* from it at the bottom, and vary between according the equations of motion already shown.

If the pilot is unable to adjust attitude *perfectly*, it likely that the turn radius will be lowest at the bottom of the loop, and largest at the top - resulting the 'imperfect' shape shown.

```

You should be able to answer _qualitative_ questions about loops, and understand the radius at given points in a loop for different load factors, using the equations given.

The following code is included to help visualise the shape of a constant load factor loop. Run the code yourself - try and change the terms; maximium load factor, entry speed, and see the change to the loop shape.

# The following is inspired by the helpful page: http://understandingairplanes.com/Aerobatics-Analysis.pdf

# Set the limits here
n_max = 3 # Maxmimum load factor possible in loop
v_stall = 56 # Stall speed in kn
v_entry = 139 # Loop entry speed in kn
Va = 98 # Manoeuvre speed

# Choices
nG = 360 # Increments around the loop


# Angular vector for the loop
gamma = np.linspace(0, 2*np.pi, nG+1, endpoint=True)

# Step size
dG = np.mean(np.diff(gamma))

# Knots to ms
kn_to_ms = 0.5144444

# initialise the start speed
start_speed = v_entry

# Make some arrays to store position
X = np.zeros(nG+1) # Horizontal position
H = np.zeros(nG+1) # Altitude

X[0] = 0
H[0] = 0

for i in range(nG):
    # Get the start and end condition of the current segment
    start_angle = gamma[i]
    end_angle = gamma[i+1]
    
    # Approximated as a straight segment flown at the average angle between the start and the end
    segment_orientation = start_angle + 0.5 * dG
    
    # Assume the speed is constant at the start speed throughout the turn (see the link above for what affect this has)
    if start_speed >= Va:
        max_load_factor = n_max # If above manoeuvre speed, n = limit
    else:
        max_load_factor = (start_speed/v_stall)**2 # else, the turn is stall limited
    
    # Get the instantaneous turn radis
    r = (start_speed * kn_to_ms) ** 2 / g / (max_load_factor - np.cos(segment_orientation))
    dl = r * dG # Segment length
    
    
    # Get the horizontal and vertical displacement
    dX = dl * np.cos(segment_orientation)
    dH = dl * np.sin(segment_orientation)
    
    # Add these into arrays
    X[i + 1] = X[i] + dX
    H[i + 1] = H[i] + dH  

    # Get the change in speed from the interchange of GPE to KE (assumes constant thrust)
    end_speed = np.sqrt((start_speed*kn_to_ms)**2 + 2 * g * dH) / kn_to_ms
    dV = end_speed - start_speed
    
    # Update the speed
    start_speed = start_speed - dV


fig = go.Figure()

fig.add_trace(go.Scatter(x=X, y=H,
    mode='lines',
    line_color='indigo', name="Turn Radius",
    showlegend=False))

fig.update_layout(
    title="Constant Load Factor Loop",
    xaxis_title="Horizontal Displacement",
    yaxis_title="Vertical Displacment",
)


# fig.update_yaxes(range= [0, 5e3])

## Steady Turns

A steady turn is one for which there is no tangential acceleration:
- Circular motion in a horizontal plane
- Constant turn radius, $R$,
- Constant TAS

```{figure} ../Images/Turning_Main.png
---
height: 300px
name: Turning_Main
---
General Steady Turn
```

The aircraft will have an angular velocity, $\omega$, which can be determined from the flightspeed and turn radius

$$V=R\,\omega$$

The centripetal (centre-seeking) acceleration required to maintain the turn is 

$$\begin{align}
a_c&=R\,\omega^2\\
&=R\frac{V^2}{R^2}\\
&= \frac{V^2}{R}
\end{align}$$

and hence from Newton's second law, the associated force reqiured, $F_c$ is

$$F_c = m\cdot a_c = \frac{m\,V^2}{R}$$

This side force can be created in one of two ways:

### Flat Turns

In a flat turn, the rudder is utilised to create the side force with wings held level. This is not preferred, because:
- Very inefficient; small sideforce, and therefore large turn radius
- Drag increase due to fuselage sideslip; increased fuel burn
- Dynamic pressure imbalance on wings causes aileron adjustment to be required
- Perceieved centrifugal force by occupants
(sec:banked-turns)=
### Banked Turn

In a banked turn, the aircraft is rolled through angle $\phi$ so part of the lift provides the sideforce:

```{figure} ../Images/Turning_Banked.png
---
height: 300px
name: Turning_Banked
---
Banked Turn
```
In a banked turn, the lift is increased by the increment $\Delta L$, which can be related to the load factor

$$L+\Delta L = n\cdot W$$

$$L\cos\phi = W$$
$$\implies \cos\phi = n^{-1}$$

This can be related to required force

$$F_c = \frac{m\, V^2}{R} = L\cdot\sin\phi = n\cdot W\cdot\sin\phi$$
$$\frac{W\cdot V^2}{g\cdot R} = n\cdot W\cdot\sin\phi$$

The quantity $V^2/R$ can be represented in three useful formats

$$\begin{align}\frac{V^2}{R}&=g\cdot n\cdot\sin\phi\\
&= g\cdot\tan\phi\\
&= g\sqrt{n^2-1}\end{align}$$

or the turn radius can be represented independently of the velocity by substituting $L$ for $W$ and using the definition of the lift coefficient

$$R=\frac{2\,W}{g\,\rho\,S\,C_L\,\sin\phi}$$

Hence for a given speed:
- For constant $n$, turn radius is directly proportional to the square of flight speed
- For constant $V$, the turn radius is inversely proportional to the load factor

We can see the conditions that will minimise $R$:
- High density, therefore low altitude
- Low wing loading ($W/S$)
- High lift coefficient
- High bank angle

#### Turn Rate

The turn rate is the rate of change of heading, $\psi$

$$\omega = \frac{\text{d}\psi}{\text{d}t} = \frac{V}{R}$$

$$\omega = \frac{g\sqrt{n^2-1}}{V} = \frac{g\,\rho\,V\,C_L\,\sin\psi}{2\frac{W}{S}}$$

