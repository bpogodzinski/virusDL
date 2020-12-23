import json
from datetime import datetime

import ray

from .evaluation.evaluate0_create_result_json import concat_and_sort_results
from .evaluation.evaluate1_hosts_sorted_to_hosts_best import filter_best_hosts
from .evaluation.evaluate2_hits_best_json import evaluate_taxonomy_performance
from .evaluation.evaluate3_true_host_rank_distribution import true_host_rank_distribution
from .evaluation.evaluate4_positive_negative import positive_negative_scores_distribution
from .evaluation.evaluate8_threshold_sens_spec import evaluate_binary_classification
from .evaluation.evaluate9_null_value import evaluate_sorted_hosts
from .evaluation.evaluate10_roc_curve_full import roc_evaluation
from .evaluation.evaluate11_prc import prc_evaluation
from virusDL import RESULT_DIR, CPU_COUNT_LOCAL

ray.init(num_cpus=CPU_COUNT_LOCAL)

def run_evaluation(tests_folder, result_dir = RESULT_DIR / f'eval_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}'):
    
    result_dir.mkdir(parents=True)
    host_sorted = concat_and_sort_results.remote(tests_folder)
    best_hosts = filter_best_hosts.remote(host_sorted)
    tax_performance = evaluate_taxonomy_performance.remote(best_hosts)
    host_rank_distribution, rank_distribution_plot = true_host_rank_distribution.remote(host_sorted)
    scores_distribution, scores_plot = positive_negative_scores_distribution.remote(host_sorted)
    model_evaluation_stats = evaluate_binary_classification.remote(host_sorted)
    host_sorted_info = evaluate_sorted_hosts.remote(host_sorted)
    roc_auc, roc_plot = roc_evaluation.remote(host_sorted, host_sorted_info)
    prc_auc, prc_plot = prc_evaluation.remote(host_sorted, host_sorted_info)

    host_sorted_result = ray.get(host_sorted)
    with open(result_dir / 'host-sorted.json','w') as fd:
        json.dump(host_sorted_result, fd, indent=3)

    best_hosts_result = ray.get(best_hosts)
    with open(result_dir / 'host-best.json','w') as fd:
        json.dump(best_hosts_result, fd, indent=3)

    tax_performance_result = ray.get(tax_performance)
    with open(result_dir / 'tax-performance.json','w') as fd:
        json.dump(tax_performance_result, fd, indent=3)

    host_rank_distribution_result = ray.get(host_rank_distribution)
    with open(result_dir / 'host-rank-distribution.json', 'w') as fd:
        json.dump(host_rank_distribution_result, fd, indent=3)

    host_rank_distribution_plot = ray.get(rank_distribution_plot)
    with open(result_dir / 'host-rank-distribution-plot.png', 'wb') as fd:
        fd.write(host_rank_distribution_plot.getvalue())

    scores_distribution_result = ray.get(scores_distribution)
    with open(result_dir / 'scores-distribution.json', 'w') as fd:
        json.dump(scores_distribution_result, fd, indent=3)

    scores_plot_result = ray.get(scores_plot)
    with open(result_dir / 'scores-plot.png', 'wb') as fd:
        fd.write(scores_plot_result.getvalue())

    model_evaluation_stats_result = ray.get(model_evaluation_stats)
    with open(result_dir / 'model-evaluation-stats.json', 'w') as fd:
        json.dump(model_evaluation_stats_result, fd, indent=3)

    host_sorted_info_result = ray.get(host_sorted_info)
    with open(result_dir / 'host-sorted.info.json', 'w') as fd:
        json.dump(host_sorted_info_result, fd, indent=3)

    roc_auc_result = ray.get(roc_auc)
    with open(result_dir / 'roc-auc.txt', 'w') as fd:
        fd.write(str(roc_auc_result))

    roc_plot_result = ray.get(roc_plot)
    with open(result_dir / 'roc.png', 'wb') as fd:
        fd.write(roc_plot_result.getvalue())

    prc_auc_result = ray.get(prc_auc)
    with open(result_dir / 'prc-auc.txt', 'w') as fd:
        fd.write(str(prc_auc_result))

    prc_plot_result = ray.get(prc_plot)
    with open(result_dir / 'prc.png', 'wb') as fd:
        fd.write(prc_plot_result.getvalue())
