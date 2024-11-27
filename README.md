# GPU Solana Grinder with Ray Integration

This project is a GPU-based Solana address grinder that uses Ray for distributed computing across multiple GPUs.

## Requirements

- CUDA-capable GPU(s)
- CUDA Toolkit
- Python 3.8+
- Ray framework

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Build the CUDA code:
```bash
make
```

## Usage

1. Start Ray cluster (if running distributed):
```bash
ray start --head
```

2. Run the distributed mining:
```bash
python src/ray_manager.py
```

## Configuration

- The number of GPUs used is automatically detected by Ray
- Each GPU runs in its own worker process
- Results are aggregated across all GPUs

## Architecture

- `ray_manager.py`: Manages distributed GPU workers using Ray
- `vanity.cu`: CUDA implementation of the mining algorithm
- Each GPU worker runs independently and reports results back to the manager

## Performance

The Ray integration allows for:
- Linear scaling with number of GPUs
- Automatic load balancing
- Fault tolerance (failed GPU tasks are automatically retried)
- Real-time monitoring of mining progress

## Monitoring

Monitor your Ray cluster:
```bash
ray dashboard
```
Default dashboard URL: http://localhost:8265
