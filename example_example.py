import datetime
from sln import project_configuration_combiner, solution

project_configs = project_configuration_combiner( ['30','31','32','33','34','35'] )
S = solution('example',  project_configs)          
S.project('example', 'example')
S.project('second_project', 'second_extension')
folder = r"c:\temp\example" 
folder = folder + datetime.datetime.now().strftime('/%Y-%m-%d_%H-%M-%S')
S.do_it(folder)
    
    