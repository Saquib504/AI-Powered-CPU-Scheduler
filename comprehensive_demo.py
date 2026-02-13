"""
Comprehensive Demo for CPU Scheduling Project
==============================================
Complete demonstration of all scheduling algorithms with multiple test cases

This script demonstrates:
1. All 6 scheduling algorithms
2. Multiple test datasets
3. Performance comparison
4. Visual outputs
"""

from cpu_scheduling_algorithms import (
    CPUScheduler, Process, SchedulingResult,
    print_gantt_chart, print_process_table, print_comparison
)
from dataset_generator import DatasetGenerator, print_dataset_summary
from visualization import SchedulingVisualizer
import os


def demo_basic_example():
    """Demo 1: Basic example with 4 processes"""
    print("\n" + "="*80)
    print("DEMO 1: BASIC EXAMPLE WITH 4 PROCESSES")
    print("="*80)
    
    processes = [
        Process(pid=1, arrival_time=0, burst_time=5, priority=2),
        Process(pid=2, arrival_time=1, burst_time=3, priority=1),
        Process(pid=3, arrival_time=2, burst_time=8, priority=3),
        Process(pid=4, arrival_time=3, burst_time=6, priority=4),
    ]
    
    print("\nInput Processes:")
    print(f"{'PID':<5} {'Arrival Time':<15} {'Burst Time':<15} {'Priority':<10}")
    print("-" * 50)
    for p in processes:
        print(f"{p.pid:<5} {p.arrival_time:<15} {p.burst_time:<15} {p.priority:<10}")
    
    scheduler = CPUScheduler(processes)
    
    # Run all algorithms
    results = []
    
    print("\n" + "-"*80)
    print("Running FCFS (First Come First Serve)...")
    fcfs_result = scheduler.fcfs()
    results.append(fcfs_result)
    print_gantt_chart(fcfs_result)
    
    print("\n" + "-"*80)
    print("Running SJF (Shortest Job First - Non-preemptive)...")
    sjf_result = scheduler.sjf()
    results.append(sjf_result)
    print_gantt_chart(sjf_result)
    
    print("\n" + "-"*80)
    print("Running SRTF (Shortest Remaining Time First - Preemptive)...")
    srtf_result = scheduler.srtf()
    results.append(srtf_result)
    print_gantt_chart(srtf_result)
    
    print("\n" + "-"*80)
    print("Running Priority Scheduling (Non-preemptive)...")
    priority_result = scheduler.priority_scheduling(preemptive=False)
    results.append(priority_result)
    print_gantt_chart(priority_result)
    
    print("\n" + "-"*80)
    print("Running Priority Scheduling (Preemptive)...")
    priority_p_result = scheduler.priority_scheduling(preemptive=True)
    results.append(priority_p_result)
    print_gantt_chart(priority_p_result)
    
    print("\n" + "-"*80)
    print("Running Round Robin (Time Quantum = 2)...")
    rr_result = scheduler.round_robin(time_quantum=2)
    results.append(rr_result)
    print_gantt_chart(rr_result)
    
    # Print detailed results for one algorithm
    print("\n" + "="*80)
    print("DETAILED RESULTS FOR FCFS")
    print("="*80)
    print_process_table(fcfs_result)
    
    # Final comparison
    print_comparison(results)
    
    return results


