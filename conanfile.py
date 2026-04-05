import os
from conans import ConanFile, CMake, tools

class cmockalibConan(ConanFile):
    name = "cproducer"
    version = "1.4.1"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "https://github.com/elear-solutions/amazon-kinesis-video-streams-producer-c.git"
    homepage = "https://github.com/awslabs/amazon-kinesis-video-streams-producer-c.git"
    description = "Amazon kinesis video streams C producer library"
    topics = ("c", "unit", "testing")
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = {
        "shared": [True, False]
    }
    default_options = {
        "shared": False
    }

    def _get_install_channel(self):
        """
        Get dependency channel with fallback logic.
        
        Priority:
        1. INSTALL_CHANNEL environment variable (explicit override - any channel)
        2. 'master' (production default)
        """
        install_channel = os.getenv('INSTALL_CHANNEL')
        if install_channel:
            return install_channel
        return 'master'

    def requirements(self):
        default_user = self.user if self.user else "jenkins"
        install_channel = self._get_install_channel()
        self.requires("OpenSSL/1.0.2r@%s/%s" % (default_user, install_channel))
        self.requires("curl/7.63.0@%s/%s" % (default_user, install_channel))

    def build(self):
        cmake = CMake(self)

        cmake.definitions["BUILD_DEPENDENCIES"] = False
        cmake.definitions["OPENSSL_ROOT_DIR"] = self.deps_cpp_info["OpenSSL"].rootpath
        cmake.definitions["CURL_ROOT"] = self.deps_cpp_info["curl"].rootpath

        cmake.configure(source_folder=".")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="src/include/")
        self.copy("*.h", dst="include", src="dependency/libkvspic/kvspic-src/src/client/include")
        self.copy("*.h", dst="include", src="dependency/libkvspic/kvspic-src/src/common/include")
        self.copy("*.h", dst="include", src="dependency/libkvspic/kvspic-src/src/duration/include")
        self.copy("*.h", dst="include", src="dependency/libkvspic/kvspic-src/src/heap/include")
        self.copy("*.h", dst="include", src="dependency/libkvspic/kvspic-src/src/mkvgen/include")
        self.copy("*.h", dst="include", src="dependency/libkvspic/kvspic-src/src/state/include")
        self.copy("*.h", dst="include", src="dependency/libkvspic/kvspic-src/src/trace/include")
        self.copy("*.h", dst="include", src="dependency/libkvspic/kvspic-src/src/utils/include")
        self.copy("*.h", dst="include", src="dependency/libkvspic/kvspic-src/src/view/include")
        self.copy("*.so", dst="lib", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [ "cproducer" ]
