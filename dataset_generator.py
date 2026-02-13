"""
Dataset Generator for CPU Scheduling
=====================================
Generates synthetic process datasets for testing scheduling algorithms

Features:
- Random process generation
- Configurable parameters
- Export to CSV
- Multiple dataset types (uniform, variable, burst-heavy, etc.)
"""

import random
import csv
from typing import List, Dict
from cpu_scheduling_algorithms import Process


class DatasetGenerator:
    """Generate process datasets for scheduling algorithms"""
    
    def __init__(self, seed: int = 42):
        """
        Initialize generator
        
        Args:
            seed: Random seed for reproducibility
        """
        random.seed(seed)
    
    def generate_uniform(self, 
                        num_processes: int = 10,
                        max_arrival: int = 20,
                        max_burst: int = 15,
                        max_priority: int = 5) -> List[Process]:
        """
        Generate processes with uniform random distribution
        
        Args:
            num_processes: Number of processes to generate
            max_arrival: Maximum arrival time
            max_burst: Maximum burst time
            max_priority: Maximum priority value
        
        Returns:
            List of Process objects
        """
        processes = []
        for i in range(1, num_processes + 1):
            arrival = random.randint(0, max_arrival)
            burst = random.randint(1, max_burst)
            priority = random.randint(1, max_priority)
            
            processes.append(Process(
                pid=i,
                arrival_time=arrival,
                burst_time=burst,
                priority=priority
            ))
        
        return processes
    
    def generate_burst_heavy(self,
                           num_processes: int = 10,
                           max_arrival: int = 10) -> List[Process]:
        """
        Generate processes with varying burst times (some very long)
        Useful for testing SJF and SRTF
        """
        processes = []
        for i in range(1, num_processes + 1):
            arrival = random.randint(0, max_arrival)
            
            # 30% chance of long burst, 70% short
            if random.random() < 0.3:
                burst = random.randint(15, 30)  # Long processes
            else:
                burst = random.randint(1, 8)   # Short processes
            
            priority = random.randint(1, 5)
            
            processes.append(Process(
                pid=i,
                arrival_time=arrival,
                burst_time=burst,
                priority=priority
            ))
        
        return processes
    
    def generate_priority_focused(self,
                                 num_processes: int = 10,
                                 max_arrival: int = 15) -> List[Process]:
        """
        Generate processes with diverse priorities
        Useful for testing priority scheduling
        """
        processes = []
        priorities = list(range(1, num_processes + 1))
        random.shuffle(priorities)
        
        for i in range(1, num_processes + 1):
            arrival = random.randint(0, max_arrival)
            burst = random.randint(2, 12)
            priority = priorities[i - 1]
            
            processes.append(Process(
                pid=i,
                arrival_time=arrival,
                burst_time=burst,
                priority=priority
            ))
        
        return processes
    
    def generate_simultaneous_arrival(self,
                                    num_processes: int = 8,
                                    arrival_window: int = 3) -> List[Process]:
        """
        Generate processes that arrive around the same time
        Useful for testing Round Robin and preemptive algorithms
        """
        processes = []
        for i in range(1, num_processes + 1):
            arrival = random.randint(0, arrival_window)
            burst = random.randint(3, 10)
            priority = random.randint(1, 5)
            
            processes.append(Process(
                pid=i,
                arrival_time=arrival,
                burst_time=burst,
                priority=priority
            ))
        
        return processes
    
    def generate_io_intensive(self,
                            num_processes: int = 10,
                            max_arrival: int = 20) -> List[Process]:
        """
        Generate processes with short CPU bursts (simulating I/O intensive)
        """
        processes = []
        for i in range(1, num_processes + 1):
            arrival = random.randint(0, max_arrival)
            burst = random.randint(1, 5)  # Short bursts
            priority = random.randint(1, 5)
            
            processes.append(Process(
                pid=i,
                arrival_time=arrival,
                burst_time=burst,
                priority=priority
            ))
        
        return processes
    
    def generate_mixed_workload(self,
                              num_processes: int = 15,
                              max_arrival: int = 25) -> List[Process]:
        """
        Generate a realistic mixed workload
        - Some CPU-intensive (long burst)
        - Some I/O-intensive (short burst)
        - Varied priorities
        """
        processes = []
        for i in range(1, num_processes + 1):
            arrival = random.randint(0, max_arrival)
            
            # Process type distribution
            process_type = random.random()
            if process_type < 0.2:
                # CPU-intensive (20%)
                burst = random.randint(15, 25)
                priority = random.randint(3, 5)  # Lower priority
            elif process_type < 0.5:
                # I/O-intensive (30%)
                burst = random.randint(1, 5)
                priority = random.randint(1, 3)  # Higher priority
            else:
                # Normal processes (50%)
                burst = random.randint(5, 12)
                priority = random.randint(2, 4)
            
            processes.append(Process(
                pid=i,
                arrival_time=arrival,
                burst_time=burst,
                priority=priority
            ))
        
        return processes
    
    def save_to_csv(self, processes: List[Process], filename: str):
        """
        Save processes to CSV file
        
        Args:
            processes: List of processes
            filename: Output CSV filename
        """
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['PID', 'Arrival_Time', 'Burst_Time', 'Priority'])
            
            for p in processes:
                writer.writerow([p.pid, p.arrival_time, p.burst_time, p.priority])
        
        print(f"Dataset saved to {filename}")
    
    @staticmethod
    def load_from_csv(filename: str) -> List[Process]:
        """
        Load processes from CSV file
        
        Args:
            filename: Input CSV filename
        
        Returns:
            List of Process objects
        """
        processes = []
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                processes.append(Process(
                    pid=int(row['PID']),
                    arrival_time=int(row['Arrival_Time']),
                    burst_time=int(row['Burst_Time']),
                    priority=int(row['Priority'])
                ))
        
        print(f"Loaded {len(processes)} processes from {filename}")
        return processes
    
    def generate_all_datasets(self, output_dir: str = "."):
        """Generate all dataset types and save to CSV"""
        datasets = {
            'uniform': self.generate_uniform(num_processes=20),
            'burst_heavy': self.generate_burst_heavy(num_processes=15),
            'priority_focused': self.generate_priority_focused(num_processes=12),
            'simultaneous': self.generate_simultaneous_arrival(num_processes=10),
            'io_intensive': self.generate_io_intensive(num_processes=15),
            'mixed_workload': self.generate_mixed_workload(num_processes=20),
        }
        
        for name, processes in datasets.items():
            filename = f"{output_dir}/dataset_{name}.csv"
            self.save_to_csv(processes, filename)
        
        return datasets


