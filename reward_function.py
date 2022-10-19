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

    reward = 1
    
    # cur step  11 waypoint 
    
    st_point = closest_waypoints[0]
    
    cur_point_end = waypoints[st_point+10]
    cur_point_begin = waypoints[st_point]

    # next step    
    next_point_end = waypoints[st_point+21]
    next_point_begin = waypoints[st_point+11]
    
    # cal 
    cur_track_direction = math.atan2(cur_point_end[1]-cur_point_begin[1],cur_point_end[0]-cur_point_begin[0])
    next_track_direction = math.atan2(next_point_end[1]-next_point_begin[1],next_point_end[0]-next_point_begin[0])
    
    # convert angle
    cur_track_direction = math.degrees(cur_track_direction)
    next_track_direction = math.degrees(next_track_direction)
    

    # the angle diff between cur step and next step  
    next_step_direction_diff = next_track_direction - cur_track_direction 
    
    #the angle diff between cur step and car's heading
    direction_diff = heading - cur_track_direction
    
    if abs(next_step_direction_diff) <= 3:

        if abs(direction_diff) <= abs(next_step_direction_diff) :

            if speed < 3.0 :
                reward += ( speed / 2)
            else :
                reward += ( speed * 2 )

        if abs(steering_angle) > 3 :
            reward = 1e-3
        else : 
            reward += abs(steering_angle)*2

    elif next_step_direction_diff <= 20:

        if  next_step_direction_diff >= 0:
            
            if direction_diff >= 0 and direction_diff < next_step_direction_diff/2:
                
                remain_angle = (next_step_direction_diff/2 - direction_diff)
                if steering_angle >= 0 and steering_angle <= remain_angle:

                    if(steering_angle <=  remain_angle / 4 and  speed >=3.2  and speed <= 4):
                        reward += speed
                    elif (steering_angle <= remain_angle / 2 and speed >=2.4  and speed < 3.2):
                        reward += speed
                    elif (steering_angle <= ( 3 * remain_angle / 4 ) and speed >=1.7  and speed < 2.4):
                        reward += speed 
                    elif (steering_angle <=  remain_angle and speed >=1.5  and speed < 1.7):
                        reward += speed

            elif direction_diff < 0 and direction_diff > next_step_direction_diff/2:
                
                remain_angle = (next_step_direction_diff/2 - direction_diff)

                if steering_angle < 0 and steering_angle > remain_angle :

                    if(steering_angle >= remain_angle / 4 and  speed >= 3.2  and speed <= 4):
                        reward += speed
                    elif (steering_angle >= remain_angle / 2 and speed >= 2.4  and speed < 3.2):
                        reward += speed
                    elif (steering_angle >= ( 3 * remain_angle / 4 ) and speed >= 1.7  and speed < 2.4):
                        reward += speed
                    elif (steering_angle >= remain_angle and speed >=1.5  and speed < 1.7):
                        reward += speed


    if is_offtrack:
        reward = 1e-3
                        

    return float(reward)