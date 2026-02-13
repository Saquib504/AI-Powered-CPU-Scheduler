# AI-Powered Process Scheduling

## 🎯 Project Overview
This project implements and analyzes six major CPU scheduling algorithms, providing a foundation for integrating machine learning techniques for predictive and adaptive scheduling.

## 📚 Implemented Algorithms

### 1. **FCFS (First Come First Serve)**
- **Type**: Non-preemptive
- **Description**: Processes are executed in order of arrival
- **Pros**: Simple to implement, no starvation
- **Cons**: Poor performance with long processes (convoy effect)

### 2. **SJF (Shortest Job First)**
- **Type**: Non-preemptive
- **Description**: Execute shortest job first among available processes
- **Pros**: Minimizes average waiting time
- **Cons**: Requires burst time knowledge, potential starvation

### 3. **SRTF (Shortest Remaining Time First)**
- **Type**: Preemptive
- **Description**: Preemptive version of SJF
- **Pros**: Optimal average turnaround time
- **Cons**: More context switches, requires burst time knowledge

### 4. **Round Robin**
- **Type**: Preemptive
- **Description**: Each process gets fixed time quantum in circular order
- **Pros**: Fair, excellent response time
- **Cons**: Higher average waiting time, quantum selection critical

### 5. **Priority Scheduling (Non-preemptive)**
- **Type**: Non-preemptive
- **Description**: Processes scheduled based on priority value
- **Pros**: Important processes get preferential treatment
- **Cons**: Potential starvation of low-priority processes

### 6. **Priority Scheduling (Preemptive)**
- **Type**: Preemptive
- **Description**: Higher priority can preempt lower priority
- **Pros**: More responsive to urgent tasks
- **Cons**: Increased context switching, potential starvation

## 🚀 Getting Started

### Prerequisites
```bash
# Python 3.x
python3 --version

# Install matplotlib for visualizations
pip install matplotlib --break-system-packages
```

### Running the Scheduler
```bash
# Run all scheduling algorithms with sample data
python3 cpu_scheduler.py

# Generate Gantt charts (requires matplotlib)
python3 gantt_visualizer.py
```

## 📊 Performance Metrics

The implementation calculates the following metrics for each algorithm:

- **Turnaround Time (TAT)**: Time from process arrival to completion
  - Formula: `TAT = Completion Time - Arrival Time`

- **Waiting Time (WT)**: Time spent in ready queue
  - Formula: `WT = Turnaround Time - Burst Time`

- **Response Time (RT)**: Time from arrival to first CPU access
  - Formula: `RT = First CPU Access Time - Arrival Time`

- **Completion Time**: Absolute time when process finishes execution

## 📈 Sample Results

Based on 5 processes with varying arrival times and burst times:

| Algorithm | Avg TAT | Avg WT | Avg RT | Best For |
|-----------|---------|--------|--------|----------|
| **FCFS** | 13.4 | 8.2 | 8.2 | Simple batch systems |
| **SJF** | 11.8 | 6.6 | 6.6 | Batch with known times |
| **SRTF** | **11.6** | **6.4** | 5.8 | **Overall performance** |
| **Round Robin** | 17.8 | 12.6 | **2.8** | **Interactive systems** |
| **Priority (NP)** | 13.0 | 7.8 | 7.8 | Critical task systems |
| **Priority (P)** | 12.8 | 7.6 | 7.0 | Real-time systems |

**Key Finding**: SRTF provides best turnaround and waiting times, while Round Robin excels in response time.

## 🧬 Code Structure

```
├── cpu_scheduler.py          # Main scheduling algorithms implementation
│   ├── Process class         # Process attributes and metrics
│   ├── SchedulingMetrics     # Performance calculation
│   ├── FCFSScheduler        # First Come First Serve
│   ├── SJFScheduler         # Shortest Job First
│   ├── SRTFScheduler        # Shortest Remaining Time First
│   ├── RoundRobinScheduler  # Round Robin
│   └── PriorityScheduler    # Priority (both types)
│
├── gantt_visualizer.py       # Gantt chart generation
│   ├── GanttChart class      # Visualization logic
│   └── Timeline creators     # Algorithm-specific timelines
│
└── Project_Report.docx       # Comprehensive project documentation
```

