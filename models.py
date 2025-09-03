from pydantic import BaseModel

class PlayerStatus(BaseModel):
    player_num: int
    player_life: int
    player_power: int
    player_move_type: int
    player_state_no: int
    player_prev_state_no: int
    player_pos_x: float
    player_pos_y: float
    player_vel_x: float
    player_vel_y: float
    
class FrameStatus(BaseModel):
    player_1_status: PlayerStatus
    player_2_status: PlayerStatus
    current_frames: int