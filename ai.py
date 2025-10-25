import neat
import math
import pickle
import random
import os

def evaluate(genomes, config):

    Ttouches = 0
    Ttackles = 0
    TO_F_B = 0
    TB_F_B = 0
    TB_goals = 0
    TR_goals = 0
    for i, (genome_id1, genome1) in enumerate(genomes):
        bpos = [(800,600),(250,300),(250,800),(400,600)]
        rpos = [(1000,550),(1250,300),(1250,800),(1100,550)]
        ball_pos = (775,600)
        genome1.fitness = 0
        touches = 0
        tackles = 0
        O_F_B = 0
        B_F_B = 0
        B_goals = 0
        R_goals = 0
        for x in range(300):

            val = random.randint(0,3)
            vals = [-20,20]
            bpos[val] = (bpos[val][0]+random.choice(vals),bpos[val][1]+random.choice(vals))

            net = neat.nn.FeedForwardNetwork.create(genome1, config)
            output = net.activate((rpos[0][0], rpos[0][1]
                                   , rpos[1][0], rpos[1][1]
                                   , rpos[2][0], rpos[2][1]
                                   , rpos[3][0], rpos[3][1]
                                   , bpos[0][0], bpos[0][1]
                                   , bpos[1][0], bpos[1][1]
                                   , bpos[2][0], bpos[2][1]
                                   , bpos[3][0], bpos[3][1]
                                   , ball_pos[0], ball_pos[1]))
            decision = output.index(max(output))

# control player 1
            if decision > 14:
                rpos[0] = (rpos[0][0],rpos[0][1]+20)
            elif decision > 13:
                rpos[0] = (rpos[0][0],rpos[0][1]-20)
            elif decision > 12:
                rpos[0] = (rpos[0][0]+20,rpos[0][1])
            elif decision > 11:
                rpos[0] = (rpos[0][0]-20,rpos[0][1])
#control player 2
            elif decision > 10:
                rpos[1] = (rpos[1][0],rpos[1][1]+20)
            elif decision > 9:
                rpos[1] = (rpos[1][0],rpos[1][1]-20)
            elif decision > 8:
                rpos[1] = (rpos[1][0]+20,rpos[1][1])
            elif decision > 7:
                rpos[1] = (rpos[1][0]-20,rpos[1][1])
#control player 3
            elif decision > 6:
                rpos[2] = (rpos[2][0],rpos[2][1]+20)
            elif decision > 5:
                rpos[2] = (rpos[2][0],rpos[2][1]-20)
            elif decision > 4:
                rpos[2] = (rpos[2][0]+20,rpos[2][1])
            elif decision > 3:
                rpos[2] = (rpos[2][0]-20,rpos[2][1])
#control player 4
            elif decision > 2:
                rpos[3] = (rpos[3][0],rpos[3][1]+20)
            elif decision > 1:
                rpos[3] = (rpos[3][0],rpos[3][1]-20)
            elif decision > 0:
                rpos[3] = (rpos[3][0]+20,rpos[3][1])
            else:
                rpos[3] = (rpos[3][0]-20,rpos[3][1])
            
            for player in rpos:
                if player[0] > 1555:
                    player = (1555,player[1])
                    O_F_B += 1
                elif player[0] < 5:
                    player = (5,player[1])
                    O_F_B += 1
                elif player[1] > 1150:
                    player = (player[0],1150)
                    O_F_B += 1
                elif player[1] < 5:
                    player = (player[0],5)
                    O_F_B += 1
            
            for player in rpos:
                distance = math.sqrt((ball_pos[0]-player[0])**2 + (ball_pos[1]-player[1])**2)
                if distance < 100:
                    if (ball_pos[1]-player[1]) > 50:
                        ball_pos = (ball_pos[0],ball_pos[1]+100)
                    elif (ball_pos[0]-player[0]) > 0:
                        ball_pos = (ball_pos[0]+100,ball_pos[1])
                    elif (ball_pos[1]-player[1]) < -50:
                        ball_pos = (ball_pos[0],ball_pos[1]-100)
                    elif (ball_pos[0]-player[0]) < 0:
                        ball_pos = (ball_pos[0]-100,ball_pos[1])
                    touches += 1
            
            for player in bpos:
                distance = math.sqrt((ball_pos[0]-player[0])**2 + (ball_pos[1]-player[1])**2)
                if distance < 100:
                    if (ball_pos[1]-player[1]) > 50:
                        ball_pos = (ball_pos[0],ball_pos[1]+100)
                        tackles += 1
                    elif (ball_pos[0]-player[0]) > 0:
                        ball_pos = (ball_pos[0]+100,ball_pos[1])
                        tackles += 1
                    elif (ball_pos[1]-player[1]) < -50:
                        ball_pos = (ball_pos[0],ball_pos[1]-100)
                        tackles += 1
                    elif (ball_pos[0]-player[0]) < 0:
                        ball_pos = (ball_pos[0]-100,ball_pos[1])
                        tackles += 1

            if ball_pos[0] < 5 and ball_pos[1] > 400 and ball_pos[1] < 700:
                bpos = [(800,600),(250,300),(250,800),(400,600)]
                rpos = [(1000,550),(1250,300),(1250,800),(1100,550)]
                ball_pos = (775,600)
                R_goals += 1
            elif ball_pos[0] > 1555 and ball_pos[1] > 400 and ball_pos[1] < 700:
                bpos = [(800,600),(250,300),(250,800),(400,600)]
                rpos = [(1000,550),(1250,300),(1250,800),(1100,550)]
                ball_pos = (775,600)
                B_goals += 1

            if ball_pos[0] > 1555:
                ball_pos = (1555,ball_pos[1])
                B_F_B += 1
            elif ball_pos[0] < 5:
                ball_pos = (5,ball_pos[1])
                B_F_B += 1
            elif ball_pos[1] > 1150:
                ball_pos = (ball_pos[0],1150)
                B_F_B += 1
            elif ball_pos[1] < 5:
                ball_pos = (ball_pos[0],5)
                B_F_B += 1

            genome1.fitness += touches * 2  
            genome1.fitness -= tackles * 5
            genome1.fitness -= B_F_B * 10  
            genome1.fitness -= B_goals * 50  
            genome1.fitness -= O_F_B * 10  
            genome1.fitness += R_goals * 100 

            Ttouches += touches
            Ttackles += tackles
            TB_F_B += B_F_B
            TB_goals += B_goals
            TO_F_B += O_F_B
            TR_goals += R_goals

            if R_goals > 0:
                genome1.fitness += 1000  
            if B_goals == 0 and O_F_B == 0:
                genome1.fitness += 500  

    print("number of touches: "+str(Ttouches))
    print("number of times tackled: "+str(Ttackles))
    print("number of times run out of play: "+str(TO_F_B))
    print("number of times Ball was out of play: "+str(TB_F_B))
    print(TB_goals," ",TR_goals)
    print()

# Define the NEAT function
def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-23")
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #check point every 5 generations
    p.add_reporter(neat.Checkpointer(5))
    # Run the NEAT algorithm for up to 50 generations
    winner = p.run(evaluate)#,50
    print(winner)

    # Print the winning genome
    print('\nBest genome:\n{!s}'.format(winner))
    with open("best8.dump","wb") as f:
        pickle.dump(winner, f)

# Run the NEAT function
if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config_file.txt')
    # Load the NEAT configuration
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    run_neat(config)