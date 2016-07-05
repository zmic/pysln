import uuid, os, shutil, datetime, itertools

class project(object):    
    def __init__(self, name, module_name):
        self.name = name
        self.module_name = module_name
        self.uuid = uuid.uuid1()
                  
    vcxproj_template = """<?xml version="1.0" encoding="utf-8"?>
<Project DefaultTargets="Build" ToolsVersion="14.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ItemGroup Label="ProjectConfigurations">{0}
  </ItemGroup>
  <PropertyGroup Label="Globals">
    <ProjectGuid>{1}</ProjectGuid>
    <Keyword>Win32Proj</Keyword>
    <RootNamespace>{2}</RootNamespace>
    <WindowsTargetPlatformVersion>8.1</WindowsTargetPlatformVersion>
  </PropertyGroup>
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.Default.props" />{3}
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.props" />
  <ImportGroup Label="ExtensionSettings">
  </ImportGroup>
  <ImportGroup Label="Shared">
  </ImportGroup>{4}
  <PropertyGroup Label="UserMacros" />{5}{6}{7}
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.targets" />
  <ImportGroup Label="ExtensionTargets">
  </ImportGroup>
</Project>
"""

    def create_project(self, project_configs, platform_toolset):
    
        project_name = self.name
        module_name = self.module_name
        guid = "{" + str(self.uuid).upper() + "}"    
        
        project_configurations = "\r\n"    
        t = '''    <ProjectConfiguration Include="{0}-{1}|{2}">
          <Configuration>{0}-{1}</Configuration>
          <Platform>{2}</Platform>
        </ProjectConfiguration>
    '''   
        for p in project_configs.iterate():
            project_configurations += t.format("Debug",p,"Win32")
            project_configurations += t.format("Debug",p,"x64")
        for p in project_configs.iterate():
            project_configurations += t.format("Release",p,"Win32")
            project_configurations += t.format("Release",p,"x64")
           
        project_configurations2 = "\r\n"           
        t1 = '''  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug-{0}|{1}'" Label="Configuration">
        <ConfigurationType>DynamicLibrary</ConfigurationType>
        <UseDebugLibraries>true</UseDebugLibraries>
        <PlatformToolset>{2}</PlatformToolset>
        <CharacterSet>Unicode</CharacterSet>
      </PropertyGroup>
    '''  
        t2 = '''  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release-{0}|{1}'" Label="Configuration">
        <ConfigurationType>DynamicLibrary</ConfigurationType>
        <UseDebugLibraries>false</UseDebugLibraries>
        <PlatformToolset>{2}</PlatformToolset>
        <WholeProgramOptimization>true</WholeProgramOptimization>
        <CharacterSet>Unicode</CharacterSet>
      </PropertyGroup>
    '''  
        for p in project_configs.iterate():
            project_configurations2 += t1.format(p,"Win32",platform_toolset)
        for p in project_configs.iterate():
            project_configurations2 += t2.format(p,"Win32",platform_toolset)
        for p in project_configs.iterate():
            project_configurations2 += t1.format(p,"x64",platform_toolset)
        for p in project_configs.iterate():
            project_configurations2 += t2.format(p,"x64",platform_toolset)
      
      
        property_sheets = "\r\n"
        t = '''  <ImportGroup Condition="'$(Configuration)|$(Platform)'=='{2}-{0}|{1}'" Label="PropertySheets">
        <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
        <Import Project="python.props" />
        <Import Project="{3}.props" />
      </ImportGroup>
    '''  
        for p in project_configs.iterate():
            property_sheets += t.format(p,"Win32", "Debug", project_name)
        for p in project_configs.iterate():
            property_sheets += t.format(p,"Win32", "Release", project_name)
        for p in project_configs.iterate():
            property_sheets += t.format(p,"x64", "Debug", project_name)
        for p in project_configs.iterate():
            property_sheets += t.format(p,"x64", "Release", project_name)
            
                    
        link_incremental = "\r\n"
        t1 = '''  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug-{0}|{1}'">
        <LinkIncremental>true</LinkIncremental>
      </PropertyGroup>        
    '''
        t2 = '''  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release-{0}|{1}'">
        <LinkIncremental>false</LinkIncremental>
      </PropertyGroup>
    '''
        for p in project_configs.iterate():
            link_incremental += t1.format(p,"Win32")
        for p in project_configs.iterate():
            link_incremental += t1.format(p,"x64")
        for p in project_configs.iterate():
            link_incremental += t2.format(p,"Win32")
        for p in project_configs.iterate():
            link_incremental += t2.format(p,"x64")

            
        t1 = '''  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Debug-{0}|Win32'">
        <ClCompile>
          <PrecompiledHeader>
          </PrecompiledHeader>
          <WarningLevel>Level3</WarningLevel>
          <Optimization>Disabled</Optimization>
          <PreprocessorDefinitions>WIN32;_DEBUG;_WINDOWS;_USRDLL;%(PreprocessorDefinitions)</PreprocessorDefinitions>
          <SDLCheck>true</SDLCheck>
          <PrecompiledHeaderFile>include.h</PrecompiledHeaderFile>      
        </ClCompile>
        <Link>
          <SubSystem>Windows</SubSystem>
          <GenerateDebugInformation>true</GenerateDebugInformation>
        </Link>
      </ItemDefinitionGroup>
    '''

        t2 = '''  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Debug-{0}|x64'">
        <ClCompile>
          <PrecompiledHeader>
          </PrecompiledHeader>
          <WarningLevel>Level3</WarningLevel>
          <Optimization>Disabled</Optimization>
          <PreprocessorDefinitions>_DEBUG;_WINDOWS;_USRDLL;%(PreprocessorDefinitions)</PreprocessorDefinitions>
          <SDLCheck>true</SDLCheck>
          <PrecompiledHeaderFile>include.h</PrecompiledHeaderFile>      
        </ClCompile>
        <Link>
          <SubSystem>Windows</SubSystem>
          <GenerateDebugInformation>true</GenerateDebugInformation>
        </Link>
      </ItemDefinitionGroup>
    '''

        t3 = '''  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release-{0}|Win32'">
        <ClCompile>
          <WarningLevel>Level3</WarningLevel>
          <PrecompiledHeader>
          </PrecompiledHeader>
          <Optimization>MaxSpeed</Optimization>
          <FunctionLevelLinking>true</FunctionLevelLinking>
          <IntrinsicFunctions>true</IntrinsicFunctions>
          <PreprocessorDefinitions>WIN32;NDEBUG;_WINDOWS;_USRDLL;%(PreprocessorDefinitions)</PreprocessorDefinitions>
          <SDLCheck>true</SDLCheck>
          <PrecompiledHeaderFile>include.h</PrecompiledHeaderFile>      
        </ClCompile>
        <Link>
          <SubSystem>Windows</SubSystem>
          <EnableCOMDATFolding>true</EnableCOMDATFolding>
          <OptimizeReferences>true</OptimizeReferences>
          <GenerateDebugInformation>true</GenerateDebugInformation>
        </Link>
      </ItemDefinitionGroup>
    '''

        t4 = ''' <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release-{0}|x64'">
        <ClCompile>
          <WarningLevel>Level3</WarningLevel>
          <PrecompiledHeader>
          </PrecompiledHeader>
          <Optimization>MaxSpeed</Optimization>
          <FunctionLevelLinking>true</FunctionLevelLinking>
          <IntrinsicFunctions>true</IntrinsicFunctions>
          <PreprocessorDefinitions>NDEBUG;_WINDOWS;_USRDLL;%(PreprocessorDefinitions)</PreprocessorDefinitions>
          <SDLCheck>true</SDLCheck>
          <PrecompiledHeaderFile>include.h</PrecompiledHeaderFile>      
        </ClCompile>
        <Link>
          <SubSystem>Windows</SubSystem>
          <EnableCOMDATFolding>true</EnableCOMDATFolding>
          <OptimizeReferences>true</OptimizeReferences>
          <GenerateDebugInformation>true</GenerateDebugInformation>
        </Link>
      </ItemDefinitionGroup>
    '''  

        compile_options = "\r\n"
        for p in project_configs.iterate():
            compile_options += t1.format(p)
        for p in project_configs.iterate():
            compile_options += t2.format(p)
        for p in project_configs.iterate():
            compile_options += t3.format(p)
        for p in project_configs.iterate():
            compile_options += t4.format(p)
      
        source_files = self.create_source_files(project_configs)
        
        return self.vcxproj_template.format(project_configurations, guid, project_name, project_configurations2, property_sheets, link_incremental, compile_options, source_files)
        
    def create_source_files(self, project_configs):    
        precompiled = "\r\n"
        t1 = '''    <PrecompiledHeader Condition="'$(Configuration)|$(Platform)'=='{0}-{1}|{2}'">Create</PrecompiledHeader>\r\n'''
        for p in project_configs.iterate():
            precompiled += t1.format('Debug', p, 'Win32')    
            precompiled += t1.format('Release', p, 'Win32')    
        for p in project_configs.iterate():
            precompiled += t1.format('Debug', p, 'x64')    
            precompiled += t1.format('Release', p, 'x64')    
        
        t = '''  <ItemGroup>
        <ClCompile Include="..\src\include.cpp">{0}
        </ClCompile>
        <ClCompile Include="..\src\main.cpp" />
      </ItemGroup>
      <ItemGroup>
        <ClInclude Include="..\src\include.h" />
      </ItemGroup>  
      '''
        return t.format(precompiled)
      
    def create_filters(self, sln_uuid):
        u1 = "{" + str(sln_uuid).upper() + "}"
        u2 = "{" + str(self.uuid).upper() + "}"
        
        t = '''<?xml version="1.0" encoding="utf-8"?>
        <Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
          <ItemGroup>
            <Filter Include="Source Files">
              <UniqueIdentifier>{0}</UniqueIdentifier>
              <Extensions>cpp;c;cc;cxx;def;odl;idl;hpj;bat;asm;asmx</Extensions>
            </Filter>
            <Filter Include="Header Files">
              <UniqueIdentifier>{1}</UniqueIdentifier>
              <Extensions>h;hh;hpp;hxx;hm;inl;inc;xsd</Extensions>
            </Filter>
          </ItemGroup>
        </Project>
    '''    
        return t.format(u1, u2)

        

