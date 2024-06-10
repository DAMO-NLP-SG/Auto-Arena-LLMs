import math
from typing import Dict, List, Tuple
import argparse
from utils.generator import load_question_from_generator
from utils.LD_pair import make_pair_debate_many_questions, peer_evaluate_many_debates 
from utils.score_utils import compute_mle_elo, calculate_win_rate
import pandas as pd
from collections import defaultdict
import os

def pair_players(
    names: List[str], previous_matchups: Dict[str, set]
) -> List[Tuple[str, str]]:
    
    def can_be_paired(player1, player2):
        return player2 not in previous_matchups.get(player1, set())

    def find_pairings():
        # repeat until all players are paired
        if not unpaired_names:
            return []

        # first player
        player = unpaired_names.pop(0)

        # for the rest (opponents)
        for opponent in unpaired_names:

            # if have not played before
            if can_be_paired(player, opponent):

                # add to matchup pairings
                unpaired_names.remove(opponent)
                previous_matchups[player].add(opponent)
                previous_matchups[opponent].add(player)
                return [(player, opponent)] + find_pairings()

        # Assign a bye if no opponent is found
        print(f"Bye for {player}")
        # None is to indicate that this player has no opponents
        # Every opponent has been played before
        return [(player, None)] + find_pairings()

    # initialize unpaired to all players
    unpaired_names = names[:]

    return find_pairings()

