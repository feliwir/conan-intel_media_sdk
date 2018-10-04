#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from conans import ConanFile, tools
import os


class IntelMediaSDKConan(ConanFile):
    name = "intel_media_sdk"
    version = "2018R2"
    url = "https://github.com/bincrafters/conan-intel_media_sdk"
    description = "Intel® Media SDK provides an API to access hardware-accelerated video decode, encode and " \
                  "filtering on Intel® platforms with integrated graphics."
    license = "MIT"
    exports = ["LICENSE.md"]
    settings = {"os": ["Windows"], "arch": ["x86", "x86_64"], "compiler": ["Visual Studio"]}

    def source(self):
        source_url = "http://registrationcenter-download.intel.com/akdlm/irc_nas/vcp/13618/MSDK2018R2.exe"
        tools.download(source_url, 'MSDK2018R2.exe')

    def build(self):
        for action in ['remove', 'install']:
            self.run('MSDK2018R2.exe '
                     '%s '
                     '--silent '
                     '--installdir=%s '
                     '--eval '
                     '--eula=accept '
                     '--output=out.txt '
                     '--send-data=no '
                     '--update=always' % (action, os.getcwd()))

    def package(self):
        install_dir = os.path.join('Intel(R) Media SDK 2018 R2', 'Software Development Kit')

        self.copy(pattern="Media_SDK_EULA.rtf", dst="licenses", src=install_dir)
        self.copy(pattern="mediasdk_release_notes.pdf", dst="licenses", src=install_dir)
        self.copy(pattern="redist.txt", dst="licenses", src=install_dir)
        self.copy(pattern="redist.txt", dst="licenses", src=install_dir)

        self.copy(pattern="*.h", dst=os.path.join('include', 'mfx'), src=os.path.join(install_dir, 'include'))
        if self.settings.arch == 'x86':
            self.copy(pattern="*.lib", dst="lib", src=os.path.join(install_dir, 'lib', 'Win32'),
                      keep_path=True)
            self.copy(pattern="*.dll", dst="bin", src=os.path.join(install_dir, 'bin', 'Win32'),
                      keep_path=True)
        elif self.settings.arch == 'x86_64':
            self.copy(pattern="*.dll", dst="bin", src=os.path.join(install_dir, 'bin', 'Win32'),
                      keep_path=True)
            self.copy(pattern="*.lib", dst="lib", src=os.path.join(install_dir, 'lib', 'x64'),
                      keep_path=True)

        with tools.chdir(os.path.join(self.package_folder, 'lib')):
            if int(str(self.settings.compiler.version)) >= 14:
                os.unlink('libmfx.lib')
                os.rename('libmfx_vs2015.lib', 'libmfx.lib')
            else:
                os.unlink('libmfx_vs2015.lib')

    def package_info(self):
        self.cpp_info.libs = ['libmfx']
        self.cpp_info.includedirs.append(os.path.join(self.package_folder, 'include', 'mfx'))
        if self.settings.compiler.runtime != 'MT':
            # libmfx.lib unfortunately has /DEFAULTLIB:LIBCMT, there is nothing better to be done
            self.cpp_info.exelinkflags.append("-NODEFAULTLIB:LIBCMT")
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
