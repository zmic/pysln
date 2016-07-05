import datetime
from sln import project_configuration_combiner, solution

project_configs = project_configuration_combiner( ['30','31','32','33','34','35'] )
S = solution('IEEE4882',  project_configs)          
S.project('IEEE4882-NI', 'ieee4882_ni')
S.project('IEEE4882-KS', 'ieee4882_ks')
S.project('IEEE4882-AL', 'ieee4882_al')
folder = r"c:\temp\ieee4882" 
folder = folder + datetime.datetime.now().strftime('/%Y-%m-%d_%H-%M-%S')
S.do_it(folder)
    