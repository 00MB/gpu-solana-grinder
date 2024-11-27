import ray
import subprocess
import os
import json
from typing import Dict, List, Optional
import numpy as np

@ray.remote(num_gpus=1)
class GPUWorker:
    def __init__(self, gpu_id: int):
        self.gpu_id = gpu_id
        os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)
        
    def run_vanity_mining(self, num_iterations: int = 1000) -> Dict:
        """Run vanity mining on a single GPU"""
        try:
            # Update path to binary
            vanity_path = "./src/release/cuda_ed25519_vanity"
            cmd = [vanity_path, str(self.gpu_id), str(num_iterations)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            return {
                "gpu_id": self.gpu_id,
                "iterations": num_iterations,
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }
        except Exception as e:
            return {
                "gpu_id": self.gpu_id, 
                "error": str(e),
                    "success": False
                }

class RayManager:
    def __init__(self):
        # Initialize Ray if not already initialized
        if not ray.is_initialized():
            ray.init()
        
        # Get available GPUs
        self.num_gpus = ray.available_resources().get("GPU", 0)
        if self.num_gpus == 0:
            print("No GPUs found, defaulting to 1 CPU worker")
            self.num_gpus = 1
        self.workers: List[GPUWorker] = []
        
    def setup_workers(self):
        """Initialize GPU workers"""
        self.workers = [GPUWorker.remote(i) for i in range(int(self.num_gpus))]
        
    def run_distributed(self, iterations_per_gpu: int = 1000):
        """Run vanity mining distributed across all available GPUs"""
        if not self.workers:
            self.setup_workers()
            
        # Launch tasks on all workers
        tasks = [worker.run_vanity_mining.remote(iterations_per_gpu) 
                for worker in self.workers]
        
        # Wait for all tasks to complete
        results = ray.get(tasks)
        
        # Aggregate results
        total_keys_found = 0
        total_executions = 0
        
        for result in results:
            if result["success"]:
                print(f"GPU {result['gpu_id']} output:")
                print(result["output"])
                
        return {
            "total_gpus_used": len(self.workers),
            "total_keys_found": total_keys_found,
            "total_executions": total_executions,
            "results": results
        }
        
    def shutdown(self):
        """Cleanup Ray resources"""
        ray.shutdown()

if __name__ == "__main__":
    manager = RayManager()
    results = manager.run_distributed()
    print(json.dumps(results, indent=2)) 