class solution(object):

    sln_template_2010 = """
Microsoft Visual Studio Solution File, Format Version 11.00
# Visual Studio 2010
{0}
Global
	GlobalSection(SolutionConfigurationPlatforms) = preSolution{1}
	EndGlobalSection
	GlobalSection(ProjectConfigurationPlatforms) = postSolution{2}
	EndGlobalSection
	GlobalSection(SolutionProperties) = preSolution
		HideSolutionNode = FALSE
	EndGlobalSection
EndGlobal
"""

    sln_template_2015 = """
Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio 14
VisualStudioVersion = 14.0.24720.0
MinimumVisualStudioVersion = 10.0.40219.1
{0}
Global
    GlobalSection(SolutionConfigurationPlatforms) = preSolution{1}
    EndGlobalSection
    GlobalSection(ProjectConfigurationPlatforms) = postSolution{2}
    EndGlobalSection
    GlobalSection(SolutionProperties) = preSolution
        HideSolutionNode = FALSE
    EndGlobalSection
EndGlobal
"""

    project_include = """Project("{0}") = "{1}", "{1}.vcxproj", "{2}"
EndProject
"""
    
    def __init__(self, name, configs):
        self.name = name
        self.configs = configs
        self.uuid = uuid.uuid1()
        self.projects = []
    def project(self, project_name, module_name):
        self.projects.append( project(project_name, module_name) )
        
    def create_sln(self, vs_version):
    
        if vs_version == 'vs2015':
            sln_template = self.sln_template_2015
        if vs_version == 'vs2010':
            sln_template = self.sln_template_2010
            
        u1 = "{" + str(self.uuid).upper() + "}"
        project_includes = ''
        for p in self.projects:
            u2 = "{" + str(p.uuid).upper() + "}"
            project_includes += self.project_include.format(u1, p.name, u2)
            
        presolution = '\r\n'
        for p in self.configs.iterate():
            presolution += "\t\tDebug-{0}|x64 = Debug-{0}|x64\r\n".format(p)
            presolution += "\t\tDebug-{0}|x86 = Debug-{0}|x86\r\n".format(p)
        for p in self.configs.iterate():
            presolution += "\t\tRelease-{0}|x64 = Release-{0}|x64\r\n".format(p)
            presolution += "\t\tRelease-{0}|x86 = Release-{0}|x86\r\n".format(p)
                                
        postsolution = '\r\n'
        for p in self.projects:
            u2 = "{" + str(p.uuid).upper() + "}"        
            for p in self.configs.iterate():
                postsolution += "\t\t{0}.Debug-{1}|x64.ActiveCfg = Debug-{1}|x64\r\n".format(u2, p)
                postsolution += "\t\t{0}.Debug-{1}|x64.Build.0 = Debug-{1}|x64\r\n".format(u2, p)
                postsolution += "\t\t{0}.Debug-{1}|x86.ActiveCfg = Debug-{1}|Win32\r\n".format(u2, p)
                postsolution += "\t\t{0}.Debug-{1}|x86.Build.0 = Debug-{1}|Win32\r\n".format(u2, p)
            for p in self.configs.iterate():
                postsolution += "\t\t{0}.Release-{1}|x64.ActiveCfg = Release-{1}|x64\r\n".format(u2, p)
                postsolution += "\t\t{0}.Release-{1}|x64.Build.0 = Release-{1}|x64\r\n".format(u2, p)
                postsolution += "\t\t{0}.Release-{1}|x86.ActiveCfg = Release-{1}|Win32\r\n".format(u2, p)
                postsolution += "\t\t{0}.Release-{1}|x86.Build.0 = Release-{1}|Win32\r\n".format(u2, p)
               
        return sln_template.format(project_includes.strip(), presolution.rstrip(), postsolution.rstrip())
            
    
    def do_it(self, root_folder):        
        folder = root_folder
        os.makedirs(folder)
        os.makedirs(folder + '/src')

        gitignore = file('gitignore_template.txt', 'rb').read()                
        file(folder + '/.gitignore', 'wb').write(gitignore)        
        main_cpp = file('main.cpp', 'rb').read()        
        include_cpp = file('include.cpp', 'rb').read()        
        include_h = file('include.h', 'rb').read()        
        file(folder + '/src/main.cpp', 'wb').write(main_cpp)
        file(folder + '/src/include.cpp', 'wb').write(include_cpp)
        file(folder + '/src/include.h', 'wb').write(include_h)

        for vs_version in ['vs2010', 'vs2015']:
            folder = root_folder + '/' + vs_version
            os.makedirs(folder)
            sln = self.create_sln(vs_version)
            file(folder + os.sep + self.name + '.sln', 'wb').write(sln)
            
            if vs_version == 'vs2015':
                platform_toolset = 'v140'
            if vs_version == 'vs2010':
                platform_toolset = 'v100'
                
            for p in self.projects:    
                project_name = p.name
                proj = p.create_project(self.configs, platform_toolset)
                file(folder + os.sep + project_name + '.vcxproj', 'wb').write(proj)
                filters = p.create_filters(self.uuid)
                file(folder + os.sep + project_name + '.vcxproj.filters', 'wb').write(filters)
                prop = file(vs_version + '_module.props', 'rb').read().format(p.module_name)  
                file(folder + os.sep + project_name + '.props', 'wb').write(prop)

            prop = file('vs2015_python.props', 'rb').read()
            file(folder + os.sep + 'python.props', 'wb').write(prop)
    
##################################################################################################################################    
          
class project_configuration_combiner(object):
    def __init__(self, *args):
        self.args = args
    def iterate(self):
        for x in itertools.product(*self.args):
            yield '-'.join(x)


            
            
            
    