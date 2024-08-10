from video_program import df

from bokeh.plotting import figure, show, output_file

p = figure(x_axis_type = 'datetime', height = 150, sizing_mode = "scale_width", title = "Motion Graph")
p.title.text_font_size = '32px'  
p.title.align = 'center'
p.title.text_font = 'times'

p.yaxis.minor_tick_line_color = None
p.ygrid.ticker = [0,1]
q = p.quad(left=df["Start"], right=df["End"], bottom=0, top=1, color = "#ff8ab5")

output_file("Graph.html")
show(p)
