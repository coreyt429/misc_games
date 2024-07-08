import cube2
import cube

winners = {0:0,1:0,2:0}
for test in range(10000):
	print("Cube 2")
	c=cube2.cube()
	c.scramble()
	c.save('clock.cube')
	time_2 = c.clock()

	print("Cube 1")
	c=cube.cube('clock.cube')
	#c.scramble()
	#c.save('clock1.cube')
	#c.scramble()
	time_1 = c.clock()

	if time_1 > time_2:
		winners[2] += 1
	elif time_1 == time_2:
		winners[0] += 1
	else:
		winners[1] += 1

print(winners)




