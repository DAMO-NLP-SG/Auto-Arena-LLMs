This is the repo for paper "Auto-Arena: Automating LLM Evaluations with Agent Peer-battles and Committee Discussions".

## Reproducing the graphs and figures

All code for reproducing the graphs and figures are included in analysis_scripts/result_analysis.ipynb


## How to use the repository to run code

Prepare the environment:
1. Set up the environment using: conda env create -f env.yml
2. Activate the environment with: conda activate LLM_Eval
3. Make sure you have the environment variables listed in utils/api_utils.py

Before including any participants, make sure:
1. The participant's calling function is written in the "generate_response" function inside "utils/api_utils.py".
2. The participant's MMLU score is included in "data/MMLU.csv". If the participant doesn't have an MMLU score, fill in "-1" and it will be initially paired with the median candidate.

**To run a tournament**, first change the "player_names" variable in the python files to adjust the tournament members. Example commands:
1. English: python run_tournament.py --tournament_dir data/main_tour_40
2. Chinese: python run_tournament.py --tournament_dir data/main_tour_40_zh --language zh

**To add a new participant to a finished tournament**, here is an example command:

1. python run_tournament_add_participant.py --tournament_dir data/main_tour_40 --add_participant gemini-1.5-flash-exp-0827

**To run debates between a pair of selected models**, here is an example command:

1. python run_LD_pair.py --model_a Qwen/Qwen1.5-72B-Chat --model_b claude-3-haiku-20240307

We release 2 questions per category as demos for each debate on the website. The full results are not pushed to the website. An analysis including all figures in the papers was run in notebook result_analysis.ipynb.