def demo_textbook_examples():
    """Demo 2: Classic textbook examples"""
    print("\n" + "="*80)
    print("DEMO 2: TEXTBOOK EXAMPLES")
    print("="*80)
    
    # Example 1: SJF advantage
    print("\n--- Example 1: SJF vs FCFS (SJF advantage) ---")
    processes = [
        Process(pid=1, arrival_time=0, burst_time=8, priority=1),
        Process(pid=2, arrival_time=1, burst_time=4, priority=2),
        Process(pid=3, arrival_time=2, burst_time=2, priority=3),
        Process(pid=4, arrival_time=3, burst_time=1, priority=4),
    ]
    
    scheduler = CPUScheduler(processes)
    fcfs = scheduler.fcfs()
    sjf = scheduler.sjf()
    
    print(f"\nFCFS - Avg Waiting Time: {fcfs.avg_waiting_time:.2f}")
    print(f"SJF  - Avg Waiting Time: {sjf.avg_waiting_time:.2f}")
    print(f"Improvement: {((fcfs.avg_waiting_time - sjf.avg_waiting_time) / fcfs.avg_waiting_time * 100):.1f}%")
    
    # Example 2: Round Robin time quantum comparison
    print("\n--- Example 2: Round Robin - Effect of Time Quantum ---")
    processes = [
        Process(pid=1, arrival_time=0, burst_time=10, priority=1),
        Process(pid=2, arrival_time=0, burst_time=5, priority=2),
        Process(pid=3, arrival_time=0, burst_time=8, priority=3),
    ]
    
    scheduler = CPUScheduler(processes)
    
    for quantum in [1, 2, 4]:
        rr = scheduler.round_robin(time_quantum=quantum)
        print(f"\nTime Quantum = {quantum}:")
        print(f"  Avg Waiting Time: {rr.avg_waiting_time:.2f}")
        print(f"  Context Switches: {rr.context_switches}")
    
    # Example 3: Priority Inversion scenario
    print("\n--- Example 3: Priority Scheduling ---")
    processes = [
        Process(pid=1, arrival_time=0, burst_time=4, priority=3),  # Low priority
        Process(pid=2, arrival_time=1, burst_time=2, priority=1),  # High priority
        Process(pid=3, arrival_time=2, burst_time=8, priority=2),  # Medium priority
    ]
    
    scheduler = CPUScheduler(processes)
    non_preemptive = scheduler.priority_scheduling(preemptive=False)
    preemptive = scheduler.priority_scheduling(preemptive=True)
    
    print(f"\nNon-Preemptive Priority:")
    print(f"  P2 (highest priority) completes at: {[p for p in non_preemptive.processes if p.pid == 2][0].completion_time}")
    print(f"\nPreemptive Priority:")
    print(f"  P2 (highest priority) completes at: {[p for p in preemptive.processes if p.pid == 2][0].completion_time}")


def demo_different_datasets():
    """Demo 3: Test with different workload types"""
    print("\n" + "="*80)
    print("DEMO 3: DIFFERENT WORKLOAD TYPES")
    print("="*80)
    
    generator = DatasetGenerator(seed=42)
    
    datasets = {
        'Uniform Distribution': generator.generate_uniform(10),
        'Burst Heavy': generator.generate_burst_heavy(10),
        'I/O Intensive': generator.generate_io_intensive(10),
        'Mixed Workload': generator.generate_mixed_workload(12),
    }
    
    all_results = {}
    
    for dataset_name, processes in datasets.items():
        print(f"\n{'-'*80}")
        print(f"Testing with: {dataset_name}")
        print(f"{'-'*80}")
        
        print_dataset_summary(processes, dataset_name)
        
        scheduler = CPUScheduler(processes)
        
        # Test all algorithms
        results = [
            scheduler.fcfs(),
            scheduler.sjf(),
            scheduler.srtf(),
            scheduler.round_robin(time_quantum=3),
        ]
        
        all_results[dataset_name] = results
        
        # Quick comparison
        print(f"\n{'Algorithm':<30} {'Avg WT':<10} {'Avg TAT':<10}")
        print("-" * 50)
        for r in results:
            print(f"{r.algorithm:<30} {r.avg_waiting_time:<10.2f} {r.avg_turnaround_time:<10.2f}")
    
    return all_results


