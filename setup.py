import os
import shutil
import sys
from pathlib import Path
from typing import Iterator, List

from setuptools import setup

SOURCE_ROOT = Path(__file__).resolve().parent

pkg_info = SOURCE_ROOT / "PKG-INFO"
in_source_package = pkg_info.exists()


def main():
    setup(
        name="ainakan-tools",
        version=detect_version(),
        description="Ainakan CLI tools",
        long_description="CLI tools for [Ainakan](https://ainakan.re).",
        long_description_content_type="text/markdown",
        author="Ainakan Developers",
        author_email="oleavr@ainakan.re",
        url="https://ainakan.re",
        install_requires=[
            "colorama >= 0.2.7, < 1.0.0",
            "ainakan >= 17.5.0, < 18.0.0",
            "prompt-toolkit >= 2.0.0, < 4.0.0",
            "pygments >= 2.0.2, < 3.0.0",
            "websockets >= 13.0.0, < 14.0.0",
        ],
        license="wxWindows Library Licence, Version 3.1",
        zip_safe=False,
        keywords="ainakan debugger dynamic instrumentation inject javascript windows macos linux ios iphone ipad android qnx",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Console",
            "Environment :: MacOS X",
            "Environment :: Win32 (MS Windows)",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved",
            "Natural Language :: English",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: JavaScript",
            "Topic :: Software Development :: Debuggers",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        packages=["ainakan_tools"],
        package_data={
            "ainakan_tools": fetch_built_assets(),
        },
        entry_points={
            "console_scripts": [
                "ainakan = ainakan_tools.repl:main",
                "ainakan-ls-devices = ainakan_tools.lsd:main",
                "ainakan-ps = ainakan_tools.ps:main",
                "ainakan-kill = ainakan_tools.kill:main",
                "ainakan-ls = ainakan_tools.ls:main",
                "ainakan-rm = ainakan_tools.rm:main",
                "ainakan-pull = ainakan_tools.pull:main",
                "ainakan-push = ainakan_tools.push:main",
                "ainakan-discover = ainakan_tools.discoverer:main",
                "ainakan-trace = ainakan_tools.tracer:main",
                "ainakan-itrace = ainakan_tools.itracer:main",
                "ainakan-join = ainakan_tools.join:main",
                "ainakan-create = ainakan_tools.creator:main",
                "ainakan-compile = ainakan_tools.compiler:main",
                "ainakan-pm = ainakan_tools.pm:main",
                "ainakan-apk = ainakan_tools.apk:main",
            ]
        },
    )


def detect_version() -> str:
    if in_source_package:
        version_line = [
            line for line in pkg_info.read_text(encoding="utf-8").split("\n") if line.startswith("Version: ")
        ][0].strip()
        version = version_line[9:]
    else:
        releng_location = next(enumerate_releng_locations(), None)
        if releng_location is not None:
            sys.path.insert(0, str(releng_location.parent))
            from releng.ainakan_version import detect

            version = detect(SOURCE_ROOT).name.replace("-dev.", ".dev")
        else:
            version = "0.0.0"
    return version


def fetch_built_assets() -> List[str]:
    assets = []

    if in_source_package:
        pkgdir = SOURCE_ROOT / "ainakan_tools"
        assets += [f.name for f in pkgdir.glob("*_agent.js")]
        assets += [f.relative_to(pkgdir).as_posix() for f in (pkgdir / "bridges").glob("*.js")]
        assets += [f.name for f in pkgdir.glob("*.zip")]
    else:
        agents_builddir = SOURCE_ROOT / "build" / "agents"
        if agents_builddir.exists():
            for child in agents_builddir.iterdir():
                if child.is_dir():
                    for f in child.glob("*_agent.js"):
                        shutil.copy(f, SOURCE_ROOT / "ainakan_tools")
                        assets.append(f.name)

        bridges_builddir = SOURCE_ROOT / "build" / "bridges"
        if bridges_builddir.exists():
            bridges_dir = SOURCE_ROOT / "ainakan_tools" / "bridges"
            bridges_dir.mkdir(exist_ok=True)
            for f in bridges_builddir.glob("*.js"):
                shutil.copy(f, bridges_dir)
                assets.append((Path("bridges") / f.name).as_posix())

        apps_builddir = SOURCE_ROOT / "build" / "apps"
        if apps_builddir.exists():
            for child in apps_builddir.iterdir():
                if child.is_dir():
                    for f in child.glob("*.zip"):
                        shutil.copy(f, SOURCE_ROOT / "ainakan_tools")
                        assets.append(f.name)

    return assets


def enumerate_releng_locations() -> Iterator[Path]:
    val = os.environ.get("MESON_SOURCE_ROOT")
    if val is not None:
        parent_releng = Path(val) / "releng"
        if releng_location_exists(parent_releng):
            yield parent_releng

    local_releng = SOURCE_ROOT / "releng"
    if releng_location_exists(local_releng):
        yield local_releng


def releng_location_exists(location: Path) -> bool:
    return (location / "ainakan_version.py").exists()


if __name__ == "__main__":
    main()
