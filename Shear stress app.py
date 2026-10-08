import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def plot_rectangle(b, h, F, I):
    y = np.linspace(0, h, 500)
    tau = (6*F/(b*h**3)) * (h*y - y**2) 
    fig, ax = plt.subplots(figsize=(4,6))
    ax.plot(tau, y, linewidth=2)
    ax.fill_betweenx(y, tau, alpha=0.2)
    ax.axhline(h/2, color='red', linestyle='--', label='N.A')
    ax.set_xlabel('Shear Stress (N/mm2)')
    ax.set_ylabel('Height from bottom (mm)')
    ax.set_title(f'Rectangle - Max at N.A = {max(tau):.2f} N/mm2')
    ax.legend()
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    st.write(f"Max Tau at N.A = {max(tau):.3f} N/mm2")

def plot_T_section(Fb, Fh, Wb, Wh, F, I, y_from_bottom, yf, yw):
    H = Fh+Wh
    Af = Fb*Fh
    y_vals = np.linspace(0, H, 800)
    tau_vals = []
    for y in y_vals:
        if y <= Wh: 
            Q = Af*(yf - y_from_bottom) + Wb*(Wh - y)*(((y+Wh)/2) - y_from_bottom)
            b = Wb
        else: 
            h_ab = H - y
            Q = Fb*h_ab*(y + h_ab/2 - y_from_bottom)
            b = Fb
        tau_vals.append(max(F*Q/(I*b),0))
    fig, ax = plt.subplots(figsize=(4,6))
    ax.plot(tau_vals, y_vals, linewidth=2)
    ax.fill_betweenx(y_vals, tau_vals, alpha=0.2)
    ax.axhline(y_from_bottom, color='red', linestyle='--', label=f'N.A y={y_from_bottom:.2f}')
    ax.axhline(Wh, color='gray', linestyle=':', label='Flange-Web')
    ax.set_xlabel('Shear Stress (N/mm2)')
    ax.set_ylabel('Height from bottom (mm)')
    ax.set_title(f'T-Section - Max at N.A = {max(tau_vals):.2f} N/mm2')
    ax.legend(fontsize=7)
    ax.grid(alpha=0.3)
    st.pyplot(fig)

def plot_I_section(Fb, Fh, Wb, Wh, F, I, y_from_bottom):
    H = 2*Fh+Wh
    Af = Fb*Fh
    Aw = Wb*Wh
    y_vals = np.linspace(0, H, 800)
    tau_vals = []
    for y in y_vals:
        if y < Fh: 
            h_rem = Fh - y
            Q = Af*((Fh+Wh+Fh/2)-y_from_bottom) + Aw*((Fh+Wh/2)-y_from_bottom) + Fb*h_rem*((y+Fh)/2 - y_from_bottom)
            b = Fb
        elif y < Fh+Wh: 
            h_web_above = Fh+Wh - y
            Q = Af*((Fh+Wh+Fh/2)-y_from_bottom) + Wb*h_web_above*(y + h_web_above/2 - y_from_bottom)
            b = Wb
        else: 
            h_top = H - y
            Q = Fb*h_top*(y + h_top/2 - y_from_bottom)
            b = Fb
        tau_vals.append(max(F*Q/(I*b),0))
    fig, ax = plt.subplots(figsize=(4,6))
    ax.plot(tau_vals, y_vals, linewidth=2)
    ax.fill_betweenx(y_vals, tau_vals, alpha=0.2)
    ax.axhline(y_from_bottom, color='red', linestyle='--', label='N.A')
    ax.set_xlabel('Shear Stress (N/mm2)')
    ax.set_ylabel('Height from bottom (mm)')
    ax.set_title(f'I-Section - Max at N.A = {max(tau_vals):.2f} N/mm2')
    ax.legend()
    ax.grid(alpha=0.3)
    st.pyplot(fig)

