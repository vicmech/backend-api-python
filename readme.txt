Instrucciones para uso de la API

ENDPOINTS PARA REPORTES

/api/reports/{report_id}
	Recibe el id del caso correspondiente y lo devuelve

/api/reports/?[PARAMS]
	Devuelve los casos que coincidan con los criterios de los parametros

PARAMS:
	status: El estatus del caso (No Case sensitive)
		'En proceso'
		'Cerrado'
		'Pausado'

	priority: La prioridad del caso (No Case sensitive)
		'Alta'
		'Media'
		'Baja'

/api/reports/solvingTime/{report_id}
	Devuelve el tiempo en dias de diferencia entre la fecha de registro del caso y la fecha de atencion (No solucion)

/api/reports/attendingTime/{report_id}
	Devuelve el tiempo en dias de diferencia entre la fecha de atencion del caso y la fecha de solucion

/api/reports/registerDate/?[PARAMS]
	Filtra casos por fecha de registro

	PARAMS:
		year
		mont
		day
	Todos corresponden a valores numericos asociados a la fecha

PARA REPORTERS

/api/reporters/?[PARAMS]
	Devuelve los reporters de acuerdo a los criterios establecidos en los parametros

	PARAMS(Opcionales):
		id: ID del reporter
		name: Nombre del reporter
		lastname: Apellido del reporter

PARA CASEMANAGERS

/api/casemanagers/?[PARAMS]
	Devuelve los casemanagers de acuerdo a los criterios establecidos en los parametros

	PARAMS(Opcionales):
		id: ID del casemanagers
		name: Nombre del casemanagers
		lastname: Apellido del casemanagers
