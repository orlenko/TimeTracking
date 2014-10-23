from collect import get_data
from graph import mkgraph
from subprocess import call


mkgraph(list(get_data()), 'graph.png')
call(['xloadimage', '-onroot', 'graph.png'])