## 💡 Usage Examples

### Custom Process Set
```python
from cpu_scheduler import Process, FCFSScheduler, SchedulingMetrics

# Create custom processes
processes = [
    Process(pid=1, arrival_time=0, burst_time=8, priority=3),
    Process(pid=2, arrival_time=1, burst_time=4, priority=1),
    Process(pid=3, arrival_time=2, burst_time=2, priority=2),
]

# Run FCFS algorithm
result, metrics = FCFSScheduler.schedule(processes)

# Display results
SchedulingMetrics.print_process_table(result, "FCFS")
print(f"Average Waiting Time: {metrics['average_waiting_time']}")
```

### Generate Gantt Charts
```python
from gantt_visualizer import GanttChart, create_fcfs_timeline

gantt = GanttChart()
timeline = create_fcfs_timeline(processes)
fig = gantt.create_gantt_chart(result, "FCFS Algorithm", timeline)
gantt.save_chart(fig, "fcfs_output.png")
```

## 🔬 Future Work: Machine Learning Integration

Based on literature review, planned ML enhancements include:

### 1. Burst Time Prediction
- **Random Forest**: Ensemble learning for robust predictions
- **K-Nearest Neighbor**: Pattern-based execution time estimation
- **LSTM Networks**: Sequential burst time modeling

### 2. Adaptive Scheduling
- **Q-Learning**: Reinforcement learning for policy optimization
- **Deep Q Networks**: Complex state-space scheduling
- **Policy Gradient Methods**: Continuous action space scheduling

### 3. Real-Time Integration
- **Edge Computing**: Distributed ML inference
- **Hardware Acceleration**: GPU/TPU for prediction
- **Lightweight Models**: Resource-efficient neural networks

## 📖 Literature References

1. **Vayadande et al. (2023)** - Comparative study of ML algorithms for CPU burst prediction
2. **Kahu (2025)** - KernelOracle: LSTM-based Linux scheduler prediction
3. **Gracias & Broklyn (2025)** - AI/ML integration in RTOS
4. **Helmy et al. (2015)** - ML-based burst time estimation for computational grids

## 🎓 Educational Value

This project is designed for:
- Operating Systems students learning scheduling concepts
- Researchers exploring ML in system software
- Developers interested in OS kernel optimization
- Anyone curious about CPU scheduling internals

## 📝 Key Insights

### When to Use Each Algorithm

**FCFS**: 
- Simple batch processing systems
- Low overhead requirement
- Predictable, long-running tasks

**SJF/SRTF**:
- When burst times are known or predictable
- Minimizing average waiting time is critical
- Batch systems with job time estimates

**Round Robin**:
- Time-sharing systems
- Interactive applications
- Fair resource distribution needed
- Response time is critical

**Priority**:
- Real-time systems with deadlines
- Critical task prioritization
- Mixed workload environments

## 🔧 Customization

### Modify Time Quantum (Round Robin)
```python
result, metrics = RoundRobinScheduler.schedule(processes, time_quantum=4)
```

### Change Priority Scale
```python
# Lower number = Higher priority (default)
Process(pid=1, arrival_time=0, burst_time=5, priority=1)  # Highest
Process(pid=2, arrival_time=1, burst_time=3, priority=5)  # Lowest
```

## 🤝 Contributing

This is a minor project for academic purposes. Suggestions for improvements:
- Additional scheduling algorithms (MLQ, MLFQ)
- Real-world process trace datasets
- ML model implementations
- Performance optimization
- Multi-core scheduling support

## 📞 Project Team

**Minor Project - AI-Powered Process Scheduling**
- Supervisor: [Supervisor Name]
- Institution: [Your Institution]
- Submission Date: February 2026

## 📄 License

This project is for educational purposes. Feel free to use and modify for learning.

## 🙏 Acknowledgments

- Research papers cited in Project_Report.docx
- Operating Systems textbooks (Silberschatz, Tanenbaum)
- Open-source Python community
- Linux kernel scheduling documentation

---

**Note**: This implementation focuses on educational clarity over production optimization. For actual OS development, refer to kernel-specific scheduling implementations.