def demo_best_and_worst_cases():
    """Demo 4: Show best and worst case scenarios for each algorithm"""
    print("\n" + "="*80)
    print("DEMO 4: BEST AND WORST CASE SCENARIOS")
    print("="*80)
    
    # FCFS: Best case - processes arrive in order of shortest burst
    print("\n--- FCFS Best Case: Processes arrive in shortest-burst order ---")
    best_fcfs = [
        Process(pid=1, arrival_time=0, burst_time=2, priority=1),
        Process(pid=2, arrival_time=1, burst_time=4, priority=2),
        Process(pid=3, arrival_time=2, burst_time=6, priority=3),
        Process(pid=4, arrival_time=3, burst_time=8, priority=4),
    ]
    
    # FCFS: Worst case - longest job arrives first
    print("\n--- FCFS Worst Case: Longest job arrives first ---")
    worst_fcfs = [
        Process(pid=1, arrival_time=0, burst_time=20, priority=1),
        Process(pid=2, arrival_time=1, burst_time=2, priority=2),
        Process(pid=3, arrival_time=2, burst_time=3, priority=3),
        Process(pid=4, arrival_time=3, burst_time=4, priority=4),
    ]
    
    scheduler_best = CPUScheduler(best_fcfs)
    scheduler_worst = CPUScheduler(worst_fcfs)
    
    best_result = scheduler_best.fcfs()
    worst_result = scheduler_worst.fcfs()
    
    print(f"\nBest Case - Avg Waiting Time: {best_result.avg_waiting_time:.2f}")
    print(f"Worst Case - Avg Waiting Time: {worst_result.avg_waiting_time:.2f}")
    print(f"Difference: {worst_result.avg_waiting_time - best_result.avg_waiting_time:.2f}")
    
    # Round Robin: Show convoy effect
    print("\n--- Round Robin: Convoy Effect ---")
    convoy = [
        Process(pid=1, arrival_time=0, burst_time=20, priority=1),  # CPU-bound
        Process(pid=2, arrival_time=0, burst_time=1, priority=2),   # I/O-bound
        Process(pid=3, arrival_time=0, burst_time=1, priority=3),   # I/O-bound
    ]
    
    scheduler_convoy = CPUScheduler(convoy)
    
    for quantum in [1, 5, 10]:
        rr = scheduler_convoy.round_robin(time_quantum=quantum)
        io_avg = sum(p.waiting_time for p in rr.processes if p.pid in [2, 3]) / 2
        print(f"\nTime Quantum = {quantum}:")
        print(f"  I/O processes avg waiting: {io_avg:.2f}")
        print(f"  Context switches: {rr.context_switches}")


def demo_performance_metrics():
    """Demo 5: Detailed performance metrics analysis"""
    print("\n" + "="*80)
    print("DEMO 5: PERFORMANCE METRICS ANALYSIS")
    print("="*80)
    
    processes = [
        Process(pid=1, arrival_time=0, burst_time=6, priority=2),
        Process(pid=2, arrival_time=2, burst_time=2, priority=1),
        Process(pid=3, arrival_time=4, burst_time=8, priority=3),
        Process(pid=4, arrival_time=6, burst_time=3, priority=2),
        Process(pid=5, arrival_time=8, burst_time=4, priority=4),
    ]
    
    scheduler = CPUScheduler(processes)
    
    algorithms = {
        'FCFS': scheduler.fcfs(),
        'SJF': scheduler.sjf(),
        'SRTF': scheduler.srtf(),
        'Priority': scheduler.priority_scheduling(preemptive=False),
        'RR (Q=2)': scheduler.round_robin(time_quantum=2),
        'RR (Q=4)': scheduler.round_robin(time_quantum=4),
    }
    
    print("\nDetailed Metrics Comparison:")
    print(f"\n{'Metric':<30} {'Best Algorithm':<20} {'Value':<10}")
    print("-" * 60)
    
    # Find best for each metric
    metrics = {
        'Average Waiting Time': ('avg_waiting_time', 'min'),
        'Average Turnaround Time': ('avg_turnaround_time', 'min'),
        'Average Response Time': ('avg_response_time', 'min'),
        'CPU Utilization': ('cpu_utilization', 'max'),
        'Throughput': ('throughput', 'max'),
        'Context Switches': ('context_switches', 'min'),
    }
    
    for metric_name, (attr, best_type) in metrics.items():
        values = {name: getattr(result, attr) for name, result in algorithms.items()}
        
        if best_type == 'min':
            best_algo = min(values, key=values.get)
            best_value = values[best_algo]
        else:
            best_algo = max(values, key=values.get)
            best_value = values[best_algo]
        
        print(f"{metric_name:<30} {best_algo:<20} {best_value:<10.2f}")
    
    # Show all results
    results_list = list(algorithms.values())
    print_comparison(results_list)


