# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/ahaddon/Programs/bocop/BocopHJB-1.1.0-Linux

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/build

# Include any dependencies generated for this target.
include CMakeFiles/bocophjb.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/bocophjb.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/bocophjb.dir/flags.make

CMakeFiles/bocophjb.dir/core/main.cpp.o: CMakeFiles/bocophjb.dir/flags.make
CMakeFiles/bocophjb.dir/core/main.cpp.o: /home/ahaddon/Programs/bocop/BocopHJB-1.1.0-Linux/core/main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/bocophjb.dir/core/main.cpp.o"
	g++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/bocophjb.dir/core/main.cpp.o -c /home/ahaddon/Programs/bocop/BocopHJB-1.1.0-Linux/core/main.cpp

CMakeFiles/bocophjb.dir/core/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/bocophjb.dir/core/main.cpp.i"
	g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/ahaddon/Programs/bocop/BocopHJB-1.1.0-Linux/core/main.cpp > CMakeFiles/bocophjb.dir/core/main.cpp.i

CMakeFiles/bocophjb.dir/core/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/bocophjb.dir/core/main.cpp.s"
	g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/ahaddon/Programs/bocop/BocopHJB-1.1.0-Linux/core/main.cpp -o CMakeFiles/bocophjb.dir/core/main.cpp.s

CMakeFiles/bocophjb.dir/core/main.cpp.o.requires:

.PHONY : CMakeFiles/bocophjb.dir/core/main.cpp.o.requires

CMakeFiles/bocophjb.dir/core/main.cpp.o.provides: CMakeFiles/bocophjb.dir/core/main.cpp.o.requires
	$(MAKE) -f CMakeFiles/bocophjb.dir/build.make CMakeFiles/bocophjb.dir/core/main.cpp.o.provides.build
.PHONY : CMakeFiles/bocophjb.dir/core/main.cpp.o.provides

CMakeFiles/bocophjb.dir/core/main.cpp.o.provides.build: CMakeFiles/bocophjb.dir/core/main.cpp.o


# Object files for target bocophjb
bocophjb_OBJECTS = \
"CMakeFiles/bocophjb.dir/core/main.cpp.o"

# External object files for target bocophjb
bocophjb_EXTERNAL_OBJECTS =

/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/bocophjb: CMakeFiles/bocophjb.dir/core/main.cpp.o
/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/bocophjb: CMakeFiles/bocophjb.dir/build.make
/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/bocophjb: /home/ahaddon/Programs/bocop/BocopHJB-1.1.0-Linux/core/lib/libbocophjbcore.a
/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/bocophjb: CMakeFiles/bocophjb.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable /home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/bocophjb"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/bocophjb.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/bocophjb.dir/build: /home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/bocophjb

.PHONY : CMakeFiles/bocophjb.dir/build

CMakeFiles/bocophjb.dir/requires: CMakeFiles/bocophjb.dir/core/main.cpp.o.requires

.PHONY : CMakeFiles/bocophjb.dir/requires

CMakeFiles/bocophjb.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/bocophjb.dir/cmake_clean.cmake
.PHONY : CMakeFiles/bocophjb.dir/clean

CMakeFiles/bocophjb.dir/depend:
	cd /home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ahaddon/Programs/bocop/BocopHJB-1.1.0-Linux /home/ahaddon/Programs/bocop/BocopHJB-1.1.0-Linux /home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/build /home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/build /home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/build/CMakeFiles/bocophjb.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/bocophjb.dir/depend

