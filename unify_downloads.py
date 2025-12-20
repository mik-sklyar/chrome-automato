from rename_by_date import rename_files_using_dates
import config

def unify_downloads():
    download_paths = set()
    for scheme in config.Config.schemes.value:
        download_paths.add(scheme.download_path)
    for path in download_paths :
        rename_files_using_dates(path, "jpeg:jpg,mp4", True)


if __name__ == '__main__':
    unify_downloads()