def generate_report_data():
    """Generate data for Monday report"""
    print("\n" + "="*80)
    print("GENERATING DATA FOR MONDAY REPORT")
    print("="*80)
    
    # Create output directory
    os.makedirs('/mnt/user-data/outputs/report_data', exist_ok=True)
    
    # Generate multiple datasets
    generator = DatasetGenerator(seed=42)
    
    print("\nGenerating datasets...")
    datasets = generator.generate_all_datasets('/mnt/user-data/outputs/report_data')
    
    # Run comprehensive tests
    print("\nRunning comprehensive tests on all datasets...")
    
    summary_results = []
    
    for dataset_name, processes in datasets.items():
        print(f"\nProcessing: {dataset_name}")
        scheduler = CPUScheduler(processes)
        
        results = {
            'Dataset': dataset_name,
            'Num_Processes': len(processes),
            'FCFS_WT': scheduler.fcfs().avg_waiting_time,
            'SJF_WT': scheduler.sjf().avg_waiting_time,
            'SRTF_WT': scheduler.srtf().avg_waiting_time,
            'Priority_WT': scheduler.priority_scheduling(preemptive=False).avg_waiting_time,
            'RR_WT': scheduler.round_robin(time_quantum=3).avg_waiting_time,
        }
        
        summary_results.append(results)
    
    # Save summary
    import csv
    summary_file = '/mnt/user-data/outputs/report_data/algorithm_comparison_summary.csv'
    
    with open(summary_file, 'w', newline='') as f:
        fieldnames = ['Dataset', 'Num_Processes', 'FCFS_WT', 'SJF_WT', 
                     'SRTF_WT', 'Priority_WT', 'RR_WT']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_results)
    
    print(f"\nSummary saved to: {summary_file}")
    
    # Print summary table
    print("\n" + "="*100)
    print("ALGORITHM COMPARISON SUMMARY")
    print("="*100)
    print(f"{'Dataset':<20} {'Processes':<12} {'FCFS':<10} {'SJF':<10} "
          f"{'SRTF':<10} {'Priority':<10} {'RR':<10}")
    print("-" * 100)
    
    for result in summary_results:
        print(f"{result['Dataset']:<20} {result['Num_Processes']:<12} "
              f"{result['FCFS_WT']:<10.2f} {result['SJF_WT']:<10.2f} "
              f"{result['SRTF_WT']:<10.2f} {result['Priority_WT']:<10.2f} "
              f"{result['RR_WT']:<10.2f}")
    
    print("="*100)
    print("\nAll report data saved to: /mnt/user-data/outputs/report_data/")


def main():
    """Run all demos"""
    print("\n" + "#"*80)
    print("#" + " "*78 + "#")
    print("#" + "COMPREHENSIVE CPU SCHEDULING ALGORITHMS DEMONSTRATION".center(78) + "#")
    print("#" + " "*78 + "#")
    print("#"*80)
    
    # Run all demos
    try:
        demo_basic_example()
        input("\nPress Enter to continue to next demo...")
        
        demo_textbook_examples()
        input("\nPress Enter to continue to next demo...")
        
        demo_different_datasets()
        input("\nPress Enter to continue to next demo...")
        
        demo_best_and_worst_cases()
        input("\nPress Enter to continue to next demo...")
        
        demo_performance_metrics()
        input("\nPress Enter to generate report data...")
        
        generate_report_data()
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    
    print("\n" + "="*80)
    print("DEMO COMPLETE!")
    print("="*80)
    print("\nAll scheduling algorithms have been demonstrated.")
    print("Check /mnt/user-data/outputs/report_data/ for generated datasets and results.")
    print("\nYou can now:")
    print("1. Review the generated CSV files")
    print("2. Use the visualization module to create charts")
    print("3. Run individual algorithms with custom datasets")
    print("4. Present the comparison results to your supervisor")


if __name__ == "__main__":
    main()
