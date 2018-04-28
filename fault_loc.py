import sys
import os
import getopt
import csv
import numpy as np

techniques = ["dstar2", "dstar3", "jaccard", "ochiai", "tarantula"]

total_passed = 0 # total passed test cases
total_failed = 0 # total failed test cases
passed_statements = [] # executions by passing test cases
failed_statements = [] # executions by failing test cases
scores = [] # Calculated scores

def main(argv):
    matrix = ''
    spectra = ''
    technique = ''
    number = None
    max_rank = None

    # Argument parsing
    try:
        opts, args = getopt.getopt(argv, "hm:s:t:n:r:",["help", "matrix=", "spectra=", "technique="])
    except getopt.GetoptError:
        usage()
        sys.exit()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-m", "--matrix"):
            matrix = arg
        elif opt in ("-s", "--spectra"):
            spectra = arg
        elif opt in ("-t", "--technique"):
            technique = arg
        elif opt == "-n":
            number = arg
        elif opt == "-r":
            max_rank = arg

        # Verify input
        check_correct_arguments(matrix, spectra, technique, number, max_rank)

        # Get matrix data
        analyze_matrix()

        scores = np.zeros(len(passed_statements))
        # Call design metric
        call_design_metric(technique)

        # Rank items
        ranks = rank(scores)
        sorted_rank_indices = np.argsort(ranks)
        spectra_lines = load_spectra(spectra)
        for i, line in enumerate(spectra_lines):
            spectra_lines[i] = "Rank: " + str(ranks[i]) + " | " + line
        np_spectra_lines = np.array(spectra_lines)
        sorted_lines = np_spectra_lines[sorted_rank_indices]
        if number:
            print(sorted_lines[:number])

        # print("Total passed: {:d}".format(total_passed))
        # print("Total failed: {:d}".format(total_failed))
        # print(passed_statements)
        # print(failed_statements)

def analyze_matrix():
    global passed_statements, failed_statements, total_failed, total_passed, scores
    with open(matrix) as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        try:
            for row in reader:
                if passed_statements == []:
                    passed_statements = np.zeros(len(row)-1)
                    failed_statements = np.zeros(len(row)-1)
                if row[-1] == '+':
                    total_passed += 1
                    visited_statements = np.array(row[:-1]).astype(int)
                    passed_statements = np.add(passed_statements, visited_statements)
                elif row[-1] == '-':
                    total_failed += 1
                    visited_statements = np.array(row[:-1]).astype(int)
                    failed_statements = np.add(failed_statements, visited_statements)
        except csv.Error as ex:
            print("Error during matrix file parsing.")
            sys.exit()

def verify_input(matrix, spectra, technque, number, max_rank)
    if(matrix == '' or spectra == '' or technique == ''):
        usage()
        sys.exit()
    if not os.path.exists(matrix):
        print("Path of matrix is invalid.")
        sys.exit()
    if not os.path.exists(spectra):
        print("Path of spectra is invalid.")
        sys.exit()
    if not technique in techniques:
        print("{:s} is not a valid technique. " \
                "Possible arguments:".format(technique))
        print(techniques)
        sys.exit()
    if number and max_rank:
        print("Do not specify rank and number of outputs together.")
        sys.exit()
    if number:
        try: number = int(number)
        except ValueError:
            print("Invalid number given.")
            sys.exit()
        if number <= 0:
            print("Number has to be positive.")
            sys.exit()
    if max_rank:
        try: max_rank = int(max_rank)
        except ValueError:
            print("Invalid rank given.")
            sys.exit()
        if max_rank <= 0:
            print("Rank has to be positive.")


def load_spectra(fname):
    f = open(fname,'r')
    data = []
    for line in f.readlines():
        data.append(line.replace('\n',''))
    f.close()
    return data

def call_design_metric(technique):
    if technique == "dstar2":
        dstar2()
    elif technique == "dstar3":
        dstar3()
    elif technique == "jaccard":
        jaccard()
    elif technique == "ochiai":
        ochiai()
    elif technique == "tarantula":
        tarantula()

def dstar2():
    global scores
    for i, _ in enumerate(scores):
        scores[i] = failed_statements[i]**2 / (total_failed - failed_statements[i] + passed_statements[i])

def dstar3():
    global scores
    for i, _ in enumerate(scores):
        scores[i] = failed_statements[i]**3 / (total_failed - failed_statements[i] + passed_statements[i])

def jaccard():
    global scores
    for i, _ in enumerate(scores):
        scores[i] = failed_statements[i] / (failed_statements[i] + (total_failed - failed_statements[i]) + passed_statements[i])

def ochiai():
    global scores
    for i, _ in enumerate(scores):
        scores[i] = failed_statements[i] / np.sqrt(total_failed * (failed_statements[i] + passed_statements[i]))

def tarantula():
    global scores
    for i, _ in enumerate(scores):
        scores[i] = (failed_statements[i]/total_failed) / (failed_statements[i]/total_failed) + (passed_statements[i]/total_passed)

def usage():
    print("Python commandtool to evaulate Gzoltar outputs.\n")
    print("faultloc.py -m <matrix file> -s <spectra file> -t <technique>")
    print("Techniques: " + ", ".join(x for x in techniques) + "\n")
    print("Parameters:")
    print("-m : specify matrix file (matrix=)")
    print("-s : specify spectra file (spectra=)")
    print("-t : specify technique for evaluation (technique=)")
    print("-w : specify output file")
    print("-n : specify number of objects to output")
    print("-r : specify number of ranks to output")
    print("-v : verbose output")
    print("-h : print this help")

def rank(v):
    if v is None or len(v) == 0:
        return []
    desc_indices = np.flipud(np.argsort(v))
    result = np.empty(len(v),int)
    result[desc_indices[0]] = 1
    for i in range(1, len(result)):
        if v[desc_indices[i]] == v[desc_indices[i-1]]:
            result[desc_indices[i]] = result[desc_indices[i-1]]
        else:
            result[desc_indices[i]] = result[desc_indices[i-1]] + 1
    return result

if __name__ == "__main__":
    main(sys.argv[1:])
