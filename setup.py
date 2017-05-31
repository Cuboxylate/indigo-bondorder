import os
import sys
import time
import warnings

from setuptools import setup, find_packages
from setuptools.command.install import install as _install


if sys.version_info[:2] < (3,4):
    raise RuntimeError("Python version >= 3.4 required.")

version = "0.1"

class install(_install):
    def run(self):
        self.execute(pre_setup, ('src/indigox',),
                     msg="Generating config.py file...")
        _install.do_egg_install(self)

def cpu_count():
    import multiprocessing
    return multiprocessing.cpu_count()

def find_java():
    # basically same as unix which command
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    
    # Find the executable
    print('Searching for java executable...')
    for path in os.environ["PATH"].split(os.pathsep):
        path = path.strip('"')
        exe_file = os.path.join(path, 'java')
        if is_exe(exe_file):
            program = exe_file
            print('FOUND ({})'.format(exe_file))
            break
    else:
        print('NOT FOUND')
        return '', False
    
    # Test if it works
    import subprocess as sp
    from pathlib import Path
    print('Testing java...')
    my_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    test_file = my_dir/'src/indigox/external/testfile.dgf'
    with test_file.open('w') as f:
        f.write('e 1 2\ne 2 3\ne 2 4\n')
    test_args = [program, '-jar', 'libtw.jar', 'nl.uu.cs.treewidth.TDPrint',
                 'upperbound', 'testfile.dgf']
    test_process = sp.Popen(test_args, stdout=sp.PIPE, stderr=sp.PIPE,
                            cwd = str(test_file.parent))
    test_out, test_err = test_process.communicate()
    test_out = test_out.decode()
    test_err = test_err.decode()
    if test_out.startswith('graph G {'):
        works = True
        print('OK')
    else:
        works = test_err if test_err else test_out
        print('FAIL')
    
    os.remove(str(test_file))
    return program, works

def pre_setup(in_dir):
    java_path, j_works = find_java()
    post_setup.j_path = java_path
    post_setup.j_works = j_works
    config_data = {'num_processes':cpu_count(),
                   'javapath':java_path,
                   'installpath':in_dir,
                   'workpath':os.path.expanduser("~")+'/tmp',
                   'date':time.strftime('%c'),
                   'version':version,
                   'foundjava':j_works if isinstance(j_works, bool) else False,
               }

    config_template = """# config.py autogenerated by setup.py at {date}

from pathlib import Path
import os

JAVA_WORKS = {foundjava}

# Directory structure setup
SOURCE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
WORK_DIR = Path('{workpath}')

# General BO things
INFINITY = 9e9
RUN_QBND = True
BASIS_LEVEL = 'def2svpd'  
COUNTERPOISE_CORRECTED = False
ALLOW_HYPERVALENT = True
ELECTRON_PAIRS = True
HYPERPENALTY = True
PREFILL_LOCATIONS = False
SUPPORTED_ELEMENTS = {{'H','C','N','O','F','P','S','Cl','Br'}}
TIMEOUT = 2.5
NUM_PROCESSES = {num_processes}
DEFAULT_METHOD = 'fpt' if JAVA_WORKS else 'lo'

# A* things
HEURISTIC = 'tight'
INITIAL_LO_ENERGY = False

# BALL things
MAX_SOLUTIONS = 50
BALL_DATA_FILE = SOURCE_DIR/'external/OriginalBO.xml'

# FPT things
JAVA_PATH = Path('{javapath}')
LIBTW_PATH = SOURCE_DIR / 'external'
TD_TIMEOUT = 60
ALLOW_FALLBACK = False
MAX_TREEWIDTH = 5

# GA things
POP_SIZE = 50
MUTATE_PROB = 0.1
MIN_GENERATIONS = 25
MAX_GENERATIONS = 100
BRUTEFORCE_CUTOFF = POP_SIZE * MIN_GENERATIONS 
CONVERGENCE = 20
ELITEISM_SIZE = 0.25
BREEDING_ELITEISM = 0.25
SEED_COUNT = 25

# LO things
INIT_WITH_GA = False

"""

    # write config file
    with open(in_dir+'/config.py','w') as f:
        f.write(config_template.format(**config_data))

def post_setup():
    if not post_setup.j_path:
        warnings.warn('Unable to locate java executable. You will be unable '
                      'to utilise the FPT method.', UserWarning)
    elif not isinstance(post_setup.j_works, bool):
        warnings.warn('Unable to execute java. You will be unable to utilise '
                      'the FPT method. Error was:\n{}'
                      ''.format(post_setup.j_works), UserWarning)
        
        


# do the setup stuff
packages = find_packages('src')

package_data = {
    'indigox':['external/*.xml','external/*.jar'],
    }


if __name__ == "__main__":
    setup(  cmdclass = {'install':install},
            name="indigox",
            version=version,
            packages=packages,
            install_requires=['scipy>=0.18',
                              'networkx>=1.10',
                              'bitarray>=0.8',
                              'openbabel>=2.3',
                              'numpy>=1.10',],
            package_data = package_data,
            package_dir={'':'src'},
            zip_safe = False,)
    post_setup()