def plot_I_section_unequal(Fb1, Fh1, Fb2, Fh2, Wb, Wh, F, I, y_from_bottom):
    H = Fh1+Wh+Fh2
    Af1 = Fb1*Fh1
    Af2 = Fb2*Fh2
    Aw = Wb*Wh
    y_vals = np.linspace(0, H, 800)
    tau_vals = []
    for y in y_vals:
        if y < Fh1:
            h_rem = Fh1 - y
            Q = Af2*((Fh1+Wh+Fh2/2)-y_from_bottom) + Aw*((Fh1+Wh/2)-y_from_bottom) + Fb1*h_rem*((y+Fh1)/2 - y_from_bottom)
            b = Fb1
        elif y < Fh1+Wh:
            h_web_above = Fh1+Wh - y
            Q = Af2*((Fh1+Wh+Fh2/2)-y_from_bottom) + Wb*h_web_above*(y + h_web_above/2 - y_from_bottom)
            b = Wb
        else:
            h_top = H - y
            Q = Fb2*h_top*(y + h_top/2 - y_from_bottom)
            b = Fb2
        tau_vals.append(max(F*Q/(I*b),0))
    fig, ax = plt.subplots(figsize=(4,6))
    ax.plot(tau_vals, y_vals, linewidth=2)
    ax.fill_betweenx(y_vals, tau_vals, alpha=0.2)
    ax.axhline(y_from_bottom, color='red', linestyle='--', label=f'N.A y={y_from_bottom:.2f}')
    ax.axhline(Fh1, color='gray', linestyle=':', label='Bottom Flange-Web')
    ax.axhline(Fh1+Wh, color='gray', linestyle=':', label='Top Flange-Web')
    ax.set_xlabel('Shear Stress (N/mm2)')
    ax.set_ylabel('Height from bottom (mm)')
    ax.set_title(f'I-Section Unequal - Max at N.A = {max(tau_vals):.2f} N/mm2')
    ax.legend(fontsize=7)
    ax.grid(alpha=0.3)
    st.pyplot(fig)

def rectangle():
    st.subheader("Rectangle")
    b=st.number_input("Enter width in mm:", value=None, placeholder="Enter width in mm", key="b_rect")
    h=st.number_input("Enter depth in mm:", value=None, placeholder="Enter depth in mm", key="h_rect")
    F_KN=st.number_input("Enter force in KN:", value=None, placeholder="Enter force in KN", key="F_rect")
    if st.button("Calculate Rectangle"):
        if b is None or h is None or F_KN is None:
            st.error("Please enter all values")
        else:
            F=F_KN*1000
            st.write(f"F = {F_KN}KN = {F}N")
            A=b*h
            st.write(f"A=b*h => A={b}*{h} => {A:.3f}mm^2")
            y=h/2
            st.write(f"y=h/2 => y={h}/2 => {y:.3f}mm")
            I=(b*h**3)/12
            st.write(f"I=b*h^3/12 =>  I={b}*{h}^3 => {I:.3f}mm^4")
            Tau=(F*A*y)/(I*b)
            st.write(f"Tau=(F*A*y)/(I*b) => Tau=({F}*{A}*{y})/({I}*{b}) => {Tau:.3f}N/mm^2")
            plot_rectangle(b, h, F, I)

