import Arena
import thread

def main():
    a = Arena.Arena()
    a.create_arena()
    a.create_robots(3, True)
    a.create_robots(10, False)
    a.print_arena()
    moveRobot(a)
    a.print_arena()



if __name__ == "__main__":
    main()

def moveRobot(arena):
        for robot in arena.movingRob:
            direction = robot[0].move()
            if (direction == 0):  # step right
                if(arena[robot[1]+1][robot[2]]==0 or arena[robot[1]+1][robot[2]]==1):
                    arena[robot[1]][robot[2]]=robot[0].color
                    arena[robot[1] + 1][robot[2]]=robot[0].id
                    robot[1]=robot[1]+1
            if (direction == 1):  # step left
                if (arena[robot[1] - 1][robot[2]] == 0 or arena[robot[1] - 1][robot[2]] == 1):
                    arena[robot[1]][robot[2]] = robot[0].color
                    arena[robot[1] - 1][robot[2]] = robot[0].id
                    robot[1] = robot[1] - 1
            if (direction == 2):  # step up
                if (arena[robot[1] ][robot[2]+ 1] == 0 or arena[robot[1]][robot[2]+ 1] == 1):
                    arena[robot[1]][robot[2]] = robot[0].color
                    arena[robot[1] ][robot[2]+ 1] = robot[0].id
                    robot[2] = robot[2] + 1
            if (direction == 3):  # step down
                if (arena[robot[1]][robot[2] - 1] == 0 or arena[robot[1]][robot[2] - 1] == 1):
                    arena[robot[1]][robot[2]] = robot[0].color
                    arena[robot[1]][robot[2] - 1] = robot[0].id
                    robot[2] = robot[2] - 1
