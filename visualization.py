"""
Visualization Module for CPU Scheduling
========================================
Creates visual representations of scheduling results

Features:
- Gantt charts
- Performance comparison charts
- Timeline visualizations
- Export capabilities
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import List, Dict
import numpy as np
from cpu_scheduling_algorithms import SchedulingResult, Process


class SchedulingVisualizer:
    """Visualize scheduling algorithm results"""
    
    def __init__(self, figsize=(12, 6)):
        """
        Initialize visualizer
        
        Args:
            figsize: Default figure size for plots
        """
        self.figsize = figsize
        self.colors = plt.cm.Set3(np.linspace(0, 1, 20))
    
    def plot_gantt_chart(self, result: SchedulingResult, save_path: str = None):
        """
        Create a visual Gantt chart
        
        Args:
            result: SchedulingResult object
            save_path: Optional path to save figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Create color map for processes
        unique_pids = sorted(set(pid for pid, _, _ in result.gantt_chart))
        color_map = {pid: self.colors[i % len(self.colors)] 
                    for i, pid in enumerate(unique_pids)}
        
        # Draw rectangles for each execution
        for pid, start, end in result.gantt_chart:
            duration = end - start
            rect = mpatches.Rectangle((start, pid - 0.4), duration, 0.8,
                                      facecolor=color_map[pid],
                                      edgecolor='black', linewidth=1.5)
            ax.add_patch(rect)
            
            # Add process label
            ax.text(start + duration/2, pid, f'P{pid}',
                   ha='center', va='center', fontweight='bold', fontsize=10)
        
        # Set labels and title
        ax.set_xlabel('Time', fontsize=12, fontweight='bold')
        ax.set_ylabel('Process ID', fontsize=12, fontweight='bold')
        ax.set_title(f'Gantt Chart - {result.algorithm}', 
                    fontsize=14, fontweight='bold', pad=20)
        
        # Set axis limits
        ax.set_xlim(0, result.total_time)
        ax.set_ylim(min(unique_pids) - 1, max(unique_pids) + 1)
        
        # Set y-ticks to process IDs
        ax.set_yticks(unique_pids)
        ax.set_yticklabels([f'P{pid}' for pid in unique_pids])
        
        # Grid
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add statistics text box
        stats_text = (f'Avg Waiting Time: {result.avg_waiting_time:.2f}\n'
                     f'Avg Turnaround Time: {result.avg_turnaround_time:.2f}\n'
                     f'CPU Utilization: {result.cpu_utilization:.2f}%\n'
                     f'Context Switches: {result.context_switches}')
        
        ax.text(1.02, 0.5, stats_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='center',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Gantt chart saved to {save_path}")
        
        plt.show()
    
    def plot_metrics_comparison(self, results: List[SchedulingResult], 
                               save_path: str = None):
        """
        Compare metrics across different algorithms
        
        Args:
            results: List of SchedulingResult objects
            save_path: Optional path to save figure
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        algorithms = [r.algorithm for r in results]
        
        # Average Waiting Time
        ax = axes[0, 0]
        waiting_times = [r.avg_waiting_time for r in results]
        bars = ax.bar(range(len(algorithms)), waiting_times, 
                     color=self.colors[:len(algorithms)])
        ax.set_xticks(range(len(algorithms)))
        ax.set_xticklabels(algorithms, rotation=45, ha='right')
        ax.set_ylabel('Time Units', fontweight='bold')
        ax.set_title('Average Waiting Time', fontweight='bold', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for i, (bar, val) in enumerate(zip(bars, waiting_times)):
            ax.text(bar.get_x() + bar.get_width()/2, val,
                   f'{val:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # Average Turnaround Time
        ax = axes[0, 1]
        turnaround_times = [r.avg_turnaround_time for r in results]
        bars = ax.bar(range(len(algorithms)), turnaround_times,
                     color=self.colors[:len(algorithms)])
        ax.set_xticks(range(len(algorithms)))
        ax.set_xticklabels(algorithms, rotation=45, ha='right')
        ax.set_ylabel('Time Units', fontweight='bold')
        ax.set_title('Average Turnaround Time', fontweight='bold', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        
        for i, (bar, val) in enumerate(zip(bars, turnaround_times)):
            ax.text(bar.get_x() + bar.get_width()/2, val,
                   f'{val:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # CPU Utilization
        ax = axes[1, 0]
        cpu_utils = [r.cpu_utilization for r in results]
        bars = ax.bar(range(len(algorithms)), cpu_utils,
                     color=self.colors[:len(algorithms)])
        ax.set_xticks(range(len(algorithms)))
        ax.set_xticklabels(algorithms, rotation=45, ha='right')
        ax.set_ylabel('Percentage (%)', fontweight='bold')
        ax.set_title('CPU Utilization', fontweight='bold', fontsize=12)
        ax.set_ylim(0, 105)
        ax.grid(True, alpha=0.3, axis='y')
        
        for i, (bar, val) in enumerate(zip(bars, cpu_utils)):
            ax.text(bar.get_x() + bar.get_width()/2, val,
                   f'{val:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # Context Switches
        ax = axes[1, 1]
        context_switches = [r.context_switches for r in results]
        bars = ax.bar(range(len(algorithms)), context_switches,
                     color=self.colors[:len(algorithms)])
        ax.set_xticks(range(len(algorithms)))
        ax.set_xticklabels(algorithms, rotation=45, ha='right')
        ax.set_ylabel('Count', fontweight='bold')
        ax.set_title('Context Switches', fontweight='bold', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        
        for i, (bar, val) in enumerate(zip(bars, context_switches)):
            ax.text(bar.get_x() + bar.get_width()/2, val,
                   f'{val}', ha='center', va='bottom', fontweight='bold')
        
        plt.suptitle('Scheduling Algorithms Performance Comparison',
                    fontsize=16, fontweight='bold', y=1.00)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Comparison chart saved to {save_path}")
        
        plt.show()
    
    def plot_process_timeline(self, result: SchedulingResult, save_path: str = None):
        """
        Create a timeline showing when each process was waiting/executing
        
        Args:
            result: SchedulingResult object
            save_path: Optional path to save figure
        """
        fig, ax = plt.subplots(figsize=(14, 6))
        
        processes = sorted(result.processes, key=lambda p: p.pid)
        color_map = {p.pid: self.colors[i % len(self.colors)] 
                    for i, p in enumerate(processes)}
        
        for i, process in enumerate(processes):
            # Waiting periods
            waiting_start = process.arrival_time
            
            # Find all execution periods for this process
            exec_periods = [(start, end) for pid, start, end in result.gantt_chart 
                          if pid == process.pid]
            
            for exec_start, exec_end in exec_periods:
                # Waiting period before this execution
                if waiting_start < exec_start:
                    ax.barh(i, exec_start - waiting_start, left=waiting_start,
                           height=0.6, color='lightgray', edgecolor='black',
                           linewidth=0.5, label='Waiting' if i == 0 else '')
                
                # Execution period
                ax.barh(i, exec_end - exec_start, left=exec_start,
                       height=0.6, color=color_map[process.pid],
                       edgecolor='black', linewidth=1,
                       label='Executing' if i == 0 else '')
                
                waiting_start = exec_end
        
        # Labels
        ax.set_xlabel('Time', fontsize=12, fontweight='bold')
        ax.set_ylabel('Process', fontsize=12, fontweight='bold')
        ax.set_title(f'Process Timeline - {result.algorithm}',
                    fontsize=14, fontweight='bold')
        ax.set_yticks(range(len(processes)))
        ax.set_yticklabels([f'P{p.pid}' for p in processes])
        ax.set_xlim(0, result.total_time)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Legend
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc='upper right')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Timeline saved to {save_path}")
        
        plt.show()
    
    def plot_all_gantt_charts(self, results: List[SchedulingResult], 
                            save_dir: str = None):
        """
        Create Gantt charts for all algorithms in a grid
        
        Args:
            results: List of SchedulingResult objects
            save_dir: Optional directory to save figures
        """
        n = len(results)
        rows = (n + 1) // 2
        cols = 2 if n > 1 else 1
        
        fig, axes = plt.subplots(rows, cols, figsize=(16, 4 * rows))
        if n == 1:
            axes = [axes]
        else:
            axes = axes.flatten()
        
        for idx, result in enumerate(results):
            ax = axes[idx]
            
            unique_pids = sorted(set(pid for pid, _, _ in result.gantt_chart))
            color_map = {pid: self.colors[i % len(self.colors)] 
                        for i, pid in enumerate(unique_pids)}
            
            # Draw rectangles
            for pid, start, end in result.gantt_chart:
                duration = end - start
                rect = mpatches.Rectangle((start, pid - 0.4), duration, 0.8,
                                          facecolor=color_map[pid],
                                          edgecolor='black', linewidth=1)
                ax.add_patch(rect)
                ax.text(start + duration/2, pid, f'P{pid}',
                       ha='center', va='center', fontweight='bold', fontsize=8)
            
            ax.set_xlabel('Time', fontweight='bold')
            ax.set_ylabel('Process ID', fontweight='bold')
            ax.set_title(result.algorithm, fontweight='bold', fontsize=11)
            ax.set_xlim(0, result.total_time)
            ax.set_ylim(min(unique_pids) - 1, max(unique_pids) + 1)
            ax.set_yticks(unique_pids)
            ax.set_yticklabels([f'P{pid}' for pid in unique_pids])
            ax.grid(True, alpha=0.3, axis='x')
        
        # Hide unused subplots
        for idx in range(len(results), len(axes)):
            axes[idx].axis('off')
        
        plt.suptitle('Gantt Charts - All Algorithms',
                    fontsize=16, fontweight='bold', y=1.00)
        plt.tight_layout()
        
        if save_dir:
            save_path = f"{save_dir}/all_gantt_charts.png"
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"All Gantt charts saved to {save_path}")
        
        plt.show()


# Example usage
if __name__ == "__main__":
    from cpu_scheduling_algorithms import CPUScheduler, Process
    
    # Create sample processes
    processes = [
        Process(pid=1, arrival_time=0, burst_time=5, priority=2),
        Process(pid=2, arrival_time=1, burst_time=3, priority=1),
        Process(pid=3, arrival_time=2, burst_time=8, priority=3),
        Process(pid=4, arrival_time=3, burst_time=6, priority=4),
    ]
    
    scheduler = CPUScheduler(processes)
    visualizer = SchedulingVisualizer()
    
    # Run algorithms
    results = [
        scheduler.fcfs(),
        scheduler.sjf(),
        scheduler.srtf(),
        scheduler.priority_scheduling(preemptive=False),
        scheduler.round_robin(time_quantum=2),
    ]
    
    # Create visualizations
    print("Creating visualizations...")
    
    # Individual Gantt chart
    visualizer.plot_gantt_chart(results[0])
    
    # Metrics comparison
    visualizer.plot_metrics_comparison(results)
    
    # Process timeline
    visualizer.plot_process_timeline(results[0])
    
    # All Gantt charts
    visualizer.plot_all_gantt_charts(results)