def T_section():
    st.subheader("T Section")
    Fb=st.number_input("Enter width of flange in mm:", value=None, placeholder="Enter width of flange", key="Fb_T")
    Fh=st.number_input("Enter depth of flange in mm:", value=None, placeholder="Enter depth of flange", key="Fh_T")
    Wb=st.number_input("Enter width of web in mm:", value=None, placeholder="Enter width of web", key="Wb_T")
    Wh=st.number_input("Enter depth of web in mm:", value=None, placeholder="Enter depth of web", key="Wh_T")
    F_KN=st.number_input("Enter force in KN:", value=None, placeholder="Enter force in KN", key="F_T")
    if st.button("Calculate T Section"):
        if None in (Fb, Fh, Wb, Wh, F_KN):
            st.error("Please enter all values")
        else:
            F=F_KN*1000
            st.write(f"F = {F_KN}KN = {F}N")
            Af=Fb*Fh
            st.write(f"Af=Fb*Fh => Af={Fb}*{Fh} => {Af:.3f}mm^2")
            Aw=Wb*Wh
            st.write(f"Aw=Wb*Wh => A={Wb}*{Wh} => {Aw:.3f}mm^2")
            yw=Wh/2
            st.write(f"yw=Wh/2 => yw={Wh}/2 => {yw:.3f}mm")
            yf=Wh+Fh/2
            st.write(f"yw=Wh+(Fh/2) => yf={Wh}+({Fh}/2) => {yf:.3f}mm")
            y_from_bottom=((Af*yf)+(Aw*yw))/(Af+Aw)
            st.write(f"y_from_bottom=((Af*yf)+(Aw*yw))/(Af+Aw) => y_from_bottom=(({Af}*{yf})+({Aw}*{yw}))/({Af}+{Aw}) =>{y_from_bottom:.3f}mm")
            If=Fb*Fh**3/12+(Af*(y_from_bottom-yf)**2)
            st.write(f"If=Fb*Fh**3/12+(Af*(y_from_bottom-yf)**2) => If={Fb}*{Fh}**3/12+({Af}*({y_from_bottom}-{yf})**2) =>{If:.3f}mm^4")
            Iw=Wb*Wh**3/12+(Aw*(y_from_bottom-yw)**2)
            st.write(f"Iw=Wb*Wh**3/12+(Af*(y_from_bottom-yw)**2) => Iw={Wb}*{Wh}**3/12+({Aw}*({y_from_bottom}-{yw})**2) =>{Iw:.3f}mm^4")
            I=If+Iw
            st.write(f"I=If+Iw => I={If}+{Iw} => {I:.3f}mm^4")
            H_Total=Fh+Wh
            y_from_top=H_Total-y_from_bottom
            y1=y_from_top-(Fh/2)
            y2=(y_from_top-Fh)/2
            A1=Fh*Fb
            A2=Wb*y2*2
            Ay_bar=(A1*y1)+(A2*y2)
            st.write(f"Ay_bar=(A1*y1)+(A2*y2) => Ay_bar=({A1}*{y1})+({A2}*{y2}) => {Ay_bar:.3f}mm^3")
            Tau=(F*Ay_bar)/(I*Wb)
            st.write(f"Tau=(F*Ay_bar)/(I*Wb) => Tau=({F}*{Ay_bar})/({I}*{Wb}) =>{Tau:.3f}N/mm^2")
            plot_T_section(Fb,Fh,Wb,Wh,F,I,y_from_bottom,yf,yw)

