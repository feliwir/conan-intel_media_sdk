#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from conans import ConanFile
import os


class IntelMediaSDKConan(ConanFile):
    name = "intel_media_sdk"
    version = "2017R1"
    url = "https://github.com/bincrafters/conan-intel_media_sdk"
    description = "Keep it short"
    license = "MIT"
    exports = ["LICENSE.md"]
    settings = {"os": ["Windows"], "arch": ["x86", "x86_64"]}
    source_subfolder = 'intel_media_sdk'

    def source(self):
        source_url = "https://github.com/SSE4/intel_media_sdk.git"
        self.run('git clone %s --depth 1 --branch %s' % (source_url, self.version))

    def package(self):
        self.copy(pattern="Media_SDK_EULA.rtf", dst="licenses", src=self.source_subfolder)
        self.copy(pattern="mediasdk_release_notes.pdf", dst="licenses", src=self.source_subfolder)
        self.copy(pattern="redist.txt", dst="licenses", src=self.source_subfolder)
        self.copy(pattern="redist.txt", dst="licenses", src=self.source_subfolder)

        self.copy(pattern="*.h", dst=os.path.join('include', 'mfx'), src=os.path.join(self.source_subfolder, 'include'))
        if self.settings.arch == 'x86':
            self.copy(pattern="*.lib", dst="lib", src=os.path.join(self.source_subfolder, 'lib', 'Win32'),
                      keep_path=True)
            self.copy(pattern="*.dll", dst="bin", src=os.path.join(self.source_subfolder, 'bin', 'Win32'),
                      keep_path=True)
        elif self.settings.arch == 'x86_64':
            self.copy(pattern="*.dll", dst="bin", src=os.path.join(self.source_subfolder, 'bin', 'Win32'),
                      keep_path=True)
            self.copy(pattern="*.lib", dst="lib", src=os.path.join(self.source_subfolder, 'lib', 'x64'),
                      keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ['libmfx_vs2015']
        self.cpp_info.includedirs.append(os.path.join(self.package_folder, 'include', 'mfx'))
