from trail import *

def update(attr, old, new):
    global Zero,Pole  
    Zero = []
    Pole = []
    new_x_of_zeros =[]
    new_y_of_zeros = []
    new_x_of_poles =[]
    new_y_of_poles = []
    if conj_state == 0:
        for i in range(len(source_z.data['x_of_zeros'])):
            Zero.append(source_z.data['x_of_zeros'][i]+source_z.data['y_of_zeros'][i]*1j)        
            new_x_of_zeros.append(source_z.data['x_of_zeros'][i])
            new_y_of_zeros.append(source_z.data['y_of_zeros'][i]*-1)
        
        conjugate_zeros.data = dict(x_of_zeros_conjugate=new_x_of_zeros, y_of_zeros_conjugate=new_y_of_zeros)
        conjugate_zeros_renderer = system.circle(x="x_of_zeros_conjugate", y="y_of_zeros_conjugate", source=conjugate_zeros,color='red', size=10)

        for i in range(len(poles_source.data['x_of_poles'])):
            Pole.append(poles_source.data['x_of_poles'][i]+poles_source.data['y_of_poles'][i]*1j)
            new_x_of_poles.append(poles_source.data['x_of_poles'][i])
            new_y_of_poles.append(poles_source.data['y_of_poles'][i]*-1)
        
        conjugate_poles.data = dict(x_conj_p=new_x_of_poles, y_conj_p=new_y_of_poles)
        conjugate_poles_renderer = system.x(x="x_conj_p", y="y_conj_p", source=conjugate_poles,line_width=3, color='black', size=15)

    else:
        for i in range(len(source_z.data['x_of_zeros'])):
            Zero.append(source_z.data['x_of_zeros'][i]+source_z.data['y_of_zeros'][i]*1j)
        for i in range(len(poles_source.data['x_of_poles'])):
            Pole.append(poles_source.data['x_of_poles'][i]+poles_source.data['y_of_poles'][i]*1j)   

    magnitude_phase()


conj_state=1
def conjugate(status):
  
    global conj_state
    if status == [0]:   
        conj_state=0
    else:
        conj_state=1
  
def dropdown_filter( new):
    reset_filter()
    if new.item== "filter_1":
        k=[-0.9,0.45]
        p=[0.2,0.63]
        zeros_filter_source.stream({'x_of_zeros_filter': k, 'y_of_zeros_filter': p})
    elif new.item== "filter_2":
        k=[0.8,0.9]
        p=[0.7,0.2]
        zeros_filter_source.stream({'x_of_zeros_filter': k, 'y_of_zeros_filter': p})
    elif new.item== "filter_3":
        k=[-0.4,-0.6]
        p=[0.1,0.2]
        poles_filter_source.stream({'x_of_poles_filter': k, 'y_of_poles_filter': p})
    elif new.item== "filter_4":
        k=[-0.5,0.9]
        p=[0.1,0.4]
        poles_filter_source.stream({'x_of_poles_filter': k, 'y_of_poles_filter': p})
    elif new.item== "filter_5":
        k=[-0.22,0.9]
        p=[1.0,0.4]
        poles_filter_source.stream({'x_of_poles_filter': k, 'y_of_poles_filter': p})

def update_filter(attr, old, new):
    global Zero_filter,Pole_filter,Zero,Pole
    new_x_of_zeros=[]
    new_y_of_zeros=[]
    new_x_of_poles=[]
    new_y_of_poles=[]    
    Zero_filter = []
    Pole_filter = []

    for i in range(len(zeros_filter_source.data['x_of_zeros_filter'])):
        Zero_filter.append(zeros_filter_source.data['x_of_zeros_filter'][i]+zeros_filter_source.data['y_of_zeros_filter'][i]*1j)
        den= ((zeros_filter_source.data['x_of_zeros_filter'][i])**2)+((zeros_filter_source.data['y_of_zeros_filter'][i])**2)
        Pole_filter.append(((zeros_filter_source.data['x_of_zeros_filter'][i])/den)+ ((zeros_filter_source.data['y_of_zeros_filter'][i])/den)*1j)
        new_x_of_poles.append((zeros_filter_source.data['x_of_zeros_filter'][i])/den)
        new_y_of_poles.append((zeros_filter_source.data['y_of_zeros_filter'][i])/den)

    relative_poles.data = dict(x_of_poles_relative=new_x_of_poles, y_of_poles_relative=new_y_of_poles)
    
    
    for i in range(len(poles_filter_source.data['x_of_poles_filter'])):
        Pole_filter.append(poles_filter_source.data['x_of_poles_filter'][i]+poles_filter_source.data['y_of_poles_filter'][i]*1j)
        den= ((poles_filter_source.data['x_of_poles_filter'][i])**2)+((poles_filter_source.data['y_of_poles_filter'][i])**2)
        Zero_filter.append(((poles_filter_source.data['x_of_poles_filter'][i])/den)+ ((poles_filter_source.data['y_of_poles_filter'][i])/den)*1j)
        new_x_of_zeros.append((poles_filter_source.data['x_of_poles_filter'][i])/den)
        new_y_of_zeros.append((poles_filter_source.data['y_of_poles_filter'][i])/den)

    relative_zeros.data = dict(x_of_zeros_relative=new_x_of_zeros, y_of_zeros_relative=new_y_of_zeros)
    
    filter_phase()
    magnitude_phase()
    
