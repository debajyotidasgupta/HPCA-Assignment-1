"""
+-----------------------------------------------------+
|               HPCA Assignment - 1                   |
+-----------------------------------------------------+
|                    GROUP - 5                        |
+-----------------------------------------------------+
|   RollNo.   |          Name                         |
+-----------------------------------------------------+
|  18CS30051  |   Debajyoti Dasgupta                  |
|  18CS30050  |   Archisman Pathak                    |
|  18CS30047  |   Somnath Jena                        |
|  18CS30048  |   Rounak Patra                        |
|  18CS30044  |   Tushar Gupta                        |
|  18CS30045  |   Vaishnavi R. Munghate               |
|  18CS30046  |   Vattikuti Rahul Naga Sri Bharadhwaj |
|  18CS30049  |   Abhinav Bohra                       |
|  18CS30052  |   Chakka Venugopal                    |
|  18CS30053  |   Kothapalli Dileep                   |
|  18EC10047  |   Rudrajyoti Roy                      |
|  18EC10075  |   Ayan Chakraborty                    |
|  21CD91R10  |   Shubhi Shukla                       |
+-----------------------------------------------------+
|            Description of the program               |
+-----------------------------------------------------+
+-----------------------------------------------------+
|       Language:  Python3                            |
|       File name: options.py                       |
|       License:   MIT Open Source License            |
|       Year:      2021-2022 Spring Semester          |
|       Course:    High Performance Computer Arch.    |
+-----------------------------------------------------+
"""

# Add the very basic options that work also in the case of the no ISA
# being used, and consequently no CPUs, but rather various types of
# testers and traffic generators.


"""
[*] Add Argument Parser for the script
[*] Add the No ISA arguments for the argument parser
    [*] The arguments are:
        1. l1d_size      - L1 data cache size         (type: str)
        2. l1i_size      - L1 instruction cache size  (type: str)
        3. l2_size       - L2 cache size              (type: str)
        4. l1_assoc      - L1 cache associativity     (type: int)
        5. l2_assoc      - L2 cache associativity     (type: int)
"""


def addNoISAOptions(parser):
    parser.add_argument('--l1d_size', default='64kB',
                        help='L1 data cache size', type=str)
    parser.add_argument('--l1i_size', default='32kB',
                        help='L1 instruction cache size', type=str)
    parser.add_argument('--l2_size', default='128kB',
                        help='L2 cache size', type=str)
    parser.add_argument('--l1_assoc', default=2,
                        help='L1 cache associativity', type=int)
    parser.add_argument('--l2_assoc', default=2,
                        help='L2 cache associativity', type=int)
# Add common options that assume a non-NULL ISA.


"""
[*] Add the common arguments for the argument parser
    [*] The arguments are:
        1. bp_type       - Branch predictor type      (type: str)
        2. numROBEntries - Number of ROB entries      (type: int)
        3. numIQEntries  - Number of IQ entries       (type: int)
"""


def addCommonOptions(parser):
    # start by adding the base options that do not assume an ISA
    addNoISAOptions(parser)

    parser.add_argument('--bp_type', default='TournamentBP')
    parser.add_argument('--numROBEntries', default=128,
                        help='Number of ROB entries', type=int)
    parser.add_argument('--numIQEntries', default=64,
                        help='Number of IQ entries', type=int)

    parser.add_argument(
        "--stats-root", action="append", default=[],
        help="If given, dump only stats of objects under the given SimObject. "
        "SimObjects are identified with Python notation as in: "
        "system.cpu[0].mmu. All elements of an array can be selected at "
        "once with: system.cpu[:].mmu. If given multiple times, dump stats "
        "that are present under any of the roots. If not given, dump all "
        "stats. ")


"""
[*] Add the simulation options for the argument parser
    [*] The arguments are:
        1. cmd           - Command to run in syscall emulation mode.
        2. options       - Options to pass to the command.
        3. env           - Environment to pass to the command.
        4. input         - Input to pass to the command.
        5. output        - Output to redirect to.
        6. errout        - Error output to redirect to.
        7. chroot        - The chroot option allows a user to alter the
        8. interp-dir    - The interp-dir option is used for
        9. redirects     - A collection of one or more redirect paths
        10. wait-gdb     - Wait for remote GDB to connect.
"""


def addSEOptions(parser):
    # Benchmark options
    parser.add_argument('-b', '--benchmark', default='', type=str)
    parser.add_argument("-c", "--cmd", default="",
                        help="The binary to run in syscall emulation mode.")
    parser.add_argument("-o", "--options", default="",
                        help="""The options to pass to the binary, use " "
                              around the entire string""")
    parser.add_argument("-e", "--env", default="",
                        help="Initialize workload environment from text file.")
    parser.add_argument("-i", "--input", default="",
                        help="Read stdin from a file.")
    parser.add_argument("--output", default="",
                        help="Redirect stdout to a file.")
    parser.add_argument("--errout", default="",
                        help="Redirect stderr to a file.")
    parser.add_argument("--chroot", action="store", type=str, default=None,
                        help="The chroot option allows a user to alter the "
                        "search path for processes running in SE mode. "
                        "Normally, the search path would begin at the "
                        "root of the filesystem (i.e. /). With chroot, "
                        "a user can force the process to begin looking at"
                        "some other location (i.e. /home/user/rand_dir)."
                        "The intended use is to trick sophisticated "
                        "software which queries the __HOST__ filesystem "
                        "for information or functionality. Instead of "
                        "finding files on the __HOST__ filesystem, the "
                        "process will find the user's replacment files.")
    parser.add_argument("--interp-dir", action="store", type=str,
                        default=None,
                        help="The interp-dir option is used for "
                        "setting the interpreter's path. This will "
                        "allow to load the guest dynamic linker/loader "
                        "itself from the elf binary. The option points to "
                        "the parent folder of the guest /lib in the "
                        "host fs")

    parser.add_argument("--redirects", action="append", type=str,
                        default=[],
                        help="A collection of one or more redirect paths "
                        "to be used in syscall emulation."
                        "Usage: gem5.opt [...] --redirects /dir1=/path/"
                        "to/host/dir1 --redirects /dir2=/path/to/host/dir2")
    parser.add_argument("--wait-gdb", default=False, action='store_true',
                        help="Wait for remote GDB to connect.")
