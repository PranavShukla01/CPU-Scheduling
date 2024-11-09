from src.utils.test import processes
import src.utils.table as table
import src.utils.graph as graph


def run(processes):
    """
        SJF (Shortest Job First) (Non-Preemptive)

    """

    print('running shortest-job-first...')
    gantt = []

    # Initialisation
    total_turnaround_time = 0
    total_completion_time = 0
    total_waiting_time = 0
    total_response_time = 0

    # Sort by arrival time
    proc = sorted(processes, key=lambda proc: proc.arrival_time)

    for i in range(len(proc)):
        index = -1  # Assuming index 'i' to be the next one to be executed
        li = []
        for j in range(i, len(proc)):
            if proc[j].arrival_time <= total_completion_time:
                li.append((j, proc[j].burst_time))

        li = sorted(li, key=lambda k: k[1])  # Sorted on the basis of burst time
        if len(li) == 0:
            index = i
            for j in range(i + 1, len(proc)):
                if proc[j].arrival_time < proc[index].arrival_time:
                    index = j
                elif proc[j].arrival_time == proc[index].arrival_time and proc[j].burst_time < proc[index].burst_time:
                    index = j
        else:
            index = li[0][0]
            # print(li)

        if proc[index].arrival_time > total_completion_time:
            total_completion_time = proc[index].arrival_time

        proc[index].completion_time = total_completion_time + proc[index].burst_time
        proc[index].turnaround_time = proc[index].completion_time - proc[index].arrival_time
        proc[index].waiting_time = proc[index].turnaround_time - proc[index].burst_time
        proc[index].response_time = total_completion_time

        gantt.append((proc[index].p_id, (total_completion_time, proc[index].burst_time)))

        # Update Total
        total_completion_time = proc[index].completion_time
        total_turnaround_time += proc[index].turnaround_time
        total_waiting_time += proc[index].waiting_time
        total_response_time += proc[index].response_time

        proc[i], proc[index] = proc[index], proc[i]  # swapping

    return {
        'name': 'SJF',
        'avg_waiting_time': total_waiting_time / len(proc),
        'avg_response_time': total_response_time / len(proc),
        'avg_turnaround_time': total_turnaround_time / len(proc),
        'processes': proc,
        'gantt': gantt
    }




# If this file is executed directly -> run temporary test-cases
def main():
    result = run(processes)
    print("Avg Waiting Time: {}".format(result['avg_waiting_time']))
    print("Avg Turnaround Time: {}".format(result['avg_turnaround_time']))
    print("Avg Response Time: {}".format(result['avg_response_time']))
    table.plot(result['processes'])
    graph.plot_gantt(result)


if __name__ == '__main__':
    main()
