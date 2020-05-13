"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
from mlgame.communication import ml as comm

def ml_loop(side: str):
    """
    The main loop for the machine learning process
    The `side` parameter can be used for switch the code for either of both sides,
    so you can write the code for both sides in the same script. Such as:
    ```python
    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()
    ```
    @param side The side which this script is executed for. Either "1P" or "2P".
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    
    ball_served = False
    def move_to(player, pred,lastplat,x_balllast,cb) : #move platform to predicted position to catch ball 
        if player == '1P':
            if scene_info["platform_1P"][0]+20  > (pred-10) and scene_info["platform_1P"][0]+20 < (pred+10):
                a=scene_info["platform_1P"][0]-lastplat
                b=scene_info["ball"][0]-x_balllast
                if b<0 and cb==True:
                    return 1
                elif b>0 and cb==True:
                        return 2
                elif scene_info["platform_1P"][0]+20  > (pred-6) and scene_info["platform_1P"][0]+20<(pred+6) :
                    
                    if b>0 and cb==False:
                        return 1
                    elif b<0 and cb==False:
                        return 2
                    else:
                        return 0
                else:
                    return 0 # NONE
            elif scene_info["platform_1P"][0]+20 <= (pred-10) : return 1 # goes right
            else : return 2 # goes left
        else :
            if scene_info["platform_2P"][0]+20  > (pred-10) and scene_info["platform_2P"][0]+20 < (pred+10):
                a=scene_info["platform_1P"][0]-lastplat
                b=scene_info["ball"][0]-x_balllast
                if b<0 and cb==True:
                    return 1
                elif b>0 and cb==True:
                        return 2
                elif scene_info["platform_2P"][0]+20  > (pred-6) and scene_info["platform_2P"][0]+20<(pred+6) :
                    if b>0 and cb==False:
                        return 1
                    elif b<0 and cb==False:
                        return 2
                    else:
                        return 0
                else:
                    return 0 # NONE
            elif scene_info["platform_2P"][0]+20 <= (pred-10) : return 1 # goes right
            else : return 2 # goes left
    
    def check_blocker(player,lastblockerpos,pred):
        if(player=='1P'):
            result=False
            if(scene_info["ball_speed"][1] > 0):
                s = ( (scene_info["platform_1P"][1]-5)-(scene_info["blocker"][1]+20) ) // scene_info["ball_speed"][1]
                ballpred=pred+(scene_info["ball_speed"][0]*s)
                blockerpred=scene_info["blocker"][0]+s*(scene_info["blocker"][0]-lastblockerpos)
                bound = ballpred // 200 # Determine if it is beyond the boundary
                if (bound > 0): # pred > 200 # fix landing position
                    if (bound%2 == 0) : 
                        ballpred = ballpred - bound*200                    
                    else :
                        ballpred = 200 - (ballpred - 200*bound)
                elif (bound < 0) : # pred < 0
                    if (bound%2 ==1) :
                        ballpred = abs(ballpred - (bound+1) *200)
                    else :
                        ballpred = ballpred + (abs(bound)*200)
            
                bound = blockerpred // 170 # Determine if it is beyond the boundary

                if (bound > 0): # pred > 200 # fix landing position
                    if (bound%2 == 0) : 
                        blockerpred = blockerpred - bound*170                   
                    else :
                        blockerpred = 170 - (blockerpred - 170*bound)
                elif (bound < 0) : # pred < 0
                    if (bound%2 ==1) :
                        blockerpred = abs(blockerpred - (bound+1) *170)
                    else :
                        blockerpred = blockerpred + (abs(bound)*170)
                if(blockerpred+32>=ballpred and blockerpred-2<=ballpred):
                    result=True
            return result        
                
                    
        else:
            result=False
            if(scene_info["ball_speed"][1] < 0):
                s = ( (scene_info["blocker"][1])-(scene_info["platform_2P"][1]+35) ) // scene_info["ball_speed"][1]
                ballpred=pred+(scene_info["ball_speed"][0]*s)
                blockerpred=scene_info["blocker"][0]+s*(scene_info["blocker"][0]-lastblockerpos)
                bound = ballpred // 200 # Determine if it is beyond the boundary
                if (bound > 0): # pred > 200 # fix landing position
                    if (bound%2 == 0) : 
                        ballpred = ballpred - bound*200                    
                    else :
                        ballpred = 200 - (ballpred - 200*bound)
                elif (bound < 0) : # pred < 0
                    if (bound%2 ==1) :
                        ballpred = abs(ballpred - (bound+1) *200)
                    else :
                        ballpred = ballpred + (abs(bound)*200)
            
                bound = blockerpred // 170 # Determine if it is beyond the boundary

                if (bound > 0): # pred > 200 # fix landing position
                    if (bound%2 == 0) : 
                        blockerpred = blockerpred - bound*170                   
                    else :
                        blockerpred = 170 - (blockerpred - 170*bound)
                elif (bound < 0) : # pred < 0
                    if (bound%2 ==1) :
                        blockerpred = abs(blockerpred - (bound+1) *170)
                    else :
                        blockerpred = blockerpred + (abs(bound)*170)
                if(blockerpred+30>=ballpred and blockerpred<=ballpred):
                    result=True
            return result
    def hit_check(lastblockerpos):
        result=[-1,-1]
        if(scene_info["ball_speed"][1] > 0 and scene_info["ball"][1]<261):
            s1 = ( (scene_info["blocker"][1])-(scene_info["ball"][1]) ) // scene_info["ball_speed"][1]
            s2 = ((scene_info["blocker"][1]+20)-(scene_info["ball"][1]))// scene_info["ball_speed"][1]
            while(True):
                ballpred=scene_info["ball"][0]+(scene_info["ball_speed"][0]*s1)
                blockerpred=scene_info["blocker"][0]+s1*(scene_info["blocker"][0]-lastblockerpos)
                bound = ballpred // 200 # Determine if it is beyond the boundary
                if (bound > 0): # pred > 200 # fix landing position
                    if (bound%2 == 0) : 
                        ballpred = ballpred - bound*200                    
                    else :
                        ballpred = 200 - (ballpred - 200*bound)
                elif (bound < 0) : # pred < 0
                    if (bound%2 ==1) :
                        ballpred = abs(ballpred - (bound+1) *200)
                    else :
                        ballpred = ballpred + (abs(bound)*200)
            
                bound = blockerpred // 170 # Determine if it is beyond the boundary

                if (bound > 0): # pred > 200 # fix landing position
                    if (bound%2 == 0) : 
                        blockerpred = blockerpred - bound*170                   
                    else :
                        blockerpred = 170 - (blockerpred - 170*bound)
                elif (bound < 0) : # pred < 0
                    if (bound%2 ==1) :
                        blockerpred = abs(blockerpred - (bound+1) *170)
                    else :
                        blockerpred = blockerpred + (abs(bound)*170)
                if(blockerpred==ballpred ):
                    # print(scene_info["frame"],":","hitLeft")
                    result[0]=ballpred
                    result[1]=scene_info["ball"][1]+(scene_info["ball_speed"][1]*s1)
                    break
                if blockerpred+30==ballpred:
                    # print(scene_info["frame"],":","hitRight")
                    result[0]=ballpred
                    result[1]=scene_info["ball"][1]+(scene_info["ball_speed"][1]*s1)
                    break
                if(s1==s2):
                    break
                else:
                    s1+=1
            
            
        return result      
            


            
    def ml_loop_for_1P(x_lastplat,x_balllast,x_lastblocker): 
        cb=False
        if scene_info["ball_speed"][1] > 0 : # 球正在向下 # ball goes down
            newpos=hit_check(lastblockerpos=x_lastblocker)
            if(newpos[0]==-1):
                x = ( scene_info["platform_1P"][1]-scene_info["ball"][1] ) // scene_info["ball_speed"][1] # 幾個frame以後會需要接  # x means how many frames before catch the ball
                pred = scene_info["ball"][0]+(scene_info["ball_speed"][0]*x)  # 預測最終位置 # pred means predict ball landing site 
            else:
                x = ( scene_info["platform_1P"][1]-newpos[1] ) // scene_info["ball_speed"][1] # 幾個frame以後會需要接  # x means how many frames before catch the ball
                pred = newpos[0]+(scene_info["ball_speed"][0]*x) 

            bound = pred // 200 # Determine if it is beyond the boundary
            if (bound > 0): # pred > 200 # fix landing position
                if (bound%2 == 0) : 
                    pred = pred - bound*200                    
                else :
                    pred = 200 - (pred - 200*bound)
            elif (bound < 0) : # pred < 0
                if (bound%2 ==1) :
                    pred = abs(pred - (bound+1) *200)
                else :
                    pred = pred + (abs(bound)*200)
            if(scene_info["ball"][1]>400 and scene_info["ball"][1]<=420):
                cb=check_blocker(player='1P',lastblockerpos=x_lastblocker,pred=pred)
            return move_to(player = '1P',pred = pred,lastplat=x_lastplat,x_balllast=x_balllast,cb=cb)
        else : # 球正在向上 # ball goes up
            return move_to(player = '1P',pred = 100,lastplat=x_lastplat,x_balllast=x_balllast,cb=cb)



    def ml_loop_for_2P(x_lastplat,x_balllast,x_lastblocker):  # as same as 1P
        cb=False
        if scene_info["ball_speed"][1] > 0 : 
            return move_to(player = '2P',pred = 100,lastplat=x_lastplat,x_balllast=x_balllast,cb=cb)
        else : 
            x = ( scene_info["platform_2P"][1]+30-scene_info["ball"][1] ) // scene_info["ball_speed"][1] 
            pred = scene_info["ball"][0]+(scene_info["ball_speed"][0]*x) 
            bound = pred // 200 
            if (bound > 0):
                if (bound%2 == 0):
                    pred = pred - bound*200 
                else :
                    pred = 200 - (pred - 200*bound)
            elif (bound < 0) :
                if bound%2 ==1:
                    pred = abs(pred - (bound+1) *200)
                else :
                    pred = pred + (abs(bound)*200)
            if(scene_info["ball"][1]>50 and scene_info["ball"][1]<=80):
                cb=check_blocker(player='2P',lastblockerpos=x_lastblocker,pred=pred)
            return move_to(player = '2P',pred = pred,lastplat=x_lastplat,x_balllast=x_balllast,cb=cb)

    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.recv_from_game()

        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info["status"] != "GAME_ALIVE":
            # Do some updating or resetting stuff
            ball_served = False

            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue

        # 3.3 Put the code here to handle the scene information

        # 3.4 Send the instruction for this frame to the game process
        if not ball_served:
            if(side=="2P"):
                x_lastblocker=scene_info["blocker"][0] 
                x_lastplat=scene_info["platform_2P"][0] 
                                
                x_last_position = scene_info["ball"][0] 
                # x_rebound = 0
                # y_rebound = 0
            elif side=="1P":
                x_lastblocker=scene_info["blocker"][0] 
                x_lastplat=scene_info["platform_1P"][0] 
                
                x_last_position = scene_info["ball"][0] 
                
                # x_rebound = 0
                # y_rebound = 0
            comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_LEFT"})
            ball_served = True
        else:
            if side == "1P":
                command = ml_loop_for_1P(x_lastplat=x_lastplat,x_balllast=x_last_position,x_lastblocker=x_lastblocker)
            else:
                command = ml_loop_for_2P(x_lastplat=x_lastplat,x_balllast=x_last_position,x_lastblocker=x_lastblocker)

            if command == 0:
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
            elif command == 1:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            else :
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            
            
            if side=="1P":
                x_lastplat=scene_info["platform_1P"][0]
                x_last_position = scene_info["ball"][0]
                x_lastblocker=scene_info["blocker"][0]
            else:
                x_lastplat=scene_info["platform_2P"][0]
                x_last_position = scene_info["ball"][0]
                x_lastblocker=scene_info["blocker"][0]  