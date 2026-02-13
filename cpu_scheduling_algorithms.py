"""
CPU Scheduling Algorithms Implementation
==========================================
Implements various CPU scheduling algorithms for process management.

Algorithms Implemented:
1. First Come First Serve (FCFS)
2. Shortest Job First (SJF) - Non-preemptive
3. Shortest Remaining Time First (SRTF) - Preemptive
4. Priority Scheduling (PS) - Non-preemptive
5. Priority Scheduling Preemptive (PSP)
6. Round Robin (RR)

Author: AI-Powered Process Scheduling Team
Date: February 2026
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass, field
import copy


@dataclass
class Process:
    """Represents a process in the scheduling system"""
    pid: int  # Process ID
    arrival_time: int  # Time when process arrives
    burst_time: int  # Total CPU time needed
    priority: int = 0  # Priority (lower number = higher priority)
    remaining_time: int = field(init=False)  # Remaining burst time
    completion_time: int = 0  # Time when process completes
    turnaround_time: int = 0  # Completion - Arrival
    waiting_time: int = 0  # Turnaround - Burst
    response_time: int = -1  # First execution - Arrival
    start_time: int = -1  # When process first gets CPU
    
    def __post_init__(self):
        self.remaining_time = self.burst_time
    
    def __repr__(self):
        return f"P{self.pid}(AT={self.arrival_time}, BT={self.burst_time}, P={self.priority})"


@dataclass
class SchedulingResult:
    """Contains results and metrics from scheduling"""
    algorithm: str
    processes: List[Process]
    gantt_chart: List[Tuple[int, int, int]]  # (pid, start_time, end_time)
    avg_waiting_time: float = 0.0
    avg_turnaround_time: float = 0.0
    avg_response_time: float = 0.0
    throughput: float = 0.0
    cpu_utilization: float = 0.0
    total_time: int = 0
    context_switches: int = 0


class CPUScheduler:
    """Main scheduler class implementing various scheduling algorithms"""
    
    def __init__(self, processes: List[Process]):
        """
        Initialize scheduler with list of processes
        
        Args:
            processes: List of Process objects to schedule
        """
        self.original_processes = processes
        self.processes = []
    
    def reset_processes(self):
        """Reset process list to original state"""
        self.processes = [copy.deepcopy(p) for p in self.original_processes]
    
    def calculate_metrics(self, algorithm_name: str, gantt_chart: List[Tuple]) -> SchedulingResult:
        """Calculate performance metrics for scheduled processes"""
        n = len(self.processes)
        total_waiting = sum(p.waiting_time for p in self.processes)
        total_turnaround = sum(p.turnaround_time for p in self.processes)
        total_response = sum(p.response_time for p in self.processes if p.response_time >= 0)
        
        # Calculate total time
        total_time = max(p.completion_time for p in self.processes) if self.processes else 0
        
        # Calculate context switches
        context_switches = len(gantt_chart) - 1
        
        # Calculate CPU utilization
        total_burst = sum(p.burst_time for p in self.processes)
        cpu_utilization = (total_burst / total_time * 100) if total_time > 0 else 0
        
        # Calculate throughput (processes per unit time)
        throughput = n / total_time if total_time > 0 else 0
        
        return SchedulingResult(
            algorithm=algorithm_name,
            processes=self.processes,
            gantt_chart=gantt_chart,
            avg_waiting_time=total_waiting / n if n > 0 else 0,
            avg_turnaround_time=total_turnaround / n if n > 0 else 0,
            avg_response_time=total_response / n if n > 0 else 0,
            throughput=throughput,
            cpu_utilization=cpu_utilization,
            total_time=total_time,
            context_switches=context_switches
        )
    
    # ==================== FCFS ====================
    def fcfs(self) -> SchedulingResult:
        """
        First Come First Serve (FCFS) Scheduling
        - Non-preemptive
        - Processes executed in order of arrival
        """
        self.reset_processes()
        self.processes.sort(key=lambda p: p.arrival_time)
        
        current_time = 0
        gantt_chart = []
        
        for process in self.processes:
            # If CPU is idle, jump to next arrival
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            
            # Record start time and response time
            process.start_time = current_time
            process.response_time = current_time - process.arrival_time
            
            # Execute process
            start = current_time
            current_time += process.burst_time
            gantt_chart.append((process.pid, start, current_time))
            
            # Calculate times
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
        
        return self.calculate_metrics("FCFS", gantt_chart)
    
    # ==================== SJF ====================
    def sjf(self) -> SchedulingResult:
        """
        Shortest Job First (SJF) Scheduling - Non-preemptive
        - Selects process with shortest burst time
        - Non-preemptive: once started, runs to completion
        """
        self.reset_processes()
        
        current_time = 0
        completed = 0
        n = len(self.processes)
        gantt_chart = []
        is_completed = [False] * n
        
        while completed < n:
            # Find process with shortest burst time that has arrived
            idx = -1
            min_burst = float('inf')
            
            for i in range(n):
                if (not is_completed[i] and 
                    self.processes[i].arrival_time <= current_time and
                    self.processes[i].burst_time < min_burst):
                    min_burst = self.processes[i].burst_time
                    idx = i
            
            if idx == -1:
                # No process available, jump to next arrival
                next_arrival = min(
                    p.arrival_time for i, p in enumerate(self.processes) 
                    if not is_completed[i]
                )
                current_time = next_arrival
                continue
            
            process = self.processes[idx]
            
            # Record start and response time
            process.start_time = current_time
            process.response_time = current_time - process.arrival_time
            
            # Execute process
            start = current_time
            current_time += process.burst_time
            gantt_chart.append((process.pid, start, current_time))
            
            # Calculate times
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
            is_completed[idx] = True
            completed += 1
        
        return self.calculate_metrics("SJF", gantt_chart)
    
    # ==================== SRTF ====================
    def srtf(self) -> SchedulingResult:
        """
        Shortest Remaining Time First (SRTF) Scheduling - Preemptive
        - Preemptive version of SJF
        - Always executes process with shortest remaining time
        """
        self.reset_processes()
        
        current_time = 0
        completed = 0
        n = len(self.processes)
        gantt_chart = []
        last_pid = -1
        
        # Get the maximum completion time
        total_burst = sum(p.burst_time for p in self.processes)
        max_arrival = max(p.arrival_time for p in self.processes)
        
        while completed < n:
            # Find process with shortest remaining time
            idx = -1
            min_remaining = float('inf')
            
            for i in range(n):
                if (self.processes[i].arrival_time <= current_time and
                    self.processes[i].remaining_time > 0 and
                    self.processes[i].remaining_time < min_remaining):
                    min_remaining = self.processes[i].remaining_time
                    idx = i
            
            if idx == -1:
                # No process available
                current_time += 1
                continue
            
            process = self.processes[idx]
            
            # Record first execution (response time)
            if process.start_time == -1:
                process.start_time = current_time
                process.response_time = current_time - process.arrival_time
            
            # Execute for 1 time unit
            if last_pid != process.pid:
                if gantt_chart and gantt_chart[-1][0] == process.pid:
                    # Extend last entry
                    gantt_chart[-1] = (process.pid, gantt_chart[-1][1], current_time + 1)
                else:
                    gantt_chart.append((process.pid, current_time, current_time + 1))
                last_pid = process.pid
            else:
                # Extend current execution
                gantt_chart[-1] = (process.pid, gantt_chart[-1][1], current_time + 1)
            
            process.remaining_time -= 1
            current_time += 1
            
            # Check if process completed
            if process.remaining_time == 0:
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                completed += 1
        
        return self.calculate_metrics("SRTF", gantt_chart)
    
    # ==================== Priority Scheduling ====================
    def priority_scheduling(self, preemptive: bool = False) -> SchedulingResult:
        """
        Priority Scheduling
        - Lower priority number = higher priority
        
        Args:
            preemptive: If True, uses preemptive priority scheduling
        """
        self.reset_processes()
        
        if preemptive:
            return self._priority_preemptive()
        else:
            return self._priority_non_preemptive()
    
    def _priority_non_preemptive(self) -> SchedulingResult:
        """Non-preemptive Priority Scheduling"""
        current_time = 0
        completed = 0
        n = len(self.processes)
        gantt_chart = []
        is_completed = [False] * n
        
        while completed < n:
            # Find highest priority process that has arrived
            idx = -1
            highest_priority = float('inf')
            
            for i in range(n):
                if (not is_completed[i] and 
                    self.processes[i].arrival_time <= current_time):
                    if self.processes[i].priority < highest_priority:
                        highest_priority = self.processes[i].priority
                        idx = i
                    elif (self.processes[i].priority == highest_priority and 
                          self.processes[i].arrival_time < self.processes[idx].arrival_time):
                        idx = i
            
            if idx == -1:
                # No process available
                next_arrival = min(
                    p.arrival_time for i, p in enumerate(self.processes) 
                    if not is_completed[i]
                )
                current_time = next_arrival
                continue
            
            process = self.processes[idx]
            
            # Record start and response time
            process.start_time = current_time
            process.response_time = current_time - process.arrival_time
            
            # Execute process
            start = current_time
            current_time += process.burst_time
            gantt_chart.append((process.pid, start, current_time))
            
            # Calculate times
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
            is_completed[idx] = True
            completed += 1
        
        return self.calculate_metrics("Priority (Non-Preemptive)", gantt_chart)
    
    def _priority_preemptive(self) -> SchedulingResult:
        """Preemptive Priority Scheduling"""
        current_time = 0
        completed = 0
        n = len(self.processes)
        gantt_chart = []
        last_pid = -1
        
        while completed < n:
            # Find highest priority process
            idx = -1
            highest_priority = float('inf')
            
            for i in range(n):
                if (self.processes[i].arrival_time <= current_time and
                    self.processes[i].remaining_time > 0):
                    if self.processes[i].priority < highest_priority:
                        highest_priority = self.processes[i].priority
                        idx = i
                    elif (self.processes[i].priority == highest_priority and
                          self.processes[i].arrival_time < self.processes[idx].arrival_time):
                        idx = i
            
            if idx == -1:
                current_time += 1
                continue
            
            process = self.processes[idx]
            
            # Record first execution
            if process.start_time == -1:
                process.start_time = current_time
                process.response_time = current_time - process.arrival_time
            
            # Execute for 1 time unit
            if last_pid != process.pid:
                if gantt_chart and gantt_chart[-1][0] == process.pid:
                    gantt_chart[-1] = (process.pid, gantt_chart[-1][1], current_time + 1)
                else:
                    gantt_chart.append((process.pid, current_time, current_time + 1))
                last_pid = process.pid
            else:
                gantt_chart[-1] = (process.pid, gantt_chart[-1][1], current_time + 1)
            
            process.remaining_time -= 1
            current_time += 1
            
            if process.remaining_time == 0:
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                completed += 1
        
        return self.calculate_metrics("Priority (Preemptive)", gantt_chart)
    
    # ==================== Round Robin ====================
    def round_robin(self, time_quantum: int = 2) -> SchedulingResult:
        """
        Round Robin (RR) Scheduling
        - Each process gets a fixed time quantum
        - Preemptive scheduling
        
        Args:
            time_quantum: Time slice for each process
        """
        self.reset_processes()
        
        current_time = 0
        queue = []
        gantt_chart = []
        n = len(self.processes)
        completed = 0
        visited = [False] * n
        
        # Add processes that have arrived at time 0
        for i, p in enumerate(self.processes):
            if p.arrival_time == 0:
                queue.append(i)
                visited[i] = True
        
        while completed < n or queue:
            if not queue:
                # Jump to next arrival
                next_arrival = min(
                    p.arrival_time for i, p in enumerate(self.processes)
                    if not visited[i]
                )
                current_time = next_arrival
                for i, p in enumerate(self.processes):
                    if p.arrival_time <= current_time and not visited[i]:
                        queue.append(i)
                        visited[i] = True
                continue
            
            idx = queue.pop(0)
            process = self.processes[idx]
            
            # Record first execution
            if process.start_time == -1:
                process.start_time = current_time
                process.response_time = current_time - process.arrival_time
            
            # Execute for time quantum or remaining time
            exec_time = min(time_quantum, process.remaining_time)
            start = current_time
            current_time += exec_time
            gantt_chart.append((process.pid, start, current_time))
            
            process.remaining_time -= exec_time
            
            # Add newly arrived processes to queue
            for i, p in enumerate(self.processes):
                if (p.arrival_time <= current_time and 
                    not visited[i] and 
                    p.remaining_time > 0):
                    queue.append(i)
                    visited[i] = True
            
            # If process not finished, add back to queue
            if process.remaining_time > 0:
                queue.append(idx)
            else:
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                completed += 1
        
        return self.calculate_metrics(f"Round Robin (Q={time_quantum})", gantt_chart)


def print_gantt_chart(result: SchedulingResult):
    """Print a visual Gantt chart"""
    print(f"\n{'='*60}")
    print(f"Gantt Chart for {result.algorithm}")
    print(f"{'='*60}")
    
    # Print timeline
    print("|", end="")
    for pid, start, end in result.gantt_chart:
        width = end - start
        print(f" P{pid} ".center(width * 3) + "|", end="")
    print()
    
    # Print time markers
    print(result.gantt_chart[0][1], end="")
    for pid, start, end in result.gantt_chart:
        width = end - start
        print(" " * (width * 3 - len(str(end))) + str(end), end="")
    print()


def print_process_table(result: SchedulingResult):
    """Print detailed process information table"""
    print(f"\n{'='*90}")
    print(f"Process Details for {result.algorithm}")
    print(f"{'='*90}")
    print(f"{'PID':<5} {'AT':<5} {'BT':<5} {'CT':<5} {'TAT':<5} {'WT':<5} {'RT':<5} {'Priority':<10}")
    print(f"{'-'*90}")
    
    for p in sorted(result.processes, key=lambda x: x.pid):
        print(f"{p.pid:<5} {p.arrival_time:<5} {p.burst_time:<5} "
              f"{p.completion_time:<5} {p.turnaround_time:<5} "
              f"{p.waiting_time:<5} {p.response_time:<5} {p.priority:<10}")
    
    print(f"{'-'*90}")
    print(f"\nAverage Waiting Time: {result.avg_waiting_time:.2f}")
    print(f"Average Turnaround Time: {result.avg_turnaround_time:.2f}")
    print(f"Average Response Time: {result.avg_response_time:.2f}")
    print(f"Throughput: {result.throughput:.4f} processes/unit time")
    print(f"CPU Utilization: {result.cpu_utilization:.2f}%")
    print(f"Context Switches: {result.context_switches}")
    print(f"Total Time: {result.total_time}")


def print_comparison(results: List[SchedulingResult]):
    """Print comparison of all algorithms"""
    print(f"\n{'='*100}")
    print(f"SCHEDULING ALGORITHMS COMPARISON")
    print(f"{'='*100}")
    print(f"{'Algorithm':<30} {'Avg WT':<10} {'Avg TAT':<10} {'Avg RT':<10} "
          f"{'Throughput':<12} {'CPU %':<8} {'CS':<5}")
    print(f"{'-'*100}")
    
    for result in results:
        print(f"{result.algorithm:<30} {result.avg_waiting_time:<10.2f} "
              f"{result.avg_turnaround_time:<10.2f} {result.avg_response_time:<10.2f} "
              f"{result.throughput:<12.4f} {result.cpu_utilization:<8.2f} "
              f"{result.context_switches:<5}")
    
    print(f"{'='*100}")
    print("\nLegend:")
    print("  Avg WT  = Average Waiting Time")
    print("  Avg TAT = Average Turnaround Time")
    print("  Avg RT  = Average Response Time")
    print("  CPU %   = CPU Utilization")
    print("  CS      = Context Switches")


# Example usage
if __name__ == "__main__":
    # Sample processes
    processes = [
        Process(pid=1, arrival_time=0, burst_time=5, priority=2),
        Process(pid=2, arrival_time=1, burst_time=3, priority=1),
        Process(pid=3, arrival_time=2, burst_time=8, priority=3),
        Process(pid=4, arrival_time=3, burst_time=6, priority=4),
    ]
    
    scheduler = CPUScheduler(processes)
    
    # Run all algorithms
    results = []
    
    print("Running FCFS...")
    results.append(scheduler.fcfs())
    
    print("Running SJF...")
    results.append(scheduler.sjf())
    
    print("Running SRTF...")
    results.append(scheduler.srtf())
    
    print("Running Priority (Non-Preemptive)...")
    results.append(scheduler.priority_scheduling(preemptive=False))
    
    print("Running Priority (Preemptive)...")
    results.append(scheduler.priority_scheduling(preemptive=True))
    
    print("Running Round Robin (Q=2)...")
    results.append(scheduler.round_robin(time_quantum=2))
    
    # Display results
    for result in results:
        print_gantt_chart(result)
        print_process_table(result)
    
    # Final comparison
    print_comparison(results)