def I_section_equalflanges():
    st.subheader("I Section (Equal Flanges)")
    Fb1=st.number_input("Enter width of flange in mm:", value=None, placeholder="Enter flange width", key="Fb1_eq")
    Fh1=st.number_input("Enter depth of flange in mm:", value=None, placeholder="Enter flange depth", key="Fh1_eq")
    Wb=st.number_input("Enter width of web in mm:", value=None, placeholder="Enter web width", key="Wb_eq")
    Wh=st.number_input("Enter depth of web in mm:", value=None, placeholder="Enter web depth", key="Wh_eq")
    F_KN=st.number_input("Enter force in KN:", value=None, placeholder="Enter force in KN", key="F_eq")
    if st.button("Calculate I Equal"):
        if None in (Fb1, Fh1, Wb, Wh, F_KN):
            st.error("Please enter all values")
        else:
            Fb2=Fb1
            Fh2=Fh1
            F=F_KN*1000
            st.write(f"F = {F_KN}KN = {F}N")
            Af1=Fb1*Fh1
            Af2=Fb2*Fh2
            st.write(f"Af1=Fb1*Fh1 => Af1={Fb1}*{Fh1} => {Af1:.3f}mm^2")
            st.write(f"Af2=Fb2*Fh2 => Af2={Fb2}*{Fh2} => {Af2:.3f}mm^2")
            Aw=Wb*Wh
            st.write(f"Aw=Wb*Wh => A={Wb}*{Wh} => {Aw:.3f}mm^2")
            yw=Fh1+(Wh/2)
            st.write(f"yw=Fh1+(Wh/2) => yw={Fh1}+({Wh}/2) => {yw:.3f}mm")
            yf1=Fh1/2
            st.write(f"yf1=Fh1/2 => yf1={Fh1}/2 => {yf1:.3f}mm")
            yf2=Fh1+Wh+(Fh2/2)
            st.write(f"yf2=Fh1+Wh+(Fh2/2) => yf2={Fh1}+{Wh}+({Fh2}/2) => {yf2:.3f}mm")
            y_from_bottom=((Af1*yf1)+(Af2*yf2)+(Aw*yw))/(Af1+Af2+Aw)
            st.write(f"y_from_bottom=((Af1*yf1)+(Af2*yf2)+(Aw*yw))/(Af1+Af2+Aw) => y_from_bottom=(({Af1}*{yf1})+({Af2}*{yf2})+({Aw}*{yw}))/({Af1}+{Af2}+{Aw}) =>{y_from_bottom:.3f}mm")
            If1=Fb1*Fh1**3/12+(Af1*(y_from_bottom-yf1)**2)
            st.write(f"If1=Fb1*Fh1**3/12+(Af1*(y_from_bottom-yf1)**2) => If1={Fb1}*{Fh1}**3/12+({Af1}*({y_from_bottom}-{yf1})**2) =>{If1:.3f}mm^4")
            If2=Fb2*Fh2**3/12+(Af2*(y_from_bottom-yf2)**2)
            st.write(f"If2=Fb2*Fh2**3/12+(Af2*(y_from_bottom-yf2)**2) => If2={Fb2}*{Fh2}**3/12+({Af2}*({y_from_bottom}-{yf2})**2) =>{If2:.3f}mm^4")
            Iw=Wb*Wh**3/12+(Aw*(y_from_bottom-yw)**2)
            st.write(f"Iw=Wb*Wh**3/12+(Af*(y_from_bottom-yw)**2) => Iw={Wb}*{Wh}**3/12+({Aw}*({y_from_bottom}-{yw})**2) =>{Iw:.3f}mm^4")
            I=If1+If2+Iw
            st.write(f"I=If1+If2+Iw => I={If1}+{If2}+{Iw} => {I:.3f}mm^4")
            H_Total=Fh1+Fh2+Wh
            y_from_top=H_Total-y_from_bottom
            y1=y_from_top-(Fh2/2)
            y2=(y_from_top-Fh2)/2
            A1=Fh2*Fb2
            A2=Wb*y2*2
            Ay_bar=(A1*y1)+(A2*y2)
            st.write(f"Ay_bar=(A1*y1)+(A2*y2) => Ay_bar=({A1}*{y1})+({A2}*{y2}) => {Ay_bar:.3f}mm^3")
            Tau=(F*Ay_bar)/(I*Wb)
            st.write(f"Tau=(F*Ay_bar)/(I*Wb) => Tau=({F}*{Ay_bar})/({I}*{Wb}) =>{Tau:.3f}N/mm^2")
            plot_I_section(Fb1,Fh1,Wb,Wh,F,I,y_from_bottom)