def filter_phase():
    phase_filter_source.data={
    'x':[], 'y':[]
    }
    num, den=zpk2tf(Zero_filter,Pole_filter,1)
    w,h=freqz(num,den,worN=10000)
    phase=np.arctan(h.imag/h.real)
    phase_filter_source.stream({
        'x':w, 'y':phase
    })


def zero_or_pole(status):
    if status == 0:
        draw_tool = PointDrawTool(renderers=[zeros_render], empty_value='red')
    else:
        draw_tool = PointDrawTool(renderers=[poles_renderer], empty_value='black')
    system.add_tools(draw_tool)
    system.toolbar.active_tap = draw_tool

radio_group.on_click(zero_or_pole)

def zero_or_pole_filter(status):
    if status == 0:
        draw_tool1 = PointDrawTool(renderers=[zeros_filter_render], empty_value='red')
    else:
        draw_tool1 = PointDrawTool(renderers=[poles_filter_renderer], empty_value='black')
    filter.add_tools(draw_tool1)
    filter.toolbar.active_tap = draw_tool1

radio_group_filter.on_click(zero_or_pole_filter)

def reset():
   
    source_z.data = {k: [] for k in source_z.data}
    poles_source.data = {k: [] for k in poles_source.data}
    conjugate_poles.data = {k: [] for k in conjugate_poles.data}
    conjugate_zeros.data = {k: [] for k in conjugate_zeros.data}
reset_button.on_click(reset)

def clear_zeros():
   
    source_z.data = {k: [] for k in source_z.data}
clear_zeros_button.on_click(clear_zeros)


def clear_poles():    
    
    poles_source.data = {k: [] for k in poles_source.data}
clear_poles_button.on_click(clear_poles)





def reset_filter():
    
    zeros_filter_source.data = {k: [] for k in zeros_filter_source.data}
    poles_filter_source.data = {k: [] for k in poles_filter_source.data}
reset_button_filter.on_click(reset_filter)



def magnitude_phase():
    phase_source.data={
    'w':[], 'p':[]
    }

    magnitude_source.data={
    'h': [], 'm': []
    }
    Zero_plot=[]
    Pole_plot=[]
    Zero_plot.extend(Zero)
    Zero_plot.extend(Zero_filter)
    Pole_plot.extend(Pole)
    Pole_plot.extend(Pole_filter)
    num, den=zpk2tf(Zero_plot,Pole_plot,1)
    w,h=freqz(num,den,worN=10000)
    num1, den1=zpk2tf(Zero,Pole,1)
    w1,h1=freqz(num1,den1,worN=10000)
    magnitude1=np.sqrt(h1.real**2+h1.imag**2)
    phase=np.arctan(h.imag/h.real)
    magnitude_source.stream({
    'h': w1, 'm': magnitude1
    })
    phase_source.stream({
        'w':w, 'p':phase
    })


source_z.on_change('data',update)
poles_source.on_change('data',update)
dropdown.on_click(dropdown_filter)
zeros_filter_source.on_change('data',update_filter)
poles_filter_source.on_change('data',update_filter)
reset_button.js_on_click(CustomJS(code="console.log('button: click!', this.toString())"))
clear_zeros_button.js_on_click(CustomJS(code="console.log('button: click!', this.toString())"))
clear_poles_button.js_on_click(CustomJS(code="console.log('button: click!', this.toString())"))
reset_button_filter.js_on_click(CustomJS(code="console.log('button: click!', this.toString())"))
dropdown.js_on_event("menu_item_click", CustomJS(code="console.log('dropdown: ' + this.item, this.toString())"))
radio_group.js_on_click(CustomJS(code="""
    console.log('radio_group: active=' + this.active, this.toString())
"""))
checkbox_group.js_on_click(CustomJS(code="""
    console.log('checkbox_group: active=' + this.active, this.toString())
"""))
radio_group_filter.js_on_click(CustomJS(code="""
    console.log('radio_group_filter: active=' + this.active, this.toString())
"""))
checkbox_group.on_click(conjugate)

radio_button_group=Row(clear_zeros_button,clear_poles_button)
filter_buttons=Row(reset_button_filter,dropdown)
first_column= column(system,filter)
second_column=column(radio_group,checkbox_group,radio_button_group,reset_button,zeros_table,poles_table,radio_group_filter,filter_buttons)
third_column=column(magnitude,phase,phase_filter)
curdoc().add_root(Row(first_column,second_column,third_column))
