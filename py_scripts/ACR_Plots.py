from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from py_scripts import DB_Connection

import plotly.graph_objs as go
import math

### Plotly Functions

def PLOTLY_BAR_PLOT(x,y, ax_type="-", title="", x_label="", y_label=""):
	trace = go.Bar(
		x=x,
		y=y,
		marker=dict(color='rgb(255,166,0)')
	)

	data = [trace]
	layout = go.Layout(
		title=title,
		xaxis=dict(title=x_label, 
			type=ax_type, 
			tickformat='%Y-%b'),
		yaxis=dict(title=y_label)
	)

	fig = go.Figure(data=data, layout=layout)
	return plot(fig, include_plotlyjs=False, output_type='div')

def PLOTLY_BAR_PLOT_2YAXIS(x,y1,y2, y1_name='', y2_name='', title="", x_label="", y1_label="", y2_label=""):
	trace1 = go.Bar(
		x=x,
		y=y1,
		name=y1_name,
		marker=dict(color='rgb(47,75,124)')
	)

	trace2 = go.Scatter(
		x=x,
		y=y2,
		name=y2_name,
		yaxis = 'y2',
		marker=dict(color='rgb(188, 80, 144)')
	)

	data = [trace1, trace2]
	layout = go.Layout(
		title=title,
		xaxis=dict(title=x_label, type='category'),
		yaxis=dict(title=y1_label),
		yaxis2=dict(title=y2_label,
					range=[0,100],
					tickfont=dict(color='rgb(188, 80, 144)'),
					overlaying='y',
					side='right')
	)

	fig = go.Figure(data=data, layout=layout)
	return plot(fig, include_plotlyjs=False, output_type='div')

def PLOTLY_LINE_PLOT(x,y, ax_type="-", title="", x_label="", y_label=""):
	trace = go.Scatter(
		x=x,
		y=y,
		mode = "lines+markers")

	layout = go.Layout(
		title=title,
		xaxis=dict(title=x_label, type=ax_type, range=[0,round(max(x)*1.01)]),
		yaxis=dict(title=y_label)
	)

	data = [trace]
	fig = go.Figure(data=data, layout=layout)
	return plot(fig, include_plotlyjs=False, output_type='div')

def PLOTLY_SPIDER_PLOT(values, axes, chart_range, title=""):
	data = [go.Scatterpolar(
	  r = values,
	  theta = axes,
	  fill = 'toself'
	)]

	layout = go.Layout(
	title=title,
	polar = dict(
		radialaxis = dict(
		  visible = True,
		  range = chart_range
		)
	  ),
	  showlegend = False
	)

	fig = go.Figure(data=data, layout=layout)
	return plot(fig, include_plotlyjs=False, output_type='div')

def PLOTLY_HISTOGRAM_PLOT(x, title="", x_label="", y_label=""):
	data = [
		go.Histogram(
		x = x,
		histnorm="percent",
		xbins = dict(
			end=1600, 
		    size=50, 
		    start=0)
		)
	]

	layout = go.Layout(
		title=title,
		xaxis=dict(title=x_label, range=[0,1600]),
		yaxis=dict(title=y_label)
	)

	fig = go.Figure(data=data, layout=layout)
	return plot(fig, include_plotlyjs=False, output_type='div')

def PLOTLY_PIE_CHART(labels, values, title=""):
	trace = go.Pie(labels=labels, values=values)
	data = [trace]
	
	layout = go.Layout(
		title=title
	)

	fig = go.Figure(data=data, layout=layout)

	return plot(fig, include_plotlyjs=False, output_type='div')

###  DB Queries

# Done
def GRAPH_ELO_DISTRIBUTION(items):
	db = DB_Connection.database()
	x = []
	
	for row in db.query("""SELECT elo_global FROM {}""".format('user_scores' if items=='Usuarios' else 'problem_scores'), fetchall=True):
		x.append(row[0]*100)

	db.close()
	return PLOTLY_HISTOGRAM_PLOT(x, title="Distribución de Puntuación ELO de los {} de ACR".format(items),
	 x_label="Puntuación ELO", y_label="% de {}".format(items))

