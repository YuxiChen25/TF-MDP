import pickle
import os
import math
import argparse
from tqdm import tqdm
import random

#path should be what the directory of data is 
path = r'C:\Users\wmasi\Documents\TF-Agent-States\RL_Training_ConnectFour'

def load_data(path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return pickle.load(f)
    return None

def generate_xy_pair(player_1_ep, player_2_ep, mode):

    # Generates XY Pairs
    # By Shifting Indices 
    # Off-By-One

    full_game = []
    full_game_2 = []
    length = 0
    max = 0
    if len(player_1_ep) < len(player_2_ep):
        length = len(player_1_ep)
        max = 2
    elif len(player_2_ep) < len(player_1_ep):
        length = len(player_2_ep)
        max = 1
    for i in range(length):
        if mode == 0 or mode == 2:
            full_game.append(player_1_ep[i][-1])
            full_game.append(player_2_ep[i][-1])
        elif mode == 1:
            full_game.append(player_1_ep[i][-1][-1])
            full_game.append(player_2_ep[i][-1][-1])
    if max == 1:
        if mode != 1:
            full_game.append(player_1_ep[-1][-1])
        else:
            full_game.append(player_1_ep[-1][-1][-1])
    elif max == 2:
        if mode != 1:
            full_game.append(player_2_ep[-1][-1])
        else:
            full_game.append(player_2_ep[-1][-1][-1])
     
    if mode == 2:
        full_game_2 = [x[1] for x in full_game][1:]

    q_vals = []
    # for i in range(len(full_game) - 1):
    if len(full_game) > 1:
        i = random.choice(range(len(full_game) - 1))
        if mode == 1:
            if i % 2 == 0: #state is player 1's move, meaning it's player 2's turn
                q_vals.append((full_game[:i + 1], player_1_ep[i // 2][1]))
            else:
                q_vals.append((full_game[:i + 1], player_2_ep[i // 2][1]))
        elif mode == 0:
            if i % 2 == 0: #state is player 1's move, meaning it's player 2's turn
                q_vals.append((full_game[:i + 1], player_1_ep[i // 2][1]))
            else:
                q_vals.append((full_game[:i + 1], player_2_ep[i // 2][1]))
        else:
            x_val = []
            for j in range(i):
                x_val.append(full_game[j])
                x_val.append(full_game_2[j])
            x_val.append(full_game[i])
            if i % 2 == 0: #state is player 1's move, meaning it's player 2's turn
                q_val = player_1_ep[i // 2][1]
            else:
                q_val = player_2_ep[i // 2][1]
            q_vals.append((x_val, q_val))
    if mode != 2:
        return (full_game[:-1], full_game[1:]), q_vals
    else:
        return (full_game[:-1], full_game_2), q_vals

num_gpus = 8


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=int, default=0, choices=[0, 1, 2], help='Data Mode (state, action, state-action)')
    args = parser.parse_args()

    for i in tqdm(range(1, 11)):
        j = 890000
        training_hist = []
        q_hist = []
        new_path_first_half = path
        while True:
            new_path_second_half_1 = rf'connect-4-data\{i}\connect_4_data\data_agent_1_games_{j}.pkl'
            new_path_second_half_2 = rf'connect-4-data\{i}\connect_4_data\data_agent_-1_games_{j}.pkl'
            train_output_path_second_half = rf'training_data\{i}\training_games_{j}'
            train_output_path = os.path.join(new_path_first_half, train_output_path_second_half)
            #print(train_output_path)
            q_output_path_second_half = rf'training_data\{i}\q_vals_games_{j}'
            q_output_path = os.path.join(new_path_first_half, q_output_path_second_half)
            games_1 = load_data(os.path.join(new_path_first_half, new_path_second_half_1))
            #print(os.path.join(new_path_first_half, new_path_second_half_1))
            if games_1 is None:
                break
            games_2 = load_data(os.path.join(new_path_first_half, new_path_second_half_2))
            for k in range(len(games_1)):
                temp_training_hist, temp_q_hist = generate_xy_pair(games_1[k], games_2[k], args.m)
                # training_hist.append(temp_training_hist)
                q_hist.append(temp_q_hist)
            j += 5000
        print(len(training_hist))
        print(len(q_hist))
        # with open(train_output_path + "_mode_" + str(args.m) + '.pkl', 'wb') as f:
        #     pickle.dump(training_hist, f)
        with open(q_output_path + "_mode_" + str(args.m) + '.pkl', 'wb') as f:
            pickle.dump(q_hist, f)   
        
if __name__ == "__main__":
    main()