import rubix_cube as r

c = r.BeginnerCube(3)

c.view()

print("Cost", c.cost())

c.scramble(100)

print("Cost", c.cost())

c.view()

print(c.solve())