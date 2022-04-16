import copy

""" if the first arrival time > 0, start from this time """


def time_normalizer(processes):
    least = sorted(processes, key=lambda i: i["arrival_time_val"])[
        0]["arrival_time_val"]
    for i in range(len(processes)):
        processes[i]["arrival_time_val"] -= least


""" Calculates the waiting time for each process, returns the average """


def waiting_calc(gnatt, processes):
    waitings = [0 for i in range(len(processes))]
    flags = [0 for i in range(len(processes))]

    for i in range(len(processes)):
        for onegnatt in gnatt:
            if onegnatt["processs_no"] - 1 == i:
                if(flags[i] == 0):
                    waitings[processes[i]["processs_no"] -
                             1] += onegnatt["start"] - processes[i]["arrival_time_val"]
                    flags[i] = onegnatt["end"]
                else:
                    waitings[processes[i]["processs_no"] -
                             1] += onegnatt["start"] - flags[i]
                    flags[i] = onegnatt["end"]

    avg_wait = sum(waitings) / len(waitings)

    return avg_wait


def FCFS(processes):
    gnatt = []
    results = sorted(processes, key=lambda i: i["arrival_time_val"])
    time = 0
    for result in results:
        gnatt.append({"processs_no": result["processs_no"],
                     "start": time, "end": time + result["burst_time_val"]})
        time += result["burst_time_val"]

    avg_wait = waiting_calc(gnatt, processes)
    return (gnatt, avg_wait)


def SJFNP(processes):

    gnatt = []
    results = []
    for process in processes:
        results.append({"processs_no": process["processs_no"],
                        "burst_time_val": process["burst_time_val"],
                        "arrival_time_val": process["arrival_time_val"],
                        })
    results = sorted(results, key=lambda i: i["burst_time_val"])

    loop = 0
    i = 0
    time = 0
    while(True):
        loop += 1
        if (results[i]["arrival_time_val"] <= time and results[i]["burst_time_val"] != 0):
            gnatt.append({"processs_no": results[i]["processs_no"],
                         "start": time, "end": time + results[i]["burst_time_val"]})

            time += results[i]["burst_time_val"]
            results[i]["burst_time_val"] = 0

            loop = 0
            i = 0
            continue
        i = (i + 1) % len(processes)
        if(loop == len(processes)):
            break

    avg_wait = waiting_calc(gnatt, processes)
    return (gnatt, avg_wait)


def SJFP(processes):

    gnatt = []
    results = []
    for process in processes:
        results.append({"processs_no": process["processs_no"],
                        "burst_time_val": process["burst_time_val"],
                        "arrival_time_val": process["arrival_time_val"],
                        })
    results = sorted(results, key=lambda i: i["burst_time_val"])

    loop = 0
    i = 0
    time = 0

    while(True):
        results = sorted(results, key=lambda i: i["burst_time_val"])
        loop += 1
        if (results[i]["arrival_time_val"] <= time and results[i]["burst_time_val"] != 0):
            if(len(gnatt) > 0):
                if(gnatt[-1]["processs_no"] == results[i]["processs_no"]):
                    gnatt[-1]["end"] = time + 1
                else:
                    gnatt.append(
                        {"processs_no": results[i]["processs_no"], "start": time, "end": time + 1})
            else:
                gnatt.append(
                    {"processs_no": results[i]["processs_no"], "start": time, "end": time + 1})

            time += 1
            results[i]["burst_time_val"] -= 1

            loop = 0
            i = 0
            continue

        i = (i + 1) % len(processes)
        if(loop == len(processes)):
            break

    avg_wait = waiting_calc(gnatt, processes)
    return (gnatt, avg_wait)


def priorityNP(processes):

    gnatt = []
    results = []
    for process in processes:
        results.append({"processs_no": process["processs_no"],
                        "burst_time_val": process["burst_time_val"],
                        "arrival_time_val": process["arrival_time_val"],
                        "priority_val": process["priority_val"]
                        })
    results = sorted(results, key=lambda i: i["priority_val"])

    loop = 0
    i = 0
    time = 0
    while(True):
        loop += 1
        if (results[i]["arrival_time_val"] <= time and results[i]["burst_time_val"] != 0):
            gnatt.append({"processs_no": results[i]["processs_no"],
                         "start": time, "end": time + results[i]["burst_time_val"]})

            time += results[i]["burst_time_val"]
            results[i]["burst_time_val"] = 0

            loop = 0
            i = 0
            continue
        i = (i + 1) % len(processes)
        if(loop == len(processes)):
            break

    avg_wait = waiting_calc(gnatt, processes)
    return (gnatt, avg_wait)


def priorityP(processes):

    gnatt = []
    gnatt = []
    results = []
    for process in processes:
        results.append({"processs_no": process["processs_no"],
                        "burst_time_val": process["burst_time_val"],
                        "arrival_time_val": process["arrival_time_val"],
                        "priority_val": process["priority_val"]
                        })
    results = sorted(results, key=lambda i: i["priority_val"])

    loop = 0
    i = 0
    time = 0

    while(True):
        results = sorted(results, key=lambda i: i["priority_val"])
        loop += 1
        if (results[i]["arrival_time_val"] <= time and results[i]["burst_time_val"] != 0):
            if(len(gnatt) > 0):
                if(gnatt[-1]["processs_no"] == results[i]["processs_no"]):
                    gnatt[-1]["end"] = time + 1
                else:
                    gnatt.append(
                        {"processs_no": results[i]["processs_no"], "start": time, "end": time + 1})
            else:
                gnatt.append(
                    {"processs_no": results[i]["processs_no"], "start": time, "end": time + 1})

            time += 1
            results[i]["burst_time_val"] -= 1

            loop = 0
            i = 0
            continue

        i = (i + 1) % len(processes)
        if(loop == len(processes)):
            break

    avg_wait = waiting_calc(gnatt, processes)
    return (gnatt, avg_wait)


def RoundRobin(processes, time_slice):

    gnatt = []
    results = []
    for process in processes:
        results.append({"processs_no": process["processs_no"],
                        "burst_time_val": process["burst_time_val"],
                        "arrival_time_val": process["arrival_time_val"],
                        })
    results = sorted(results, key=lambda i: i["arrival_time_val"])

    loop = 0
    i = 0
    time = 0

    while(True):
        loop += 1
        if (results[i]["arrival_time_val"] <= time and results[i]["burst_time_val"] != 0):
            if(results[i]["burst_time_val"] < time_slice):
                gnatt.append(
                    {"processs_no": results[i]["processs_no"], "start": time, "end": time + results[i]["burst_time_val"]})
                time += results[i]["burst_time_val"]
                results[i]["burst_time_val"] = 0
            else:
                gnatt.append(
                    {"processs_no": results[i]["processs_no"], "start": time, "end": time + time_slice})
                time += time_slice
                results[i]["burst_time_val"] -= time_slice
            loop = 0

        i = (i + 1) % len(processes)
        if(loop == len(processes)):
            break

    avg_wait = waiting_calc(gnatt, processes)
    return (gnatt, avg_wait)
