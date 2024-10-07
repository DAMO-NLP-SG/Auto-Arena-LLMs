import trueskill
from collections import defaultdict
import numpy as np
import pandas as pd
import math
from sklearn.linear_model import LogisticRegression

# ELO SCORE CALCULATION

def compute_elo(rating, battles, judge_debate_rounds, K=4, SCALE=400, BASE=10):

    if rating is None:
        rating = defaultdict(lambda: 1000)

    # battle loop
    for b in battles:
        _, model_a, model_b = b['gamekey']
        winner = b['final_winner'][judge_debate_rounds]
        ra = rating[model_a]
        rb = rating[model_b]
        ea = 1 / (1 + BASE ** ((rb - ra) / SCALE))
        eb = 1 / (1 + BASE ** ((ra - rb) / SCALE))
        if winner == "A":
            sa = 1
        elif winner == "B":
            sa = 0
        elif winner == "tie":
            sa = 0.5
        else:
            print(f"unexpected vote {winner}")
            continue
        rating[model_a] += K * (sa - ea)
        rating[model_b] += K * (1 - sa - eb)

    return dict(rating)

def update_elo(rating, winner, K=4, SCALE=400, BASE=10):
    ra = rating[winner]
    # average rating
    rb = sum(rating.values())/len(rating)
    ea = 1 / (1 + BASE ** ((rb - ra) / SCALE))
    sa = 1
    rating[winner] += K * (sa - ea)

    return dict(rating)

# WIN-RATE CALCULATION
def calculate_win_rate(evals, judge_debate_rounds):
    final_result = {}

    # win rate calculation
    # model: {num_wins: ; num_matches: }
    overall_wins = defaultdict(lambda: defaultdict(lambda: 0))
    # judge: {model: ; ... ; ties:}
    judge_wins = defaultdict(lambda: defaultdict(lambda: 0))
    agreements = defaultdict(lambda: 0)

    for eval in evals:
        model_a = eval['gamekey'][1]
        model_b = eval['gamekey'][2]

        final_winner = eval['final_winner'][judge_debate_rounds]
        # overall win rate
        if final_winner == 'A':
            overall_wins[model_a]['wins'] += 1
        elif final_winner == 'B':
            overall_wins[model_b]['wins'] += 1
        elif final_winner == 'tie':
            overall_wins[model_a]['ties'] += 1
            overall_wins[model_b]['ties'] += 1
        overall_wins[model_a]['matches'] += 1
        overall_wins[model_b]['matches'] += 1
        
        # per judge win rate and agreement
        judgements = []
        for judge in eval['judges']:
            judge_winner = eval[judge]['winner'][judge_debate_rounds]
            judgements.append(judge_winner)
            if judge_winner == 'A':
                judge_wins[judge][model_a] += 1
            elif judge_winner == 'B':
                judge_wins[judge][model_b] += 1
            else:
                judge_wins[judge]['tie'] += 1

        # check how many are in agreement
        agreements[len(judgements) - len(set(judgements)) + 1] += 1

    final_result['overall_win_rate'] = {}
    for model in overall_wins:
        win_rate = overall_wins[model]['wins']/overall_wins[model]['matches']
        final_result['overall_win_rate'][model] = win_rate

    final_result['judge'] = {}
    for judge in judge_wins:
        final_result['judge'][judge] = {}
        for model in judge_wins[judge]:
            judge_win_rate = judge_wins[judge][model]/len(evals)
            final_result['judge'][judge][model] = judge_win_rate

    final_result['agreement'] = {}
    for agreement in agreements:
        agg = agreements[agreement]/len(evals)
        final_result['agreement'][agreement] = agg
    
    return final_result

def calculate_agreement(evals, judge_debate_rounds):
    # unique judges
    judges = [j for eval in evals for j in eval['judges']]
    judges = list(set(judges))

    pairings = [(a, b) for idx, a in enumerate(judges) for b in judges[idx + 1:]]
    agreements = []
    for (a, b) in pairings:
        agree = 0
        total = 0
        for eval in evals:
            # exclude error
            if a in eval['judges'] and b in eval['judges'] and eval[a]['winner'][judge_debate_rounds] != 'error' and eval[b]['winner'][judge_debate_rounds] != 'error':
                total += 1
                # count ties
                if eval[a]['winner'][judge_debate_rounds] == eval[b]['winner'][judge_debate_rounds]:
                    agree += 1
        agreements.append(agree / total)
    print(f"Probability of two judges agreeing: {np.mean(agreements)}")

# print out the elo ratings and win rates
def print_eval_results(evals, initial_score = None, print_scores = False, judge_debate_rounds = 0):
    # compute elo
    elo_scores = compute_elo(initial_score, evals, judge_debate_rounds)
    # prints win rates
    win_rates = calculate_win_rate(evals, judge_debate_rounds)
    if print_scores:
        print("ELO SCORES")
        for model in elo_scores:
            print(f"{model}: {elo_scores[model]}")
        print("WIN RATES")
        print(win_rates)
        print('MLE ELO: ')
        print(preety_print_model_ratings(compute_mle_elo(evals, judge_debate_rounds)[1]))
    return elo_scores, win_rates

# maxmium likelihood estimation for elo score
def compute_mle_elo(judge_results, judge_debate_rounds, SCALE=400, BASE=10, INIT_RATING=1000):
    model_a = [j['gamekey'][1] for j in judge_results]
    model_b = [j['gamekey'][2] for j in judge_results]
    winner = []
    for j in judge_results:
        try:
            winner.append(j['final_winner'][judge_debate_rounds])
        except:
            print(j)
            raise Exception(f"Missing final_winner")
    df = pd.DataFrame({'model_a': model_a, 'model_b': model_b, 'winner': winner})

    models = pd.concat([df["model_a"], df["model_b"]]).unique()
    models = pd.Series(np.arange(len(models)), index=models)

    # duplicate battles
    df = pd.concat([df, df], ignore_index=True)
    p = len(models.index)
    n = df.shape[0]

    X = np.zeros([n, p])
    X[np.arange(n), models[df["model_a"]]] = +math.log(BASE)
    X[np.arange(n), models[df["model_b"]]] = -math.log(BASE)

    # one A win => two A win
    Y = np.zeros(n)
    Y[df["winner"] == "A"] = 1.0

    # one tie => one A win + one B win
    # find tie + tie (both bad) index
    tie_idx = (df["winner"] == "tie")
    tie_idx[len(tie_idx)//2:] = False
    Y[tie_idx] = 1.0

    lr = LogisticRegression(fit_intercept=False, penalty=None, tol=1e-8)
    lr.fit(X,Y)

    elo_scores = SCALE * lr.coef_[0] + INIT_RATING

    # set anchor as mixtral = 1000
    if "Mixtral-8x7B-Instruct-v0.1" in models.index:
        elo_scores += 1000 - elo_scores[models["mixtral-8x7b-instruct-v0.1"]]
    print_ratings = pd.Series(elo_scores, index = models.index).sort_values(ascending=False)
    dict_ratings = dict(zip(models.index, elo_scores))
    return (dict_ratings, print_ratings)

def preety_print_model_ratings(ratings):
    df = pd.DataFrame([
        [n, ratings[n]] for n in ratings.keys()
    ], columns=["Model", "Elo rating"]).sort_values("Elo rating", ascending=False).reset_index(drop=True)
    # df["Elo rating"] = (df["Elo rating"] + 0.5).astype(int)
    df.index = df.index + 1
    return df