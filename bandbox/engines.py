"""
Engines perform analyses on the tree. They are all run concurrently for performance.

quick wins
- [DONE] detect redundant dirs [S2.a]
- [DONE] detect obvious folders e.g tiff/*.tif* [S2.b]
- [DONE] detect excessive files per directory [S2.c]
- detect directories with mixed files [S3.a]
- detect cryptic names (against a dictionary) [N1]
- detect dates in names [N1.b]
- detect accessions e.g. 'EMPIAR' [N1.c]
- detect mixed case in names [N2.a]
- detect periods in names [N2.a]
- detect odd characters in names [N2.b]
- detect long names [N2.d]
- detect inconsistent names [N3.a]
- detect external references e.g. 'figure' [N3.c]
- detect words to avoid e.g. 'files', 'data' [N3.c]
- detect missing padding [N3.e]
- detect embedded paths (needs file format library) [N3.f]
- detect unknown extensions [M1.a]
- detect proprietary extensions [M1.b]
- detect presence of documentation e.g. README [M2.a]
- detect presence of checksums [M3]
- detect hard links
- detect symbolic links
- detect broken symbolic links
"""

import bandbox
import styled


async def _report(dirs: list, rule_text: str, fail_text: str = '') -> None:
    """Reporting function"""
    print(styled.Styled(f"[[ '{rule_text.ljust(60)}'|bold ]]"), end=" ")
    if dirs:
        if fail_text:
            print(styled.Styled(f"[[ '{fail_text.rjust(40)}'|fg-red:bold ]]"))
        else:
            fail_text = f"fail [{len(dirs)} directories]".rjust(40)
            print(styled.Styled(f"[[ '{fail_text}'|fg-red:bold ]]"))
        for item in dirs:
            print(f"  * {item}")
    else:
        ok_text = "ok".rjust(40)
        print(styled.Styled(f"[[ '{ok_text}'|fg-green:bold ]]"))
    print()


async def s2_detect_redundant_directories(tree, args):
    """Detect the presence of redundant directories

    A directory is redundant if:
    - it is empty
    - it is non-empty but is the only child of a parent folder
    """
    # empty folders
    empty_folders = tree.find_empty_directories(include_root=args.include_root)
    await _report(empty_folders, f"S2 - redundant directories...")


async def s2_detect_obvious_folders(tree, args):
    """Detect obvious folders"""
    obvious_folders = tree.find_obvious_folders(include_root=args.include_root)
    await _report(obvious_folders, f"S2 - obvious directory names...")


async def s2_detect_excessive_files_per_directory(tree, args):
    """Detect excessive files per directory"""
    excess_files = tree.find_excessive_files_per_directory()
    await _report(excess_files, f"S2 - excessives (>{bandbox.MAX_FILES}) files per directory...")


async def s3_detect_directories_with_mixed_files(tree, args):
    """Detect folders with mixed files"""
    mixed_files = tree.find_directories_with_mixed_files()
    await _report(mixed_files, f"S3 - directories with mixed files...")


async def n2_detect_long_names(tree, args):
    """Detect entities with very long names"""
    # print(f"info: working on {tree} with {args}...")
    dirs = tree.find_long_names()
    await _report(dirs, f"N2 - long names (>{bandbox.MAX_NAME_LENGTH} chars)...")
