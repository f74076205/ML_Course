"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)
def cal_m(x2,y2,m):        
        #m=(y2-y1)/(x2-x1)
        board_x=-((y2-400)/m-x2)
        
        rwall_y=y2-m*(x2-200)
        lwall_y=y2-m*(x2-0)
        if(rwall_y>y2 and rwall_y<400):
            return cal_m(200,rwall_y,-m)
        elif(lwall_y>y2 and lwall_y<400):
            return cal_m(0,lwall_y,-m)
        else:
             return board_x
        # print(x1)
        # if(x1<=0):
        #     return -(x1)
        # elif(x1>=400):
        #     return 400-(x1-400)
        # else:
        #     return x1
def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()#一定要保留這行 跟遊戲核心的通道


    # 3. Start an endless loop.
    
    
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()#取得遊戲場景資訊 

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information
        
        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
            goal=0
            # pregoal=-1
            m=-1
            ball_x_pre=95
            ball_y_pre=400
        else:
            
            ball_x=scene_info.ball[0]
            ball_y=scene_info.ball[1]
            platform_x_left=scene_info.platform[0]
            platform_x_right=scene_info.platform[0]+40
            #print(scene_info.platform[0])
            #if(ball_x==0 or ball_x==200):
            m=(ball_y-ball_y_pre)/(ball_x-ball_x_pre)
            #print(m)
                
            
            goal=cal_m(ball_x,ball_y,m)
            # print(goal)
            # if(goal!=pregoal):
            #     print(goal)

            
            if (platform_x_left-5)>goal:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            elif (platform_x_right+5)<goal:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            else :
               comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            
            
            ball_x_pre=ball_x
            ball_y_pre=ball_y
            # pregoal=goal
        
            
