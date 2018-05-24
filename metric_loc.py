import sys
import os
import getopt
import numpy as np
import csv

verboseprint = None
def main(argv):
    matrix = ''
    dest_path = None
    verbose = False

    # Argument parsing
    try:
        opts, args = getopt.getopt(argv, "hm:vw:",["help", "matrix=", "verbose"])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-m", "--matrix"):
            matrix = arg
        elif opt == "-w":
            dest_path = arg
        elif opt in ("-v", "--verbose"):
            verbose = True

    # Verify input
    global verboseprint
    verboseprint = print if verbose else lambda *a, **k: None
    verboseprint("[STATUS] Verifying your input ...")
    verify_input(matrix, dest_path)
    verboseprint("[STATUS] Input verified.")

    # Get matrix and spectra data
    verboseprint("[STATUS] Loading matrix file ...")
    verboseprint("[STATUS] Matrix file successfully loaded. Analyzing ...")
    data, results = analyze_matrix(matrix)
    print(data.shape)
    print(num_failing_tests(results))
    print(num_passing_tests(results))
    print(num_tests(results))
    print(num_elements(data))
    print(num_visited_elements(data))
    print(num_not_visited_elements(data))
    print(num_visitations(data))
    print(sparsity(data))
    print(percentage_passing_tests(results))
    print(percentage_failing_tests(results))
    print(coverage_passing_tests(data, results))
    print(coverage_failing_tests(data, results))
    print(avg_num_visited_elements(data))
    print(avg_num_pass_visited_elements(data, results))
    print(avg_num_fail_visited_elements(data, results))

    verboseprint("[STATUS] Output generated!")
    # if dest_path:
    #     verboseprint("[STATUS] Writing output to file " + dest_path)
    #     write_output(dest_path, output)
    #     verboseprint("[STATUS] Output written!")
    # else:
        ### verboseprint("[INFO] Printing results ...")
        ### print(output)
    verboseprint("[STATUS] Success! Exiting ...")


def analyze_matrix(matrix):
    with open(matrix) as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        try:
            data = np.array([])
            results = np.array([])
            for row in reader:
                if data.size is 0:
                    data = row[:-1]
                    results = row[-1]
                data = np.vstack((data, row[:-1]))
                results = np.vstack((results, row[-1]))
            return (data.astype(np.int),results)
        except csv.Error as ex:
            verboseprint("[ERROR] Exception during matrix file parsing.")
            print("Failed. Aborting ...")
            sys.exit()

def verify_input(matrix, dest_path):
    if(matrix == ''):
        usage()
        sys.exit()
    if not os.path.isfile(matrix):
        verboseprint("[ERROR] Path of matrix is invalid.")
        print("Failed. Aborting ...")
        sys.exit()
    if dest_path and not os.path.exists(dest_path):
        verboseprint("[ERROR] Destination path invalid.")
        print("Failed. Aborting ...")
        sys.exit()

def write_output(fname, output):
    with open(fname, 'w') as text_file:
        try:
            for line in output:
                text_file.write(line + '\n')
        except Exception:
            verboseprint("[ERROR] Exception during writing output to {:s}".format(fname))
            print("Failed. Aborting ...")
            sys.exit()

def call_design_metric(technique):
    if technique == "dstar2":
        scores = dstar2()
    elif technique == "dstar3":
        scores = dstar3()
    elif technique == "jaccard":
        scores = jaccard()
    elif technique == "ochiai":
        scores = ochiai()
    elif technique == "tarantula":
        scores = tarantula()
    elif technique == "zoltar":
        scores = zoltar()
    else:
        print("[ERROR] Technique not implemented yet.")
        print("Failed. Aborting ...")
        sys.exit()
    return scores

def num_failing_tests(results):
    return (results == '-').sum()

def num_passing_tests(results):
    return (results == '+').sum()

def num_tests(results):
    return len(results)

def percentage_failing_tests(results):
    return (results == '-').sum()/len(results)

def percentage_passing_tests(results):
    return (results == '+').sum()/len(results)

def num_elements(data):
    return data.shape[1]

def num_visited_elements(data):
    return (np.sum(data, axis=0) != 0).sum()

def num_not_visited_elements(data):
    return (np.sum(data, axis=0) == 0).sum()

def num_visitations(data):
    return np.sum(data)

def sparsity(data):
    return np.sum(data)/(np.prod(data.shape))

def coverage(data):
    return num_visited_elements(data) / num_elements(data)

def coverage_passing_tests(data, results):
    passing_tests = get_passing_data(data, results)
    return num_visited_elements(passing_tests) / num_elements(data)

def coverage_failing_tests(data, results):
    failing_tests = get_failing_data(data, results)
    return num_visited_elements(failing_tests) / num_elements(data)

def avg_num_visited_elements(data):
    visits = np.sum(data, axis=1)
    return np.sum(visits)/ len(data)

def avg_num_pass_visited_elements(data, results):
    passing_tests = get_passing_data(data, results)
    visits = np.sum(passing_tests, axis=1)
    return np.sum(visits)/ len(passing_tests)

def avg_num_fail_visited_elements(data, results):
    failing_tests = get_failing_data(data, results)
    visits = np.sum(failing_tests, axis=1)
    return np.sum(visits)/ len(failing_tests)

def num_same_visited_methods(data, results):
    passing_data = get_passing_data(data, results)
    failing_data = get_failing_data(data, results)

def get_passing_data(data, results):
    mask = np.transpose(results == '+')[0]
    return data[mask]

def get_failing_data(data, results):
    mask = np.transpose(results == '-')[0]
    return data[mask]

def usage():
    print("\nPython command tool to evaluate Gzoltar outputs.\n")
    print("faultloc.py -m <matrix file>")
    print("Parameters:")
    print("-m : specify matrix file (--matrix=)")
    print("-w : specify output file")
    print("-v : verbose output (--verbose)")
    print("-h : print this help")


if __name__ == "__main__":
    main(sys.argv[1:])