# Done
def GRAPH_TRIES_AVERAGE():
	db = DB_Connection.database()

	num_subm = {}
	for i in range(1,21): 
		num_subm[str(i)] = 0
	num_subm['+ de 20'] = 0

	rows = db.query("""SELECT user_id, problem_id, SUM(CASE 
		WHEN status = 'AC' THEN 1 
		WHEN status = 'PE' THEN 1 
		ELSE 0 END), COUNT(id) 
		FROM submission 
		GROUP BY user_id, problem_id""", fetchall=True)

	for row in rows:
		if row[2] != 0:
			if row[3] < 21:  
				num_subm[str(row[3])] += 1
			else: 
				num_subm['+ de 20'] += 1

	x = list(num_subm.keys())
	total_sum = sum(num_subm.values())
	
	y1 = [(i/total_sum)*100 for i in num_subm.values()]
	y2 = [sum(y1[:i+1]) for i in range(len(y1))]

	db.close()
	return PLOTLY_BAR_PLOT_2YAXIS(x,y1,y2, title="% de Usuarios que han necesitado X intentos para resolver un problema", 
		x_label="Nº de Intentos", y1_label="% de Alumnos", y1_name="% de Alumnos", y2_name="% Acumulado de Alumnos")

# Done
def TRIES_PER_PROBLEM(problem_id):
	db = DB_Connection.database()
	
	num_subm = {}
	for i in range(1,21): num_subm[str(i)] = 0
	num_subm['+ de 20'] = 0

	rows = db.query("""SELECT user_id, problem_id, SUM(CASE 
		WHEN status = 'AC' THEN 1 
		WHEN status = 'PE' THEN 1 
		ELSE 0 END), COUNT(id) 
		FROM submission
		WHERE problem_id = {}
		GROUP BY user_id, problem_id""".format(problem_id), fetchall=True)

	for row in rows:
		if row[2] != 0:
			if row[3] < 21:  
				num_subm[str(row[3])] += 1
			else: 
				num_subm['+ de 20'] += 1

	total_sum = sum(num_subm.values())
	total_sum = total_sum if total_sum != 0 else 1

	x = list(num_subm.keys())
	y = [(val/total_sum)*100 for val in num_subm.values()]

	db.close()
	return PLOTLY_BAR_PLOT(x, y, x_label="Nº de Intentos", y_label="% de Alumnos", 
		ax_type='category', title="% de Usuarios que han necesitado X intentos para resolver este problema",)

# Done
def GRAPH_SUBMISSIONS_PER_MONTHS():
	db = DB_Connection.database()
	
	x = []
	y = []
	
	for r in db.query("SELECT DATE_FORMAT(submissionDate, '%Y-%m'), COUNT(id) FROM submission GROUP BY  DATE_FORMAT(submissionDate, '%Y-%m') ORDER BY submissionDate ASC", fetchall=True):
		x.append(r[0])
		y.append(r[1])

	db.close()
	return PLOTLY_BAR_PLOT(x,y, ax_type='date', title="Envios por Mes", y_label="Nº de Envios", x_label="Fecha")

# Done
def GRAPH_USERS_EVOLUTION(user_id):
	db = DB_Connection.database()

	rows = db.query("""SELECT user_elo FROM submission 
	WHERE user_id = {}
	AND user_elo IS NOT NULL 
	ORDER BY id""".format(user_id), fetchall=True)
	
	y = [round(x[0]*100) for x in rows]
	y.insert(0,800)

	latest_elo = round(db.query("SELECT elo_global FROM user_scores WHERE user_id = {}".format(user_id), fetchone=True)[0]*100)
	if y[-1] != latest_elo:
		y.append(latest_elo)

	db.close()
	return PLOTLY_LINE_PLOT([x for x in range(len(y))], y, title="Evolución de tu Puntuación ELO", x_label="", y_label="Puntuación ELO")

# Done
def GRAPH_PROBLEMS_EVOLUTION(problem_id):
	db = DB_Connection.database()
	rows = db.query("""SELECT problem_elo FROM submission 
		WHERE problem_id = {}
		AND problem_elo IS NOT NULL 
		ORDER BY id""".format(problem_id), fetchall=True)

	y = [round(x[0]*100) for x in rows]
	y.insert(0,800)

	latest_elo = round(db.query("SELECT elo_global FROM problem_scores WHERE problem_id = {}".format(problem_id), fetchone=True)[0]*100)
	if y[-1] != latest_elo:
		y.append(latest_elo)

	db.close()
	return PLOTLY_LINE_PLOT([x for x in range(len(y))], y, title="Evolución de la Puntuación ELO del Problema", x_label="", y_label="Puntuación ELO")

