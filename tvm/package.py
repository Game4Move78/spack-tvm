# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install tvm
#
# You can edit this file again by typing:
#
#     spack edit tvm
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import sys

class Tvm(CMakePackage):
    """
    Apache TVM is an open source machine learning compiler framework for
    CPUs, GPUs, and machine learning accelerators. It aims to enable machine
    learning engineers to optimize and run computations efficiently on any
    hardware backend.
    """

    homepage = "https://tvm.apache.org/"
    url      = "https://github.com/apache/tvm/releases/download/v0.8.0/apache-tvm-src-v0.8.0.tar.gz"
    maintainers = ['Game4Move78']

    git = "https://github.com/apache/tvm.git"

    version('main', branch='main')
    version('0.8.0', sha256='519fe65d27ca5f67c571ead2f5254d800890dc09baa3cd3a41142166de30a8c7')
    version('0.7.0', sha256='3a9906ac76adc9923b02832c53eea62ebaed0564ff80febff21c71da5a118')
    version('0.6.1', sha256='288d4d4413b4a179f01b86ba3c676840fe1cc472f0581c5489f6ab6736d6e012')
    version('0.6.0', sha256='bc83bbe87ecafbb047645a643534f845477def2b07121dd5139578a469fee5d7')

    generator = "Ninja"

    variant("cuda",
            default=False, description="Build with CUDA enabled")
    variant("llvm",
            default=True, description="Build with llvm support")
    variant("libbacktrace",
            default=(sys.platform == "darwin" or sys.platform == "linux"),
            description="Build with line and column information on stack traces")
    variant("rocm",
            default=False,
            description="Build with ROCM runtime enabled")
    variant("sdaccel",
            default=False,
            description="Build with SDAccel runtime enabled")
    variant("aocl",
            default=False,
            description="Build with Intel FPGA SDK for OpenCL (AOCL) runtime enabled")
    variant("opencl",
            default=False,
            description="Build with OpenCL runtime enabled")
    variant("metal",
            default=(sys.platform == "darwin"),
            description="Build with Metal runtime enabled")
    # variant("vulkan",
    #         default=False,
    #         description="Build with Vulkan runtime enabled")
    variant("opengl",
            default=False,
            description="Build with OpenGL runtime enabled")
    variant("micro",
            default=False,
            description="Build with MicroTVM runtime enabled")
    variant("rpc",
            default=True,
            description="Build with RPC runtime enabled")
    variant("cpp_rpc",
            default=False,
            description="Build with C++ RPC runtime enabled")
    variant("ios_rpc",
            default=False,
            description="Build with C++ RPC runtime enabled")

    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
    )

    depends_on('ninja', type="build")

    depends_on('llvm targets=all', when="+llvm")

    with when('+rocm'):
        depends_on('rocm-cmake')
        depends_on('hip')

    depends_on('opencl', when="+opencl")

    # depends_on('vulkan', when="+vulkan")

    depends_on('opengl', when="+opengl")

    depends_on('python@3.7:3.9')
    depends_on('cmake@3.5:')
    depends_on('ncurses+termlib')
    depends_on('libedit')
    depends_on('libxml2')
    depends_on('py-setuptools')
    depends_on('py-cython')
    depends_on('py-decorator')
    depends_on('py-psutil')
    depends_on('py-scipy')
    depends_on('py-numpy')

    depends_on('cuda@8.0:', when="+cuda")

    conflicts('%gcc@:5',
              msg = "C++14 support is required to build tvm")

    # executables = ['tvmc']

    def cmake_args(self):
        # Based on https://github.com/apache/tvm/tree/main/conda/recipe/build.sh

        spec = self.spec
        define = self.define
        from_variant = self.define_from_variant

        python = spec['python']
        cmake_args = [
        ]

        if "+cuda" in "spec":
            cmake_args.extend([
                define("USE_CUDA", spec["cuda"].prefix),
                define("USE_CUBAS", True),
                define("USE_CUDNN", True)
            ])

        if "+opencl" in "spec":
            cmake_args.extend([
                define("USE_OPENCL", spec["opencl"].prefix),
            ])

        # if "+vulkan" in "spec":
        #     cmake_args.extend([
        #         define("USE_VULKAN", spec["vulkan"].prefix),
        #     ])

        if spec.platform == "darwin":
            cmake_args.extend([
                define("USE_METAL", True),
            ])

        cmake_args.extend([
            define("USE_RPC", True),
            define("USE_CPP_RPC", False),
            define("USE_SORT", True),
            define("USE_RANDOM", True),
            define("USE_PROFILER", True),
            from_variant("USE_LLVM", "llvm"),
            from_variant("USE_ROCM", "rocm"),
            from_variant("USE_AOCL", "aocl"),
            from_variant("USE_METAL", "metal"),
            from_variant("USE_OPENGL", "opengl"),
            from_variant("USE_MICRO", "micro"),
            from_variant("USE_RPC", "rpc"),
            from_variant("USE_CPP_RPC", "cpp_rpc"),
            from_variant("USE_IOS_RPC", "ios_rpc"),
            from_variant("USE_LIBBACKTRACE", "libbacktrace"),
            define("INSTALL_DEV", True),
        ])
        return cmake_args

    @run_after("install")
    def post_install(self):
        # put $TVM_HOME/python on PYTHONPATH
        install_tree("python", python_platlib)
