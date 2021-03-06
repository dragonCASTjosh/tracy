from conans import ConanFile, CMake

class TracyClient(ConanFile):
    name = 'tracy_client'
    version = 'master'
    license = 'BSD'
    description = 'A real time, nanosecond resolution, remote telemetry frame profiler for games and other applications'
    url = 'https://bitbucket.org/Manu343726/tracy/src/master'

    exports_sources = '*.cpp', '*.hpp', '*.h', 'CMakeLists.txt'

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {
        'TRACY_ENABLE': [True, False],
        'TRACY_ON_DEMAND': [True, False],
        'TRACY_NO_EXIT': [True, False],
        'TRACY_NO_BROADCAST': [True, False],
        'TRACY_PORT': 'ANY',
        'TRACY_USE_CONSTEXPR_VARIABLES': [True, False]
    }
    default_options = {
        'TRACY_ENABLE': True,
        'TRACY_ON_DEMAND': False,
        'TRACY_NO_EXIT': False,
        'TRACY_NO_BROADCAST': False,
        'TRACY_PORT': 8086,
        'TRACY_USE_CONSTEXPR_VARIABLES': True
    }

    def build(self):
        cmake = CMake(self)
        cmake.verbose = True
        cmake.configure(defs={
            'TRACY_ENABLE': self.options.TRACY_ENABLE,
            'TRACY_ON_DEMAND': self.options.TRACY_ON_DEMAND,
            'TRACY_NO_EXIT': self.options.TRACY_NO_EXIT,
            'TRACY_NO_BROADCAST': self.options.TRACY_NO_BROADCAST,
            'TRACY_PORT': self.options.TRACY_PORT,
            'TRACY_USE_CONSTEXPR_VARIABLES': self.options.TRACY_USE_CONSTEXPR_VARIABLES
        })
        cmake.build()

    def package(self):
        self.copy('*.h', dst='include')
        self.copy('*.hpp', dst='include')
        self.copy('*.a', dst='lib')
        self.copy('*.lib', dst='lib')

    def package_info(self):
        self.cpp_info.libs = ['tracy_client']

        if self.options.TRACY_ENABLE:
            if not self.settings.os == 'Windows':
                self.cpp_info.cxxflags = ['-pthread']
                self.cpp_info.system_libs = ['dl', 'pthread']

            self.cpp_info.defines = ['TRACY_ENABLE']

        if self.options.TRACY_ON_DEMAND:
            self.cpp_info.defines.append('TRACY_ON_DEMAND')

        if self.options.TRACY_NO_EXIT:
            self.cpp_info.defines.append('TRACY_NO_EXIT')

        if self.options.TRACY_NO_BROADCAST:
            self.cpp_info.defines.append('TRACY_NO_BROADCAST')

        self.cpp_info.defines.append('TRACY_PORT={}'.format(self.options.TRACY_PORT))

        if self.options.TRACY_USE_CONSTEXPR_VARIABLES:
            self.cpp_info.defines.append('TRACY_USE_CONSTEXPR_VARIABLES')
