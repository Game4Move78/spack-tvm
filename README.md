Not: this package does not build the Python package dependencies e.g. numpy

# Known issues

Unable to build LLVM13 on arm64 with kernel version <4.15 if LLDB is enabled. 
See:
https://github.com/llvm/llvm-project/issues/52823
https://github.com/spack/spack/issues/27992

Resolved by adding `^llvm targets=all ~lldb` or `^llvm@12.0.1 targets=all` to the end of spec