def I_section_unequalflanges():
    st.subheader("I Section (Unequal Flanges)")
    Fb1=st.number_input("Enter width of bottom flange in mm:", value=None, placeholder="Bottom flange width", key="Fb1_uneq")
    Fh1=st.number_input("Enter depth of bottom flange in mm:", value=None, placeholder="Bottom flange depth", key="Fh1_uneq")
    Fb2=st.number_input("Enter width of top flange in mm:", value=None, placeholder="Top flange width", key="Fb2_uneq")
    Fh2=st.number_input("Enter depth of top flange in mm:", value=None, placeholder="Top flange depth", key="Fh2_uneq")
    Wb=st.number_input("Enter width of web in mm:", value=None, placeholder="Web width", key="Wb_uneq")
    Wh=st.number_input("Enter depth of web in mm:", value=None, placeholder="Web depth", key="Wh_uneq")
    F_KN=st.number_input("Enter force in KN:", value=None, placeholder="Force in KN", key="F_uneq")
    if st.button("Calculate I Unequal"):
        if None in (Fb1, Fh1, Fb2, Fh2, Wb, Wh, F_KN):
            st.error("Please enter all values")
        else:
            F=F_KN*1000
            st.write(f"F = {F_KN}KN = {F}N")
            Af1=Fb1*Fh1
            Af2=Fb2*Fh2
            st.write(f"Af1=Fb1*Fh1 => Af1={Fb1}*{Fh1} => {Af1:.3f}mm^2")
            st.write(f"Af2=Fb2*Fh2 => Af2={Fb2}*{Fh2} => {Af2:.3f}mm^2")
            Aw=Wb*Wh
            st.write(f"Aw=Wb*Wh => A={Wb}*{Wh} => {Aw:.3f}mm^2")
            yw=Fh1+(Wh/2)
            st.write(f"yw=Fh1+(Wh/2) => yw={Fh1}+({Wh}/2) => {yw:.3f}mm")
            yf1=Fh1/2
            st.write(f"yf1=Fh1/2 => yf1={Fh1}/2 => {yf1:.3f}mm")
            yf2=Fh1+Wh+(Fh2/2)
            st.write(f"yf2=Fh1+Wh+(Fh2/2) => yf2={Fh1}+{Wh}+({Fh2}/2) => {yf2:.3f}mm")
            y_from_bottom=((Af1*yf1)+(Af2*yf2)+(Aw*yw))/(Af1+Af2+Aw)
            st.write(f"y_from_bottom=((Af1*yf1)+(Af2*yf2)+(Aw*yw))/(Af1+Af2+Aw) => y_from_bottom=(({Af1}*{yf1})+({Af2}*{yf2})+({Aw}*{yw}))/({Af1}+{Af2}+{Aw}) =>{y_from_bottom:.3f}mm")
            If1=Fb1*Fh1**3/12+(Af1*(y_from_bottom-yf1)**2)
            st.write(f"If1=Fb1*Fh1**3/12+(Af1*(y_from_bottom-yf1)**2) => If1={Fb1}*{Fh1}**3/12+({Af1}*({y_from_bottom}-{yf1})**2) =>{If1:.3f}mm^4")
            If2=Fb2*Fh2**3/12+(Af2*(y_from_bottom-yf2)**2)
            st.write(f"If2=Fb2*Fh2**3/12+(Af2*(y_from_bottom-yf2)**2) => If2={Fb2}*{Fh2}**3/12+({Af2}*({y_from_bottom}-{yf2})**2) =>{If2:.3f}mm^4")
            Iw=Wb*Wh**3/12+(Aw*(y_from_bottom-yw)**2)
            st.write(f"Iw=Wb*Wh**3/12+(Af*(y_from_bottom-yw)**2) => Iw={Wb}*{Wh}**3/12+({Aw}*({y_from_bottom}-{yw})**2) =>{Iw:.3f}mm^4")
            I=If1+If2+Iw
            st.write(f"I=If1+If2+Iw => I={If1}+{If2}+{Iw} => {I:.3f}mm^4")
            H_Total=Fh1+Fh2+Wh
            y_from_top=H_Total-y_from_bottom
            y1=y_from_top-(Fh2/2)
            y2=(y_from_top-Fh2)/2
            A1=Fh2*Fb2
            A2=Wb*y2*2
            Ay_bar=(A1*y1)+(A2*y2)
            st.write(f"Ay_bar=(A1*y1)+(A2*y2) => Ay_bar=({A1}*{y1})+({A2}*{y2}) => {Ay_bar:.3f}mm^3")
            Tau=(F*Ay_bar)/(I*Wb)
            st.write(f"Tau=(F*Ay_bar)/(I*Wb) => Tau=({F}*{Ay_bar})/({I}*{Wb}) =>{Tau:.3f}N/mm^2")
            plot_I_section_unequal(Fb1,Fh1,Fb2,Fh2,Wb,Wh,F,I,y_from_bottom)

st.title("------Shear Stress Calculator------")
ch=st.sidebar.selectbox("Enter choice", ["Rectangle", "T Section", "I Section(with equal flanges)", "I Section(with unequal flanges)"])
if ch=='Rectangle':
    rectangle()
elif ch=='T Section':
    T_section()
elif ch=='I Section(with equal flanges)':
    I_section_equalflanges()
elif ch=='I Section(with unequal flanges)':
    I_section_unequalflanges()