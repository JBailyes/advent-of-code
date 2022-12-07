from aocutils import load_input
import re


class FileInfo():
    def __init__(self, name, size) -> None:
        self.size: int = size
        self.name: str = name


class DirInfo():
    def __init__(self, name: str, parent):
        self.name: str = name
        self.parent = parent
        self.dirs: dict = {}
        self.files = []
        if parent:
            self.path = f'{parent.path}/{name}'
        else:
            self.path = '/'
    
    def add_child(self, child):
        if not child.name in self.dirs:
            self.dirs[child.name] = child
        if child.parent is None:
            child.parent = self

    def size(self):
        total = 0
        for file in self.files:
            total += file.size
        for subdir in self.dirs.values():
            total += subdir.size()
        return total


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    root = DirInfo('/', None)
    cwd = root
    
    all_dirs: dict[str, DirInfo] = {}
    all_dirs.setdefault('/', root)

    for line in puzzle_input[1:]:
        if line.startswith('$'):
            print(line.split(' '))
            op = line.split(' ')[1]
            if op == 'cd':
                path = line.split(' ')[2]
                if path == '..':
                    cwd = cwd.parent
                elif path == '/':
                    cwd = root
                else:
                    subdir = DirInfo(path, cwd)
                    if not subdir.path in all_dirs: 
                        all_dirs[subdir.path] = subdir
                        cwd.add_child(subdir)
                    else:
                        subdir = all_dirs[subdir.path]
                    cwd = subdir
        else:
            filematch = re.match(r'^(\d+) (.*)', line)
            if filematch:
                filesize = int(filematch.group(1))
                filename = filematch.group(2)
                newfile = FileInfo(filename, filesize)
                cwd.files.append(newfile)
            elif line.startswith('dir'):
                subdir_name = line.split(' ')[1]
                subdir = DirInfo(subdir_name, cwd)
                if not subdir.path in all_dirs: 
                    all_dirs[subdir.path] = subdir
                    cwd.add_child(subdir)


    target = root.size() - 40_000_000

    candidates = []
    for dir in all_dirs.values():
        dirsize = dir.size()
        if dirsize >= target:
            candidates.append(dirsize)

    print(min(candidates))

    # Correct answer: 214171


if __name__ == "__main__":
    main()
