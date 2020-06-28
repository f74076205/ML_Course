class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0                            # speed initial
        self.car_pos = (0,0)                        # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        self.car_prepos= (0,0)
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        self.pre_grid=set()
        pass

    def update(self, scene_info):
        """
        9 grid relative position
        |    |    |    |
        |  1 |  2 |  3 |
        |    |  5 |    |
        |  4 |  c |  6 |
        |    |    |    |
        |  7 |  8 |  9 |
        |    |    |    |       
        """
        def check_grid():
            grid = set()
            grid_coin=set()
            speed_ahead = 100
            # if self.car_pos[0] <= 65: # left bound
            #     grid.add(-1)
            #     grid.add(-4)
            #     grid.add(-7)
            # elif self.car_pos[0] >= 565: # right bound
            #     grid.add(-3)
            #     grid.add(-6)
            #     grid.add(-9)
            for coin in scene_info["coins"]:
                x = self.car_pos[0] - coin[0] # x relative position
                y = self.car_pos[1] - coin[1] # y relative position
                if x <= 40 and x >= -40 :      
                    if y > 0 and y < 300:
                        grid_coin.add(2)
                        if y < 200:
                            grid_coin.add(5) 
                    elif y < 0 and y > -200:
                        grid_coin.add(8)
                if x > -110 and x < -40 :
                    
                    if y > 80 and y < 250:
                        grid_coin.add(3)
                    elif y < -80 and y > -200:
                        grid_coin.add(9)
                    elif y < 80 and y > -80:
                        grid_coin.add(6)
                if x < 110 and x > 40:
                    
                    if y > 80 and y < 250:
                        grid_coin.add(1)
                    elif y < -80 and y > -200:
                        grid_coin.add(7)
                    elif y < 80 and y > -80:
                        grid_coin.add(4)

            for car in scene_info["cars_info"]:
                if car["id"] != self.player_no:
                    x = self.car_pos[0] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position
                    if x <= 40 and x >= -40 :      
                        if y > 0 and y < 300:
                            grid.add(2)
                            if y < 200:
                                speed_ahead = car["velocity"]
                                grid.add(5) 
                        elif y < 0 and y > -200:
                            grid.add(8)
                    if x > -100 and x < -40 :
                        
                        if y > 80 and y < 250:
                            grid.add(3)
                        elif y < -80 and y > -200:
                            grid.add(9)
                        elif y < 80 and y > -80:
                            grid.add(6)
                    if x < 100 and x > 40:
                        
                        if y > 80 and y < 250:
                            grid.add(1)
                        elif y < -80 and y > -200:
                            grid.add(7)
                        elif y < 80 and y > -80:
                            grid.add(4)
            self.pre_grid=grid
            return move(grid= grid, speed_ahead = speed_ahead,grid_coin=grid_coin)
            
        def move(grid, speed_ahead,grid_coin): 
            pregrid=self.pre_grid
            # lane=self.car_lane
            # if self.player_no == 1:
            #     print(grid)
                # print("self_lane ",self.car_lane)
            # if self.player_no == 0:
            #     print(grid_coin)
            if len(grid) == 0:
                return ["SPEED"]
            elif(self.car_pos[0]<65):
                if(2 not in grid) :
                    if(5 in grid_coin) :
                        return["SPEED"]
                    elif(6 not in pregrid) and (3 not in grid) and (6 not in grid):
                        return ["SPEED", "MOVE_RIGHT"]
                    elif(6 not in pregrid) and (6 not in grid) and (9 not in grid):
                        return ["MOVE_RIGHT"]
                    elif(3 in grid_coin )and (3 not in grid )and( 6 not in grid):
                        return ["SPEED", "MOVE_RIGHT"]
                    elif(6 in grid_coin )and (3 not in grid )and( 6 not in grid):
                        return ["SPEED", "MOVE_RIGHT"]
                    else :
                        return["SPEED"]
                else :
                    if(5 in grid):
                        if(6 not in pregrid) and (3 not in grid) and (6 not in grid):
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                return ["BRAKE", "MOVE_RIGHT"]
                        elif(6 not in pregrid) and (6 not in grid) and (9 not in grid):
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                return ["BRAKE", "MOVE_RIGHT"]
                        else :
                            if self.car_vel < speed_ahead:
                                return ["SPEED"]
                            else:
                                return ["BRAKE"]
                    else:
                        if(5 in grid_coin):
                            return["SPEED"]
                        elif (3 not in grid) and (6 not in grid):
                            return ["SPEED", "MOVE_RIGHT"]
                        elif (6 not in grid) and (9 not in grid):
                            return ["MOVE_RIGHT"]
                        else :
                            return["SPEED"]
            elif(self.car_pos[0]>625):
                if(2 not in grid) :
                    if(5 in grid_coin):
                        return["SPEED"]
                    elif(4 not in pregrid) and (1 not in grid) and (4 not in grid):
                        return ["SPEED", "MOVE_LEFT"]
                    elif(4 not in pregrid) and (4 not in grid) and (7 not in grid):
                        return ["MOVE_LEFT"]
                    elif(1 in grid_coin) and (4 not in grid) and (1 not in grid):
                        return ["SPEED", "MOVE_LEFT"]
                    elif(4 in grid_coin) and (4 not in grid) and (1 not in grid):
                        return ["SPEED", "MOVE_LEFT"]
                    else :
                        return["SPEED"]
                else :
                    if(5 in grid):
                        if(4 not in pregrid) and (1 not in grid) and (4 not in grid):
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            else:
                                return ["BRAKE", "MOVE_LEFT"]
                        elif(4 not in pregrid) and (4 not in grid) and (7 not in grid):
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            else:
                                return ["BRAKE", "MOVE_LEFT"]
                        else :
                            if self.car_vel < speed_ahead:
                                return ["SPEED"]
                            else:
                                return ["BRAKE"]
                    else:
                        if(5 in grid_coin):
                            return["SPEED"]
                        elif (1 not in grid) and (4 not in grid):
                            return ["SPEED", "MOVE_LEFT"]
                        elif (4 not in grid) and (7 not in grid):
                            return ["MOVE_LEFT"]
                        else :
                            return["SPEED"]
            else:
                if (2 not in grid) : # Check forward
                    if (5 in grid_coin):
                        return["SPEED"] 
                    elif(1 in grid_coin) and (4 not in grid) and (1 not in grid):
                        return ["SPEED", "MOVE_LEFT"]
                    elif(3 in grid_coin )and (3 not in grid )and( 6 not in grid):
                        return ["SPEED", "MOVE_RIGHT"]
                    elif(4 in grid_coin) and (4 not in grid) and (1 not in grid):
                        return ["SPEED", "MOVE_LEFT"]
                    elif(6 in grid_coin )and (3 not in grid )and( 6 not in grid):
                        return ["SPEED", "MOVE_RIGHT"]
                    elif(2 in grid_coin):
                        return["SPEED"]
                    else :
                        # Back to lane center
                        if self.car_pos[0] > self.lanes[self.car_lane]:
                            return ["SPEED", "MOVE_LEFT"]
                        elif self.car_pos[0] < self.lanes[self.car_lane]:
                            return ["SPEED", "MOVE_RIGHT"]
                        else :return ["SPEED"]
                else:
                    if (5 in grid): # NEED to BRAKE
                        if (4 in pregrid) and (6 not in grid) and (9 not in grid):
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                return ["BRAKE", "MOVE_RIGHT"]
                        if (6 in pregrid) and (4 not in grid) and (7 not in grid):
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            else:
                                return ["BRAKE", "MOVE_LEFT"]
                        if (4 not in grid) and (7 not in grid): # turn left 
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            else:
                                return ["BRAKE", "MOVE_LEFT"]
                        elif (6 not in grid) and (9 not in grid): # turn right
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                return ["BRAKE", "MOVE_RIGHT"]
                        else : 
                            if self.car_vel < speed_ahead:  # BRAKE
                                return ["SPEED"]
                            else:
                                return ["BRAKE"]
                    # if (self.car_pos[0] < 30 ):
                    #     return ["SPEED", "MOVE_RIGHT"]
                    # if (self.car_pos[0] <60 ):
                    #     return ["SPEED", "MOVE_RIGHT"]
                    if (1 not in grid) and (4 not in grid) and (7 not in grid) and(4 in grid_coin) :
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid) and (9 not in grid)and (6 in grid_coin): # turn right 
                        return ["SPEED", "MOVE_RIGHT"]  
                    if (1 not in grid) and (4 not in grid) and (7 not in grid) and(1 in grid_coin) :
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid) and (9 not in grid)and(3 in grid_coin): # turn right 
                        return ["SPEED", "MOVE_RIGHT"]                      
                    if (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                        return ["SPEED", "MOVE_RIGHT"]

                    if (1 not in grid) and (4 not in grid)  and(4 in grid_coin) :
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid) and (6 in grid_coin): # turn right 
                        return ["SPEED", "MOVE_RIGHT"]  
                    if (1 not in grid) and (4 not in grid) and(1 in grid_coin) :
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid) and(3 in grid_coin): # turn right 
                        return ["SPEED", "MOVE_RIGHT"]  
                    if (1 not in grid) and (4 not in grid): # turn left 
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid): # turn right
                        return ["SPEED", "MOVE_RIGHT"]
                    if (4 not in grid) and (7 not in grid): # turn left 
                        return ["MOVE_LEFT"]    
                    if (6 not in grid) and (9 not in grid): # turn right
                        return ["MOVE_RIGHT"]
                    
                    
                    
                    
        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]
        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"
        checklane=0
        for curlane in self.lanes:
            if(self.car_pos[0]>curlane-22.5 and self.car_pos[0]<curlane+22.5):
                checklane=1
            if(self.car_pos[0]<65):
                checklane=1
            if self.car_pos[0]>625:
                checklane=1

        if(checklane==0):
            if(self.car_pos[0]-self.car_prepos[0]>0):
                if(self.car_pos[1]-self.car_prepos[1]>=self.car_vel):
                    self.car_prepos=self.car_pos
                    return ["SPEED", "MOVE_RIGHT"]
                else:
                    self.car_prepos=self.car_pos
                    return ["MOVE_RIGHT"]
            elif(self.car_pos[0]-self.car_prepos[0]<0):
                if(self.car_pos[1]-self.car_prepos[1]>=self.car_vel):
                    self.car_prepos=self.car_pos
                    return ["SPEED", "MOVE_LEFT"] 
                else:
                    self.car_prepos=self.car_pos
                    return ["MOVE_LEFT"]
               
            # print("no in center")
        # print(self.car_prepos)

        
        self.car_lane = self.car_pos[0] // 70
        self.car_prepos=self.car_pos
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass