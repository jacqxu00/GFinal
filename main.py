from display import *
from draw import *
from parser import *
from matrix import *
import math

screen = new_screen()
color = [ 21, 244, 238 ]
edges = []
transform = new_matrix()

# print_matrix( make_bezier() )
# print
# print_matrix( make_hermite() )
# print

#dw test file
parse_file( 'script', edges, transform, screen, color )

#henry
#parse_file( 'snowmansled', edges, transform, screen, color )
