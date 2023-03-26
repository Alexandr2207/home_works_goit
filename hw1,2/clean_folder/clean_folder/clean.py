import os
from pathlib import Path
import shutil
import sys



CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
"f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g"
)
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

def normalize(name: str):
    return name.translate(TRANS)


if len(sys.argv) < 2:
    print("Параметр не введено")
    exit()

folder_path = Path(sys.argv[1])

if not folder_path.exists() or not folder_path.is_dir():
    print("Введено невалідний шлях до теки")
    exit()

# ключі будуть назвою папок
extensions = {
    'IMAGES': ['jpeg', 'png', 'jpg', 'svg'],
    'VIDEO': ['avi', 'mp4', 'MOV', 'mkv'],
    'DOCS': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
    'MUSIC': ['mp3', 'ogg', 'wav', 'amr'],
    'ARCHIVES': ['zip', 'gz', 'tar']
}

# створює папки з ключів словника
def create_folders(folder_path, folder_names):
    for folder in folder_names:
        if not (folder_path / folder).exists():
            (folder_path / folder).mkdir()


# переміщення
def move_file(target_folder:Path, file:Path):
    extension = file.suffix.replace('.', '')
    for cat, ext in extensions.items():
        if extension in ext:
            print(f'Переміщую {file.name} в папку {(target_folder / cat).name} \n')
            file.replace(target_folder / cat / normalize(file.name))
            return None
    print(f'Переміщую {file.name} в папку {(target_folder).name} \n')
    file.replace(target_folder / normalize(file.name))
    return None


# сортуєм файли 
def sort_files(folder_path:Path):
    for file in folder_path.glob('**/*.*'):
        move_file(folder_path, file)
            

# розпакоувка
def unpack_archives(folder_path: Path):
    for file in folder_path.glob('*'):
        if file.is_file() and file.suffix in ('.zip', '.gz', '.tar'):
            print(f'Розпаковую {file.name} в папку {folder_path.name} \n')
            shutil.unpack_archive(str(file), str(folder_path))
            file.unlink()  
        elif file.is_dir():
            unpack_archives(file)  


#видаляємо пусті папки  
def remove_empty_folders(folder_path: Path):
    for folder in folder_path.glob('*'):
        if folder.is_dir():
            remove_empty_folders(folder)
            if not any(folder.iterdir()):
                folder.rmdir()
                print(f'Видаляю пусту папку {folder}')




def main():
    main_path = Path(sys.argv[1])
    create_folders(main_path, extensions.keys())
    sort_files(main_path)
    unpack_archives(main_path)
    remove_empty_folders(main_path)

if __name__ == '__main__':
    main()
