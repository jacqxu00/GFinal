test: robot.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
	python main.py simple_anim.mdl

run: main.py display.py draw.py matrix.py parser.py
	python main.py

clean:
	rm *.pyc
	rm *~
