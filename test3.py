import threading
import multiprocessing

def io_bound_function():
    print("I/O-bound task")

def cpu_bound_function():
    print("CPU-bound task")

def thread_task():
    # Run an I/O-bound task in a thread
    io_bound_function()

def process_task():
    # Run a CPU-bound task in a separate process
    cpu_bound_function()

if __name__ == "__main__":
    # Create and start a thread
    thread = threading.Thread(target=thread_task)
    thread.start()

    # Create and start a process
    process = multiprocessing.Process(target=process_task)
    process.start()

    # Wait for the thread and process to finish
    thread.join()
    process.join()

    print("Main thread continues")
