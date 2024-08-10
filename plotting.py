from video_program import df

from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds=ColumnDataSource(df)

p = figure(x_axis_type = 'datetime', height = 150, sizing_mode = "scale_width", title = "Motion Graph")
p.title.text_font_size = '32px'  
p.title.align = 'center'
p.title.text_font = 'times'

p.yaxis.minor_tick_line_color = None
p.ygrid.ticker = [0,1]

hoover = HoverTool(tooltips=[("Start ", "@Start_string"), ("End ", "@End_string")])
p.add_tools(hoover)

q = p.quad(left="Start", right="End", bottom=0, top=1, color = "#ff8ab5", source = cds)

output_file("Graph.html")
show(p)
