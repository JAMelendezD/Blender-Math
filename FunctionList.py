def saddle():
	z = 'x**2-y**2'
	return(z)

def trigonometric():
	z = 'cos(x)*cos(y)'
	return(z)

def wave():
	z = 'sin(sqrt(x**2+y**2))/sqrt(x**2+y**2)'
	return(z)

def exponential():
	z = '(1-x/ 2+x**7+y**3)*exp(-x**2-y**2)'
	return(z)

def pyramid():
	z = '1-abs(x+y)-abs(y-x)'
	return(z)

def paper():
	z = 'sin(x*y)'
	return(z)

def torus():
	x = '(2+cos(p))*cos(t)'
	y = '(2+cos(p))*sin(t)'
	z = 'sin(p)'
	return(x,y,z)

def sphere():
	x = 'cos(p)*sin(t)'
	y = 'sin(p)*sin(t)'
	z = 'cos(t)'
	return(x,y,z)

def dna():
	x = 'cos(p)*cos(t)'
	y = 'sin(t)*cos(p)'
	z = 't'
	return(x,y,z)

def curves():
	x = '(2+sin(7*p+5*t))*cos(p)*sin(t)'
	y = '(2+sin(7*p+5*t))*sin(p)*sin(t)'
	z = '(2+sin(7*p+5*t))*cos(t)'
	return(x,y,z)

def kleinbot():
	x = '-2/15*cos(p)*(3*cos(t)-30*sin(p)+90*cos(p)**4*sin(p)-60*cos(p)**6*sin(p)+5*cos(p)*sin(p)*cos(t))'
	y = '-1/15*sin(p)*(3*cos(t)-3*cos(p)**2*cos(t)-48*cos(p)**4*cos(t)+48*cos(p)**6*cos(t)-60*sin(p)+5*cos(p)*sin(p)*cos(t)-5*cos(p)**3*sin(p)*cos(t)-80*cos(p)**5*sin(p)*cos(t)+80*cos(p)**7*sin(p)*cos(t))'
	z = '3/15*(3+5*cos(p)*sin(p))*sin(t)'
	return(x,y,z)

def klein8():
	x = 'cos(t)*(2+cos(t/2)*sin(p)-sin(t/2)*sin(2*p))'
	y = 'sin(t)*(2+cos(t/2)*sin(p)-sin(t/2)*sin(2*p))'
	z = 'sin(t/2)*sin(p)+cos(t/2)*sin(2*p)'
	return(x,y,z)

def shell():
	x = 't*sin(t)*cos(p)'
	y = 't*cos(t)*cos(p)'
	z = 't*sin(p)'
	return(x,y,z)

def cylinder():
	x = 'cos(p)-cos(t)'
	y = 'sin(p)-sin(t)'
	z = 't'
	return(x,y,z)
