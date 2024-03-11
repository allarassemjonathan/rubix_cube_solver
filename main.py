import rubix_cube as r

c = r.BeginnerCube(3)

c.view()

c.scramble(7)

c.view()

print(c.solve())