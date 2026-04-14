import tarfile
import os
import sys

exclude_files = [".tmp", ".log", ".stdout", ".stderr"]


def filterFunction(tarinfo):
    """
    Filter unwanted files while creating tarball.

    Skips files with extensions in exclude_files.
    """

    ext = os.path.splitext(tarinfo.name)[1]

    if ext in exclude_files:
        return None

    return tarinfo


def make_tarfile(source_dir, output_filename):
    """
    Create a gzipped tarball of a directory.

    Parameters
    ----------
    output_filename : str
        Name of output tar.gz file
    source_dir : str
        Directory to archive
    """

    with tarfile.open(output_filename, "w:gz") as tar:
        print("make_tarfile:: Started creating tar file...")

        tar.add(
            source_dir,
            arcname=os.path.basename(source_dir),
            filter=filterFunction
        )

        print("make_tarfile:: Done...")