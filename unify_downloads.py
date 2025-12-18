from rename_by_date import rename_files_using_dates


def unify_downloads():
    rename_files_using_dates("Downloads", "jpeg:jpg,mp4", True)


if __name__ == '__main__':
    unify_downloads()