if __name__ == "__main__":
    # read arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("--num_each_domain_to_load", type=int, default=5, help="number of questions to debate for each domain")
    parser.add_argument("--judge_debate_rounds", type=int, default=1, help="How many rounds of debates to run")
    parser.add_argument("--question_save_file", type=str, default='data/generated_questions_difficult.jsonl', help="where to save generated questions")
    parser.add_argument("--tournament_dir", type=str, required=True, help="where to save the tournament files")
    parser.add_argument("--shuffle_ab", type=bool, default=True, help="whether to shuffle the order of model_a and model_b")
    parser.add_argument("--evaluate_first_turn", action="store_true", help="whether to evaluate the first turn of the debate")
    parser.add_argument("--language", type=str, default='en', help="language used for evaluation")
    
    args = parser.parse_args()
    if args.language == 'zh' and 'zh' not in args.tournament_dir:
        raise Exception("Mismatch between language and tournament directory. Please use a directory with 'zh' in the name.")
    if args.language not in ['en', 'zh']:
        raise Exception("Invalid language. Choose either 'en' or 'zh'.")
    # if args.language == 'en':
    #     args.all_judge_file = 'data/all_results/all_judge_results_LD.jsonl'
    #     args.all_debate_file = 'data/all_results/all_debate_history_LD.jsonl'
    # elif args.language == 'zh':
    #     args.all_judge_file = 'data/all_results/all_judge_results_LD_zh.jsonl'
    #     args.all_debate_file = 'data/all_results/all_debate_history_LD_zh.jsonl'

    if args.language == 'en':
        # 7 models initially
        player_names = ['gpt-4-turbo-2024-04-09', 'Qwen/Qwen1.5-72B-Chat', 'claude-3-haiku-20240307',
                    'zero-one-ai/Yi-34B-Chat', 'mistralai/Mixtral-8x7B-Instruct-v0.1', 'gpt-35-turbo-0125',
                    'meta-llama/Llama-2-70b-chat-hf']
    elif args.language == 'zh':
        # also include chinese models
        player_names = ['gpt-4-turbo-2024-04-09', 'meta-llama/Llama-3-70b-chat-hf', 'claude-3-haiku-20240307',
                        'Qwen/Qwen1.5-72B-Chat', 'zero-one-ai/Yi-34B-Chat', 
                        'deepseek-ai/deepseek-llm-67b-chat', 'glm-4', 
                        'wenxin-4', 'minimax-abab6.5-chat', 'SenseChat-5']
    
    # organized according to MMLU ranking
    mmlu_ratings = pd.read_csv('data/MMLU.csv')
    mmlu_ratings = mmlu_ratings[mmlu_ratings['Model'].isin(player_names)]
    mmlu_ratings = mmlu_ratings.sort_values(by='MMLU', ascending=False)
    missing_players = [p for p in player_names if p not in mmlu_ratings['Model'].tolist()]
    if len(missing_players) > 0:
        print(f"Missing MMLU ratings for the following players: {missing_players}")
        raise Exception(f'Provide initial MMLU scores of {missing_players} in data/MMLU.csv!')
    else:
        player_names = mmlu_ratings['Model'].tolist()
    ############################################################
    ##################### INITIALIZATION #######################
    ############################################################

    # Swiss style tournament
    initial_seeding = player_names.copy()

    # determine number of rounds
    num_rounds = math.ceil(math.log2(len(player_names)))
    print("Number of rounds in total:", num_rounds)

    # initialize previous matchups as empty
    previous_matchups = {p: set() for p in player_names}

    # #initialize ELO scores
    INIT_RATING=1000
    scores = defaultdict(lambda: INIT_RATING) 

    ############################################################
    ################### 1. LOAD QUESTIONS ######################
    ############################################################

    # load questions
    questions = load_question_from_generator(args.question_save_file, args.num_each_domain_to_load, language = args.language)
    all_judge_results = []

    # for each round
    for round_num in range(num_rounds):
        print('***************** ROUND', round_num+1, '*****************')

        # reorganize players according to current ratings at the beginning of each round
        # Sort by scores, then initial seed
        player_names.sort(
            key=lambda p: (-scores[p], initial_seeding.index(p))
        )  
        # pair players
        pairings = pair_players(
            list(player_names), previous_matchups
        )
        print('Pairings for this round: ', pairings)
        
        # create a folder
        round_dir = f"{args.tournament_dir}/round{round_num+1}"
        os.makedirs(round_dir, exist_ok=True)

        elo_history = {}
        for model in player_names:
            elo_history[model] = [scores[model]]

        for pairing_i, (model_a, model_b) in enumerate(pairings):
            print('----------------- Match:', model_a, model_b, '-----------------')
            print('initial scores:', scores)
            if model_b == None:
                # model_a wins by default
                # scores = update_elo(scores, model_a)
                # print(f"{model_a} wins by default")
                print('Bye for', model_a)
            else:
                print('scores: ', scores)
                # committee in descending order of scores
                committee = sorted(scores, key=scores.get, reverse=True)
                committee = [c for c in committee if c != model_a and c != model_b][:5]
                print('Committee:', committee)
                    
                save_model_a_name = model_a.replace('/', '_')
                save_model_b_name = model_b.replace('/', '_')

                debate_history_file = f"{round_dir}/{pairing_i}_{save_model_a_name}_{save_model_b_name}_debate_history.jsonl"
                judge_save_file = f"{round_dir}/{pairing_i}_{save_model_a_name}_{save_model_b_name}_judge_results.jsonl"

                # if no file
                if not os.path.exists(debate_history_file):
                    # create file
                    open(debate_history_file, 'w').close()
                    open(judge_save_file, 'w').close()
                    raise Exception('end')
                print('---- Peer Battles ----')
                debates = make_pair_debate_many_questions(model_a, model_b, questions,
                                                          debate_history_file,
                                                          shuffle_ab = args.shuffle_ab,
                                                          language = args.language)

                print('---- Peer Reviews ----')
                evals, elo_scores = peer_evaluate_many_debates(debates, committee, args.judge_debate_rounds,
                                                               judge_save_file,
                                                               initial_score=scores, print_scores = False,
                                                               evaluate_first_turn = args.evaluate_first_turn,
                                                               language = args.language)
                print('Win rates: ')
                print(calculate_win_rate(evals, args.judge_debate_rounds)['overall_win_rate'])
                all_judge_results.extend(evals)
                # scores = elo_scores # update scores

                # raise Exception("Stop here")
            mle_elo, _ = compute_mle_elo(all_judge_results, args.judge_debate_rounds)
            # update scores
            for model in player_names:
                if model in mle_elo:
                    scores[model] = mle_elo[model]
            print('final scores:', scores)
            for model in player_names:
                elo_history[model].append(scores[model])

        elo_history_df = pd.DataFrame.from_dict(elo_history)
        elo_history_df.to_csv(f"{round_dir}/elo_history.csv")
        print(f"Round {round_num+1} Scores sorted: {sorted(player_names, key=lambda p: -scores[p])}")
    
    # Sort players by their final scores for the final ranking
    final_ranking = sorted(player_names, key=lambda p: -scores[p])
    print("Final Ranking:", final_ranking)
    print("Final Scores:", scores)