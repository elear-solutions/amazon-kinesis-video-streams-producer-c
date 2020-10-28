from conans import ConanFile, CMake, tools

class cmockalibConan(ConanFile):
    name = "amazon-kinesis-video-streams-producer-c"
    version = "0.1.0"
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

    def build(self):
        self.run("apt-get update")
        self.run("apt-get install git -y")
        cmake = CMake(self)
        cmake.configure(source_folder=".")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="include")
        self.copy("*", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [ "cproducer" ]
