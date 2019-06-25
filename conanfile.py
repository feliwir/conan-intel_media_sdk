#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from conans import ConanFile, tools, CMake
import os


class IntelMediaSDKConan(ConanFile):
    name = "intel-mediasdk"
    version = "19.1.0"
    url = "https://github.com/bincrafters/conan-intel_media_sdk"
    description = "Intel® Media SDK provides an API to access hardware-accelerated video decode, encode and " \
                  "filtering on Intel® platforms with integrated graphics."
    author = "Bincrafters <bincrafters@gmail.com>"
    topics = {"video","decoding","acceleration","intel"}

    license = "MIT"
    homepage = "https://software.intel.com/en-us/media-sdk"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = {"os": ["Windows", "Linux"], "arch": ["x86", "x86_64"]}
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': False, 'fPIC': True}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        source_url = "https://github.com/Intel-Media-SDK/MediaSDK/archive/"
        tools.get("{0}/{1}-{2}.tar.gz".format(source_url, self.name, self.version),
                  sha256="fbb617112bfdc6602a621f97a480c71dc272a4a433c66a3ce3f5c3695e7e91be")
        extracted_dir = "MediaSDK-" + self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("COPYING", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
