import pandas as pd
import json
import os

class StatisticsManager:
    __default_result_directory = 'Results'
    __optimal_soltions_path = 'Files/Optimal-Solutions.json'

    def __init__(self, aggregated_file_name):
        self.__dataframe = pd.DataFrame(columns=['problem', 'algorithm', 'time-required', 'space-required', 'solution', 'optimal-solution', 'solution-quality', 'problem-size'])
        self.__aggregated_file_path = self.__default_result_directory + '/' + aggregated_file_name + '.csv'
        
        with open(self.__optimal_soltions_path, 'r') as file:
            self.__optimal_solutions = json.load(file) 

    def Save(self):
        if not os.path.exists(self.__default_result_directory):
            os.makedirs(self.__default_result_directory)
        
        if os.path.exists(self.__aggregated_file_path):
            existing_data = pd.read_csv(self.__aggregated_file_path)
            combined_data = pd.concat([existing_data, self.__dataframe], ignore_index=True)
        else:
            combined_data = self.__dataframe
        
        combined_data.to_csv(self.__aggregated_file_path, index=False)

    def __compare_solutions__(self, problem, solution):
        optimal_value = self.__optimal_solutions.get(problem)
        quality = abs(optimal_value - solution) / max(optimal_value, solution)
        return optimal_value, quality

    def __add_dataframe_row__(self, problem, solution, algorithm, time_required, space_required, optimal_solution, solution_quality, graph_size):
        new_row = {
            'problem': problem, 
            'algorithm': algorithm, 
            'time-required': time_required,
            'space-required': space_required, 
            'solution': solution, 
            'optimal-solution': optimal_solution, 
            'solution-quality': solution_quality,
            'problem-size': graph_size
        }
        self.__dataframe.loc[len(self.__dataframe)] = new_row

    def AddTimeoutSolution(self, problem, algorithm, time_required, graph_size):
        optimal_value = self.__optimal_solutions.get(problem)
        self.__add_dataframe_row__(problem, None, algorithm, time_required, None, optimal_value, None, graph_size)

    def AddSolution(self, problem, solution, algorithm, time_required, space_required, graph_size):
        optimal, quality = self.__compare_solutions__(problem, solution)
        self.__add_dataframe_row__(problem, solution, algorithm, time_required, space_required, optimal, quality, graph_size)

        