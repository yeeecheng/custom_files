import math

def reward_function(params):
    '''
    Example of penalize steering, which helps mitigate zig-zag behaviors
    '''

    # Read input parameters
    distance_from_center = params['distance_from_center']
    steering_angle = params['steering_angle']
    track_width = params['track_width']
    speed = params['speed']
    is_left_of_center = params['is_left_of_center']
    is_offtrack = params['is_offtrack']
    closest_waypoints= params['closest_waypoints']
    x = params['x']
    y = params['y']
    heading = params['heading']
    all_wheels_on_track = params["all_wheels_on_track"]
    waypoints = params["waypoints"]


    next_point = waypoints[closest_waypoints[3]]
    prev_point = waypoints[closest_waypoints[0]]
    
    reward = 1

    track_direction = math.atan2(next_point[1]-prev_point[1],next_point[0]-prev_point[0])
    track_direction = math.degrees(track_direction)
    
    direction_diff = abs(track_direction - heading)
    if direction_diff < 5:

        if  abs(steering_angle) > 2 :
            reward  = 1e-3
        
        else :
            if speed < 4:
                reward += (speed/2 * (track_width/2 - distance_from_center))
            else:
                reward += (speed * (track_width/2 - distance_from_center))


    elif direction_diff < 25:
        
        if is_left_of_center and  steering_angle <= 0 and steering_angle >= (2-direction_diff): 

            if(steering_angle >= -10 and  speed >=4  and speed <= 4.5):
                reward += speed
            elif (steering_angle >= -15 and speed >=3  and speed < 4):
                reward += speed
            elif (steering_angle >= -20 and speed >=2  and speed < 3):
                reward += speed
            elif (steering_angle >= -25 and speed >=1.5  and speed < 2):
                reward += speed
            else :
                reward += (steering_angle+25) 

        elif not is_left_of_center and  steering_angle >=0 and steering_angle <= (direction_diff - 2): 
            if(steering_angle <= 10 and  speed >=4  and speed <= 4.5):
                reward += speed
            elif (steering_angle <= 15 and speed >=3  and speed < 4):
                reward += speed
            elif (steering_angle <= 20 and speed >=2  and speed < 3):
                reward += speed 
            elif (steering_angle <= 25 and speed >=1.5  and speed < 2):
                reward += speed
            else :
                reward -= (steering_angle - 25)   
    
        else :
            reward = 1e-3
    
    else :
        reward -= direction_diff

    
    if is_offtrack:
        reward = 1e-3
                        
    return float(reward)