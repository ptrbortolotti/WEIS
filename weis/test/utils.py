import os
import importlib
from pathlib import Path
from time import time
import pickle

from openmdao.utils.assert_utils import assert_near_equal

def execute_script(fscript):
    thisdir = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.dirname(os.path.dirname(thisdir))
    examples_dir = os.path.join(root_dir, "examples")
    
    # Go to location due to relative path use for airfoil files
    print("\n\n")
    print("NOW RUNNING:", fscript)
    print()
    fullpath = os.path.join(examples_dir, fscript + ".py")
    basepath = os.path.join(examples_dir, fscript.split("/")[0])
    os.chdir(basepath)

    # Get script/module name
    froot = fscript.split("/")[-1]

    # Use dynamic import capabilities
    # https://www.blog.pythonlibrary.org/2016/05/27/python-201-an-intro-to-importlib/
    print(froot, os.path.realpath(fullpath))
    spec = importlib.util.spec_from_file_location(froot, os.path.realpath(fullpath))
    mod = importlib.util.module_from_spec(spec)
    s = time()
    spec.loader.exec_module(mod)
    print(time() - s, "seconds to run")
    
def run_all_scripts(folder_string):
    scripts = [m for m in all_scripts if m.find(folder_string) >= 0]
    for k in scripts:
        try:
            execute_script(k)
        except Exception as e:
            print("Failed to run,", k)
            raise
            
def compare_regression_values(values_to_test, truth_value_filename, directory='', train=False, tol=1e-6):
    
    # Change current working directory to the level where the main python script was called
    truth_value_filename = os.path.join(directory, truth_value_filename)
    
    if train:
        with open(truth_value_filename, "wb") as f:
            pickle.dump(values_to_test, f)
        
    else:
        with open(truth_value_filename, "rb") as f:
            truth_values = pickle.load(f)
            
        for i_case, truth_dict in enumerate(truth_values):
            output_dict = values_to_test[i_case]
            for key in output_dict:
                if key == 'meta':
                    continue
                testing_value = output_dict[key]
                truth_value = truth_dict[key]
                
                try:
                    assert_near_equal(output_dict[key], truth_dict[key], tolerance=tol)
                except Exception as e:
                    print()
                    print(f"Error: Comparison values not equal for {key}.")
                    print()
                    raise
        
        

                