# Done
def GRAPH_USER_CATEGORIES(user_id):
	db = DB_Connection.database()
	row = db.query("""SELECT * FROM user_scores WHERE user_id = {}""".format(user_id), fetchone=True)
	
	values = [round(i*100) for i in row[2:]]
	values.append(values[0])
	
	axes = ['Ad-hoc', 'Recorridos', 'Busqueda', 'Busqueda Binaria', 'Ordenacion', 'Algoritmos voraces','Programacion dinamica',
	'Divide y venceras','Busqueda exhaustiva, vuelta atras','Busqueda en el espacio de soluciones','Grafos','Geometria','Ad-hoc']
	
	db.close()
	return PLOTLY_SPIDER_PLOT(values, axes, [0,1600], title="ELO por Categoria")

# Done
def GRAPH_USER_PROBLEM_PROGRESS(user_id):
	db = DB_Connection.database()
	
	values = []

	# if user new (no submissions)
	if db.query("SELECT COUNT(*) FROM submission WHERE user_id = {}".format(user_id), fetchone=True)[0] != 0:

		# Problems solved by the user
		val = db.query("""SELECT user_id, SUM(CASE 
			WHEN status = 'AC' THEN 1 
			WHEN status = 'PE' THEN 1 
			ELSE 0 END) FROM submission 
			WHERE user_id = {}
			GROUP BY user_id""".format(user_id), fetchone=True)

		values.append(val[1])

		# Problems tried by the user
		val = db.query("""SELECT user_id, COUNT(DISTINCT(problem_id)) FROM submission 
			WHERE user_id = {}
			GROUP BY user_id""".format(user_id), fetchone=True)
		
		values.append(val[1] - values[0])

	else:
		values = [0,0]


	# Number of problems
	val = db.query("""SELECT COUNT(*) FROM problem_scores""", fetchone=True)

	values.append(val[0] - sum(values))

	labels=['Resueltos', 'Intentados, sin resolver', 'Por Hacer']

	db.close()
	return PLOTLY_PIE_CHART(labels, values, title="Progreso de Problemas")

	# Done

# Done
def GRAPH_PROBLEM_SOLVE_RATIO(problem_id):
	db = DB_Connection.database()
	
	if db.query("SELECT COUNT(*) FROM submission WHERE problem_id = {}".format(problem_id), fetchone=True)[0] != 0:

		user_who_solved_it = db.query("""SELECT COUNT(DISTINCT(user_id)) FROM submission 
			WHERE problem_id = {}
			AND (status = 'AC' OR status = 'PE')""".format(problem_id), fetchone=True)[0]

		user_who_havent_solved_yet = db.query("""SELECT COUNT(DISTINCT(user_id)) FROM submission 
			WHERE problem_id = {}
			AND (status != 'AC' AND status != 'PE')
			AND user_id NOT IN (
				SELECT user_id FROM submission 
				WHERE problem_id = {}
				AND (status = 'AC' OR status = 'PE')
			)""".format(problem_id, problem_id), fetchone=True)[0]

		values = [user_who_solved_it, user_who_havent_solved_yet]
		labels = ['Usuarios que lo han resuelto', 'Usuarios que aun no lo han resuelto']

		db.close()
		return PLOTLY_PIE_CHART(labels, values, title="Grafica de Resolucion")
	else: 
		db.close()
		return '<h2 style="text-align: center; vertical-align: middle; line-height: 200px; height: 200px; color: dimgray;"> Sin Actividad </h2>'

# Done
def GRAPH_PROBLEM_LANGUAGES(problem_id):
	db = DB_Connection.database()

	if db.query("SELECT COUNT(*) FROM submission WHERE problem_id = {}".format(problem_id), fetchone=True)[0] != 0:

		rows = db.query("""SELECT language, COUNT(*) FROM submission 
			WHERE problem_id = {}
			GROUP BY language""".format(problem_id), fetchall=True)
		
		labels = []
		values = []
		for row in rows:
			labels.append(row[0])
			values.append(row[1])
		db.close()
		return PLOTLY_PIE_CHART(labels, values, title="Distribución de Lenguajes")
	else: 
		db.close()
		return '<h2 style="text-align: center; vertical-align: middle; line-height: 200px; height: 200px; color: dimgray;"> Sin Actividad </h2>'