def print_dataset_summary(processes: List[Process], dataset_name: str):
    """Print summary statistics of a dataset"""
    print(f"\n{'='*60}")
    print(f"Dataset: {dataset_name}")
    print(f"{'='*60}")
    print(f"Number of Processes: {len(processes)}")
    print(f"Arrival Time Range: {min(p.arrival_time for p in processes)} - "
          f"{max(p.arrival_time for p in processes)}")
    print(f"Burst Time Range: {min(p.burst_time for p in processes)} - "
          f"{max(p.burst_time for p in processes)}")
    print(f"Average Burst Time: {sum(p.burst_time for p in processes) / len(processes):.2f}")
    print(f"Priority Range: {min(p.priority for p in processes)} - "
          f"{max(p.priority for p in processes)}")
    
    # Show first few processes
    print(f"\nFirst 5 processes:")
    print(f"{'PID':<5} {'Arrival':<10} {'Burst':<10} {'Priority':<10}")
    print("-" * 40)
    for p in sorted(processes, key=lambda x: x.pid)[:5]:
        print(f"{p.pid:<5} {p.arrival_time:<10} {p.burst_time:<10} {p.priority:<10}")


# Example usage
if __name__ == "__main__":
    generator = DatasetGenerator(seed=42)
    
    # Generate different types of datasets
    print("Generating datasets...")
    
    datasets = {
        'Uniform Distribution': generator.generate_uniform(15),
        'Burst Heavy': generator.generate_burst_heavy(12),
        'Priority Focused': generator.generate_priority_focused(10),
        'Simultaneous Arrival': generator.generate_simultaneous_arrival(8),
        'I/O Intensive': generator.generate_io_intensive(12),
        'Mixed Workload': generator.generate_mixed_workload(20),
    }
    
    # Print summaries
    for name, processes in datasets.items():
        print_dataset_summary(processes, name)
    
    # Save all datasets
    print("\n\nSaving all datasets to CSV...")
    generator.generate_all_datasets()
    
    # Example: Load a dataset
    print("\n\nExample: Loading dataset from CSV...")
    loaded = DatasetGenerator.load_from_csv('dataset_uniform.csv')
    print(f"Successfully loaded {len(loaded)} processes")
